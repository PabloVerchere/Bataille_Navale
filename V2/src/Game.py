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


    # Human player against a random boat player
    def play(self, debug = False,):
        nb = [0, 0] # Number of turns
        self.exchange_coord() # Exchange the coord of the boats between the 2 players, so each player play on in own grid

        clearScreen()
        self.playerList[0].intro() # Show the intro of the game (work for all the players, so we use the first one)

        # While one of the player not sunk all the enemie fleet
        while (not self.playerList[0].allSunk()) and (not self.playerList[1].allSunk()):
                clearScreen()

                # Bot
                print("Bot")
                self.playerList[1].playBot() # Play a random coord
                self.playerList[1].showGrid(debug) # Show the grid
                nb[1] += 1 # Increment the number of turns
                print()

                if not self.playerList[1].allSunk(): # If the bot not sunk all the player's fleet, the player can play
                    # Human
                    print("Joueur")
                    self.playerList[0].showGrid(debug) # Show the grid
                    self.playerList[0].playHuman() # Play a coord
                    nb[0] += 1 # Increment the number of turns
                    
                    input("Continuer...") # Wait for the player to press any key to continue


        # Return the winner and his number of turns
        if nb[1] > nb[0]:
            winner = "Joueur Ordi  "
            nW = nb[1]

        else:
            winner = "Joueur Humain"
            nW = nb[0]

        outro2(nW, winner)