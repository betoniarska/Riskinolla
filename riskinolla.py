from tkinter import *
from datetime import datetime

pelaaja = "0"
valimuisti = {} # Tallettaa pelihistorian pelin ajan

def click(r, s):
    """"Kutsutaan nappia painettaessa"""
    global pelaaja
    
    # Riippuen vuorosta muuttaa painetun napin tekstiä, sekä painetun indexin tilan
    if lauta[r][s]["text"] == "" and pelaaja == "*":
        lauta[r][s]["text"] = pelaaja
        pelaaja = "0"
        tila[r][s] = 1

    if lauta[r][s]["text"] == "" and pelaaja == "0":
        lauta[r][s]["text"] = pelaaja
        pelaaja = "*"
        tila[r][s] = 2

    paattyiko_peli() # Testaa jokaisen vuoron jälkeen onko voittoja

def lopetus(kumpi: bool):
    """Kertoo että peli on ohi"""
    # "kumpi", parametrin arvo kertoo voittajan: True = *, False = O
    if kumpi:
        
        # Luo näytölle tekstin, joka kertoo lopputuloksen
        voitto_teksti = Label(
                    text = "Riski voitti :)",
                    height = 2,
                    width = 10,
                    font = ("Helvetica", "20"),
                    fg="#FCCB16",
                    bg="#2C8F43")
        voitto_teksti.grid(row=1, column=1)

        tallennus(True) # Tallentaa lopputuloksen historia.txt tiedostoon

    else:
        voitto_teksti = Label(
                    text = "Riski hävisi :(",
                    height = 2,
                    width = 10,
                    font = ("Helvetica", "20"),
                    bg="#8B0000")
        voitto_teksti.grid(row=1, column=1)

        tallennus(False) # Tallentaa lopputuloksen historia.txt tiedostoon



def paattyiko_peli():
    """Testaa onko voittoa"""
    # Käy läpi kaikki mahdolliset voitot kummallakin pelaajalla: 1 = *, 2 = O
    # Jos löytää voiton kutsuu lopetus(bool): True = *, False = O

    #Tarkistaa vaakarivit
    for i in range(3):

        if tila[i][0] == 1 and tila[i][1] == 1 and tila[i][2] == 1:
            lopetus(True)
            
        elif tila[i][0] == 2 and tila[i][1] == 2 and tila[i][2] == 2:
            lopetus(False)


    # Tarkistaa pystyrivit
    for i in range(3):

        if tila[0][i] == 1 and tila[1][i] == 1 and tila[2][i] == 1:
            lopetus(True)

        if tila[0][i] == 2 and tila[1][i] == 2 and tila[2][i] == 2:
            lopetus(False)

    # Tarkistaa laskevan diagonaalin
    
    if tila[0][0] == 1 and tila[1][1] == 1 and tila[2][2] == 1:
        lopetus(True)

    elif tila[0][0] == 2 and tila[1][1] == 2 and tila[2][2] == 2:
        lopetus(False)

    # Tarkistaa nousevan diagonaalin

    if tila[2][0] == 1 and tila[1][1] == 1 and tila[0][2] == 1:
        lopetus(True)

    elif tila[2][0] == 2 and tila[1][1] == 2 and tila[0][2] == 2:
        lopetus(False)

def peli_historia():
    """Luo ikkunan missä näkyy pelihistoria"""

    historia_ikkuna = Tk()
    historia_ikkuna.title("Peli historia")
    historia_ikkuna.geometry("500x500")

    historiakentta = Listbox(historia_ikkuna)
    historiakentta.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(historia_ikkuna)
    scrollbar.pack(side=RIGHT, fill=BOTH)

    historiakentta.config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = historiakentta.yview)

    # Lisää välimuistin sisällön näkymään
    for avain in valimuisti:
        historiakentta.insert(END, avain + ": " + valimuisti[avain])


def nollaa_peli():
    """Nollaa tilamatriisin"""

    for lista in range(len(tila)):
        for alkio in range(len(tila[lista])):
            tila[lista][alkio] = 0

def hae():
    """Lukee tiedostosta historia.txt aiempien pelien ajankohdat ja lopputulokset"""
    try:
        with open("historia.txt") as t:
            
            for rivi in t:
                data = rivi.strip().split(",")
                # Kirjoittaa tiedot välimuistiin missä ajankohta on avain ja lopputulos arvo
                valimuisti[data[0]] = data[1]

    except FileNotFoundError:   # Ensimmäisellä kutsukerralla kerralla tiedostoa ei vielä ole olemassa
        pass

def tallennus(kumpi: bool):
    """Tallentaa uuden pelin lopputuloksen ja ajankohdan tiedostoon historia.txt"""
    
    aika = datetime.now() # Tallennetaan pelin päättymisen ajankohta

    # Lisätään sanakirjaan välimuisti uusi peli, missä avain = ajankohta ja arvo = tulos
    if kumpi: 
        valimuisti[str(aika)] = "Asteriski voitti" 
    else: 
        valimuisti[str(aika)] = "Asteriski hävisi"

    # Kirjoitetaan välimuisti historia.txt tiedostoon
    with open("historia.txt", "w") as t:
        for avain in valimuisti:
            t.write(avain + "," + valimuisti[avain] + "\n")


    
def luo_lauta():
    """Luo napit lauta matriisin mukaan"""

    hae() # Haetaan edelliset pelit tiedostosta välimuistiin

    # Luodaan pelinäkymä
    window = Tk()
    window.title("riskinolla")
    window.resizable(0,0)

    # Käydään matriisi "lauta" läpi ja luodaan jokaiseen alkioon nappi
    for rivi in range(3):

        for sarake in range(3):
            
            lauta[rivi][sarake] = Button(window,
                            text = "",
                            height = 5,
                            width = 8,
                            font = ("Helvetica", "25"),
                            command = lambda r = rivi, s = sarake : click(r, s)) 
            
            lauta[rivi][sarake].grid(row = rivi, column = sarake)
    
    # Pelihistoria nappi, avaa pelihistorianäkymän
    historia_nappi = Button(window,
                text = "Historia",
                height = 1,
                width = 4,
                font = ("Helvetica", "15"),
                command = peli_historia)
    historia_nappi.grid(row=4, column=2, padx=5, pady=5)

    # Luo uuden tyhjän pelin, tuhoaa edellisen ja nollaa tilanteen
    uusipeli_nappi = Button(window,
                text = "Uusi peli",
                height = 1,
                width = 4,
                font = ("Helvetica", "15"),
                command = lambda:[window.destroy(), luo_lauta(), nollaa_peli()])
    uusipeli_nappi.grid(row=4, column=0, padx=5, pady=5)

# Päälle luodaan napit          
lauta = [
        [0,0,0],
        [0,0,0],
        [0,0,0]]

# Pitää yllä pelin tilannetta (0 = "", 1 = *, 2 = O)
tila = [
        [0,0,0],
        [0,0,0],
        [0,0,0]]


luo_lauta()
mainloop()