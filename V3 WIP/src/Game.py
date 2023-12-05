from . import Player
from .fct import *


class Game:
    def __init__(self):
        self.playerList = []

        # Add players to the game
        self.playerList.append(Player.Player()) # Create a human player
        self.playerList.append(Player.Player(0)) # Create a bot player


    # Exchange the Boat's coord between the 2 players
    def exchange_coord(self):
        tmpB = self.playerList[0].TabBoat
        tmpC = self.playerList[0].TabCoord

        self.playerList[0].TabBoat = self.playerList[1].TabBoat
        self.playerList[0].TabCoord = self.playerList[1].TabCoord

        self.playerList[1].TabBoat = tmpB
        self.playerList[1].TabCoord = tmpC


    # Human player against a smart boat player
    def play(self, debug = False):
        nb = [0, 0]
        self.exchange_coord()

        # Init the heatmap for the bot
        

        clearScreen()
        self.playerList[0].introV1()


        # Bot
        print("Bot")
        heatmap = self.playerList[1].initHeatmap() # Init the heatmap for the bot, and play the first turn

        maxCo = maxCoGrid(heatmap) # Find the coord of the max value in the heatmap
        self.playerList[1].playCo(maxCo, heatmap)  # Play the 1rst coord (in the middle of the grid)
        heatmap = self.playerList[1].updateHeatmap(heatmap, maxCo)


        self.playerList[1].showGrid(debug)
        nb[1] += 1

        # Human
        print("Joueur")
        self.playerList[0].showGrid(debug)
        self.playerList[0].playV1()
        nb[0] += 1
        wait  = input("Continuer...")




        # While one of the player not sunk all the enemie fleet
        while(not self.playerList[0].allSunk()) and (not self.playerList[1].allSunk()):
                clearScreen()

                # Bot
                print("Bot")
                printGrid(heatmap) # Show the heatmap
                self.playerList[1].playBotSmart(heatmap)

                self.playerList[1].showGrid(debug)
                nb[1] += 1
                print()

                if not self.playerList[1].allSunk():
                    # Human
                    print("Joueur")
                    self.playerList[0].showGrid(debug)
                    self.playerList[0].playV1()
                    nb[0] += 1
                    input("Continuer...")


        if nb[1] > nb[0]:
            winner = "Joueur Ordi  "
            nW = nb[1]

        else:
            winner = "Joueur Humain "
            nW = nb[0]

        outro2(nW, winner)