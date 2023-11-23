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


    def play(self, debug = False):
        if len(self.PlayerList) == 1: # V1 of the game, ie: player against a random boat grid
            nb = 0
            self.PlayerList[0].introV1()

            while(not self.PlayerList[0].allSunk()):
                self.PlayerList[0].showGrid(debug)
                self.PlayerList[0].playV1()
                nb += 1

            outroV1(nb)