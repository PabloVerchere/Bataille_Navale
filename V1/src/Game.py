from . import Player
from .fct import *


class Game:
    def __init__(self):
        self.player = Player.Player() # Create a player


    # Player against a random boat grid
    def play(self, debug = False):
            nb = 0 # Number of turns
            clearScreen()
            self.player.intro()

            while(not self.player.allSunk()): # While all the boats are not sunk, we continue playing
                self.player.showGrid(debug)
                self.player.play()
                nb += 1 # Increment the number of turns

                input("Continuer...")
                clearScreen()

            self.player.showGrid(debug)
            outro(nb) # Show the outro, when the game is finished
