from . import Player
from .fct import *

class Game:
    def __init__(self):
        self.PlayerList = []

        # Add players to the game
        n = int(input("Combien de joueurs ? (1 ou 2) : "))
        human = int(input("Combien de joueurs humains ? : "))

        if n == 1: # V1
            self.PlayerList.append(Player.Player(0)) # Create a bot player to place the boats, but it will play like a human

        else:
            for i in range(n):
                if i < human:
                    clearScreen()
                    print("Joueur", i + 1)
                    self.PlayerList.append(Player.Player()) # Create a human player
                else:
                    self.PlayerList.append(Player.Player(0)) # Create a bot player


    # Exchange the Boat's coord between the 2 players
    def exchange_coord(self):
        self.PlayerList[0].showGrid(1)
        self.PlayerList[1].showGrid(1)

        tmpB = self.PlayerList[0].TabBoat
        tmpC = self.PlayerList[0].TabCoord

        self.PlayerList[0].TabBoat = self.PlayerList[1].TabBoat
        self.PlayerList[0].TabCoord = self.PlayerList[1].TabCoord

        self.PlayerList[1].TabBoat = tmpB
        self.PlayerList[1].TabCoord = tmpC

        self.PlayerList[0].showGrid(1)
        self.PlayerList[1].showGrid(1)



        

    def play(self, debug = False):
        # V2
        nb = [0, 0]
        self.exchange_coord()

        clearScreen()
        self.PlayerList[0].introV1()

        # While one of the player not sunk all the enemie fleet
        while(not self.PlayerList[0].allSunk()) and (not self.PlayerList[1].allSunk()):
                clearScreen()

                print("Bot")
                for boat in self.PlayerList[1].TabBoat:
                    boat.print()

                print()
                print("Joueur")
                for boat in self.PlayerList[0].TabBoat:
                    boat.print()

                print()

                # Bot
                print("Bot")
                self.PlayerList[1].playBot()
                self.PlayerList[1].showGrid(debug)
                nb[1] += 1
                print()

                if not self.PlayerList[1].allSunk():
                    # Human
                    print("Joueur")
                    self.PlayerList[0].showGrid(debug)
                    self.PlayerList[0].playV1()
                    print("All sunk J", self.PlayerList[0].allSunk())
                    nb[0] += 1
                    wait  = input("Continuer...")


        if nb[1] > nb[0]:
            winner = "Joueur Ordi  "
            nW = nb[1]

        else:
            winner = "Joueur Humain"
            nW = nb[0]

        outroV2(nW, winner)