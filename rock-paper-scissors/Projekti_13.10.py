"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Student Id: 150281685
Name:       Miska Pajukangas
Email:      miska.pajukangas@tuni.fi

Kivi-paperi-sakset peli graafisella käyttöliittymällä. Ohjelmassa tähdättiin
kehittyneen käyttöliittymän luomiseen.

Pelin toteutuksessa hyödynnetään kolmea ikkunaa, josta ensimmäinen on pelin
aloitusikkuna. Kyseisessä ikkunassa käyttäjältä vaaditaan valintaa mikäli hän
tahtoo aloittaa pelin vai sulkea ohjelman.

Pelin alettua aloitusvalikko suljetaan ja uusi ikkuna avataan, ikkunassa
on ohjeistus, jonka mukaan voittaja päätetään "best of three"-periaatteella,
joka käytännössä tarkoittaa, sitä joka kykenee kolmesta erästä
voittamaan enemmistön. Tällöin siis kaksi erää ensimmäisenä voittanut on
voittanut pelin.

Jos ei ole ennestään tuttu niin kivi-paperi-sakset pelin periaate on seuraava:
Kivi voittaa sakset, mutta häviää paperille ja sakset voittaa paperin.

Käyttäjä tekee valintansa kolmen radiopainikkeen välillä, joissa on pelin
siirron mahdolliset valinnat.

Tekstikenttä radiopainikkeiden yllä osoittaa käyttäjälle, että vastustaja
on valmis pelaamaan ja odottavansa siirtoa. Ensimmäisen erän jälkeen teksti
muuttuu osoittamaan, että käyttäjä voi suorittaa seuraavan siirron.

Alapuolella ohjelma näyttää kunkin erän tuloksen ja vastustajan valinnan
tekstinä sekä kuvana. Näiden alapuolella on myös tulostaulukko, joka näyttää
jokaisen erän pistetilanteen ja kuinka monta erää on kulunut pelin alkamisesta.

Yhden pelin päätyttyä ohjelmaan avautuu pop-up ikkuna, joka vaatii käyttäjältä
valintaa tahtoo hän jatkaa peliä, uuden pelin aloittaessa kaikki edelliset ikkunat
sulkeutuvat ja ohjelman toiminta alkaa uudelleen "peli-ikkunasta". Tämän lisäksi 
edellisen pelin tulos viedään parametrina seuraavaa peliä varten. Mikäli pelaaja 
ei halua jatkaa, niin ohjelman toiminta päättyy siihen.
"""

from tkinter import *
import random


class Game:
    """
    Luokka pitää sisällään kaikki ohjelman suoritukseen liittyvät toiminnot
    main funktiota lukuunottamatta, joka käynnistää luokan.

    __init__ metodissa määritellään aloitusikkunan toiminnot, mutta suurin osa
    peliin liittyvistä komennoista on määritelty myöhemmässä vaiheessa, sillä
    ohjelman toiminta on hajautettu kolmeen tkinter-ikkunaan.
    """

    def __init__(self, winStreak):
        """
        Luo pääikkunan tkinter-ohjelmaan. Antaa käyttäjälle valinnan
        pelin aloittamisen ja ohjelmasta poistumisen välillä
        :param winStreak: int, aiemmin voitetut pelit
        """
        # Edellisten voitettujen pelien määrä, oletuksena -1 ensimmäiselle
        # pelille pisteiden laskemisen selkeyttämiseksi
        self.__winStreak = winStreak

        if self.__winStreak == -1:

            self.__mainWindow = Tk()

            # Keskittää aloitusikkunan näytön koon perusteella
            screenWidth = self.__mainWindow.winfo_screenwidth()
            screenHeight = self.__mainWindow.winfo_screenheight()
            windowWidth = 500
            windowHeight = 100
            x = (screenWidth / 2) - (windowWidth / 2)
            y = (screenHeight / 2) - (windowHeight / 2)
            self.__mainWindow.geometry('%dx%d+%d+%d' % (windowWidth,
                                                        windowHeight,
                                                        x, y))

            self.__greeting = Label(self.__mainWindow,
                                    text="Welcome to Rock, Paper, Scissors!",
                                    font=("Helvetica", 22,))
            self.__greeting.pack()
            
            # Suorittaa playWindow metodin
            self.__startGame = Button(self.__mainWindow,
                                      text="Start Game",
                                      command=self.playWindow)
            self.__startGame.pack()

            self.__quitGame = Button(self.__mainWindow,
                                     text="Quit",
                                     command=quit, )
            self.__quitGame.pack()

            self.__playerScore = 0
            self.__opponentScore = 0
            self.__roundCounter = 0

            # Asetetaan attribuutit None arvoon __init__ metodissa, sillä ne
            # määritellään vasta myöhemmässä vaiheessa muissa metodeissa
            self.__gameWindow = None
            self.__anotherGame = None
            self.__answer = None
            self.__info = None
            self.__rockButton = None
            self.__paperButton = None
            self.__scissorsButton = None
            self.__result = None
            self.__resultOpponent = None
            self.__scoreBoard = None
            self.__playersChoice = None
            self.__opponentChoice = None
            self.__img1 = None
            self.__img2 = None
            self.__img3 = None

            self.__mainWindow.mainloop()

        # Avaa peli-ikkunan suoraan, mikäli peli ei ollut ensimmäinen, eli
        # toisin sanoen self.__winStreak on arvossa 0
        else:
            self.__playerScore = 0
            self.__opponentScore = 0
            self.__roundCounter = 0

            self.playWindow()

    def playWindow(self):
        """
        Pelin aloitettua tuhoaa edellisen aloitusvalikon
        ja luo pelivalikon jossa ohjelman päätoiminnallisuus on toteutettu.
        Käyttäjä saa aluksi ohjeistuksen pelin kulusta, ja viittauksen
        valitsemaan yhden kolmesta vaihtoehdosta.

        Ensimmäisen valinnan jälkeen peli alkaa, jolloin ohjelma tiedottaa
        käyttäjää mikä erän tulos oli, näyttäen myös vastustajan valintaa
        vastaavan kuvan. Alaosassa on tämän lisäksi vielä tulostaulukko, joka
        näyttää kunkin osapuolen pisteet ja erälukeman.
        :returns: None
        """
        # Tuhoaa pääikkunan ja avaa uuden ikkunan peliä varten jos peli on
        # ensimmäinen
        if self.__winStreak == -1:
            self.__mainWindow.destroy()

        self.__gameWindow = Tk()

        # Keskittää peli-ikkunan näytön koon perusteella
        screenWidth = self.__gameWindow.winfo_screenwidth()
        screenHeight = self.__gameWindow.winfo_screenheight()
        windowWidth = 500
        windowHeight = 550
        x = (screenWidth / 2) - (windowWidth / 2)
        y = (screenHeight / 2) - (windowHeight / 2)
        self.__gameWindow.geometry('%dx%d+%d+%d' % (windowWidth,
                                                    windowHeight,
                                                    x, y))

        self.__info = Label(
            text="The winner will be the best out of three rounds!"
                 "\n\nYour opponent is waiting, \nselect your choice below!",
            font=('Helvetica', 16)
        )
        self.__info.pack()

        # Määrittelee pelaajan vastauksen merkkijonomuuttujaksi
        self.__answer = StringVar()

        self.__rockButton = Radiobutton(self.__gameWindow,
                                        text="Rock",
                                        font=("Helvetica", 13),
                                        variable=self.__answer,
                                        value="Rock",
                                        command=self.selection
                                        )
        self.__rockButton.pack()

        self.__paperButton = Radiobutton(self.__gameWindow,
                                         text="Paper",
                                         variable=self.__answer,
                                         font=("Helvetica", 13),
                                         value="Paper",
                                         command=self.selection
                                         )
        self.__paperButton.pack()

        self.__scissorsButton = Radiobutton(self.__gameWindow,
                                            text="Scissors",
                                            variable=self.__answer,
                                            font=("Helvetica", 13),
                                            value="Scissors",
                                            command=self.selection,
                                            )
        self.__scissorsButton.pack()

        # Alla olevat "Labelit" muuttuvat tulosten perusteella, jotka
        # määritellään muissa metodeissa
        self.__result = Label()
        self.__result.pack()

        self.__resultOpponent = Label()

        self.__resultOpponent.pack()

        self.__scoreBoard = Label()
        self.__scoreBoard.pack(side=BOTTOM)

    def selection(self):
        """
        Tässä metodissa käsitellään ohjelman toiminnallisuutta.
        Vastustajan valinta on määritelty random-kirjaston choice-toiminnon
        avulla, joka valitsee sattumanvaraisesti kyseisen siirron.

        Pelaajan ja vastustajan valintojen pohjalta ohjelma uudelleenkonfiguroi
        kuvan vastaamaan vastustajan valintaa ja myös pistetilanteen
        lähettämällä kierrostuloksen resultOfRound-metodiin.
        :returns: None
        """
        # Pelaajan valinta haetaan radiopainikkeen variable-arvosta
        self.__playersChoice = self.__answer.get()
        # Vastustajan eli tietokoneen valinta tehdään random-kirjaston avulla
        self.__opponentChoice = random.choice(["Rock", "Paper", "Scissors"])

        self.__info.configure(text="The winner will be the best out of three "
                                   "rounds!\n\nSelect your next choice!",
                              font=('Helvetica', 16))

        # Määritellään kuvat pysyviksi, jotta Pythonin "roskankerääjä" ei
        # poista niitä ennen käyttöä
        self.__img1 = PhotoImage(file="rock.png")
        self.__img2 = PhotoImage(file="paper.png")
        self.__img3 = PhotoImage(file="scissors.png")

        # Muuttaa kuvan vastaamaan käyttäjän valintaa siinä tilanteessa, jossa
        # vastustajan valinta oli sama kuin käyttäjän.
        playersChoicePhoto = None  # Muuttujan arvo ennen valintaa

        if self.__playersChoice == "Rock":
            playersChoicePhoto = self.__img1

        if self.__playersChoice == "Paper":
            playersChoicePhoto = self.__img2

        if self.__playersChoice == "Scissors":
            playersChoicePhoto = self.__img3

        # Kivi-paperi-sakset pelin toiminnan runko-osuus, lähettää kunkin
        # kierroksen tuloksen resultOfRound-metodiin
        if self.__opponentChoice == self.__playersChoice:
            self.resultOfRound("draw")
            # Kuva joka vastaa pelaajan valintaa
            self.__resultOpponent.configure(image=playersChoicePhoto)

        elif self.__opponentChoice == "Rock":
            self.__resultOpponent.configure(image=self.__img1)

            if self.__playersChoice == "Paper":
                self.resultOfRound("won")
            else:
                self.resultOfRound("lost")

        elif self.__opponentChoice == "Paper":
            self.__resultOpponent.configure(image=self.__img2)

            if self.__playersChoice == "Scissors":
                self.resultOfRound("won")
            else:
                self.resultOfRound("lost")

        elif self.__opponentChoice == "Scissors":
            self.__resultOpponent.configure(image=self.__img3)

            if self.__playersChoice == "Rock":
                self.resultOfRound("won")
            else:
                self.resultOfRound("lost")

    def resultOfRound(self, result):
        """
        Tässä metodissa käsitellään kunkin kierroksen lopputulosta. Lopputulos
        saadaan kussakin if lausekkeessa olevalla resultOfRound-toiminnolla,
        joka lähettää merkkijonon parametrina tähän metodiin, määrittelemään
        voittiko vai hävisikö pelaaja, vai tuliko tasapeli. Lopussa myös
        tarkastellaan mikäli jompi kumpi pelaajista on saavuttanut kaksi
        pistettä.

        :param result: str, kierroksen lopputulos
        :returns: None
        """
        
        # Mikäli erän tulos on tasapeli, niin ainoastaan erien lkm kasvaa
        if result == "draw":
            self.__result.configure(text="\nIt's a draw!"
                                         "\nYour opponent chose..."
                                         f"\n{self.__answer.get()}",
                                    font=('Helvetica', 15))
            self.__roundCounter += 1

        if result == "lost":
            self.__result.configure(text="\nYou lost this round!"
                                         "\nYour opponent chose..."
                                         f"\n{self.__opponentChoice}",
                                    font=('Helvetica', 15))

            self.__opponentScore += 1
            self.__roundCounter += 1

        if result == "won":
            self.__result.configure(text="\nYou win this round!"
                                         "\nYour opponent chose..."
                                         f"\n{self.__opponentChoice}",
                                    font=('Helvetica', 15))
            self.__playerScore += 1
            self.__roundCounter += 1

        self.__scoreBoard.configure(text=f"The current scores are:"
                                         f"\nYou: {self.__playerScore}"
                                         f"\nOpponent: {self.__opponentScore}"
                                         f"\nRound counter: "
                                         f"{self.__roundCounter}",
                                    font=('Helvetica', 14),
                                    relief="ridge")
        
        # Jos saavutetaan kaksi pistettä, peli päättyy ja avaa uuden ikkunan
        if self.__opponentScore == 2 or self.__playerScore == 2:
            self.nextGameWindow()

    def nextGameWindow(self):
        """
        Tässä metodissa käsitellään pelin päättymistä, jossa jompi kumpi on
        saavuttanut kaksi pistettä.

        "Pop-up"-ikkuna kysyy käyttäjältä mikäli
        hän tahtoo jatkaa pelaamista, "Yes"-valinnalla ohjelma siirtyy
        metodiin restart ja "No"-valinnalla ohjelma sulkeutuu.
        :returns: None
        """

        # Pelin päätyttyä radiovalitsimet kytketään pois virhetilanteiden
        # ehkäisemisen vuoksi
        self.__rockButton.configure(state=DISABLED)
        self.__paperButton.configure(state=DISABLED)
        self.__scissorsButton.configure(state=DISABLED)

        self.__anotherGame = Tk()
        self.__anotherGame.eval('tk::PlaceWindow . center')

        if self.__playerScore == 2:
            # voittoputki on oletuksena ensimmäisellä pelikerralla -1
            # joten ensimmäiseen voittoon lisätään kaksi pistettä yhden sijaan
            if self.__winStreak == -1:
                self.__winStreak += 2
                
            else:
                self.__winStreak += 1

            # Onnitteluviesti muuttuu käyttäjän voittoputken perusteella
            # ja nollaantuu häviöstä
            if self.__winStreak >= 3:
                anotherGameText = Label(self.__anotherGame,
                                        text="Unbelievable!\n"
                                             "You are on a winning streak "
                                             f"of {self.__winStreak}!"
                                             "\n\nDo you wish to play "
                                             "another game?",
                                        font=('Helvetica', 16),
                                        foreground="#32CD32")
                anotherGameText.pack()

            elif self.__winStreak >= 2:
                anotherGameText = Label(self.__anotherGame,
                                        text="You are on a winning streak "
                                             f"of {self.__winStreak}!"
                                             "\n\nDo you wish to play "
                                             "another game?",
                                        font=('Helvetica', 16),
                                        foreground="#32CD32")
                anotherGameText.pack()

            else:
                anotherGameText = Label(self.__anotherGame,
                                        text="Congratulations, you won!"
                                             "\n\nDo you wish to play "
                                             "another game?",
                                        font=('Helvetica', 16),
                                        foreground="#32CD32")
                anotherGameText.pack()

        else:
            anotherGameText = Label(self.__anotherGame,
                                    text="You lost :( "
                                         "Better luck next time!"
                                         "\n\nDo you wish to play "
                                         "another game?",
                                    font=('Helvetica', 16),
                                    foreground="red")
            self.__winStreak = 0
            anotherGameText.pack()

        # Suorittaa restart metodin
        anotherGameButton = Button(self.__anotherGame, text="Yes",
                                   command=self.restart)

        anotherGameButton.pack()

        notAnotherGameButton = Button(self.__anotherGame, text="No",
                                      command=quit)
        notAnotherGameButton.pack()

    def restart(self):
        """
        Tuhoaa kaikki edelliset ikkunat ja "käynnistää" ohjelman
        uudelleen palaamalla main funktioon.
        :returns: None
        """
        self.__gameWindow.destroy()
        self.__anotherGame.destroy()
        main(self.__winStreak)


def main(winStreak):
    """
    Käynnistää Game-luokan, ja vie parametrinä edellisen pelin tuloksen
    :returns: None
    """
    Game(winStreak)


if __name__ == "__main__":
    main(winStreak=-1)
