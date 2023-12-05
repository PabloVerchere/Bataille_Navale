from . import Boat
from . import Data
from . import Coordinates

from random import randint


# Init the tab of boats with the Boats from Data.py
def initTabBoat():
    TabBoat = []

    for name, size in Data.Boats.items():
        TabBoat.append(Boat.Boat(name, size))

    return TabBoat


# Print a text with a given color
def print_color(text : str, color : str, end = True):
    if end:
        print(color + color + text + Data.colorReset)
    else:
        print(str(color) + str(color) + str(text) + Data.colorReset, end = "") # No end line


# Clear the screen
def clearScreen():
    print(Data.clear, end = "")


# Message to stop the game and show the winner in a 2 players game
def outro2(n : int, win :str):
        print("""
#######################################################################
################# Bravo,""", win, """ a gagné en""", n, """coups ###########
#######################################################################""")


# DEBUG, show the grid
def printGrid(grid : list):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] < 10:
                print(str(0 + grid[i][j]), end = "  ")
                print(grid[i][j], end = " ")
        print()


# Ask the player to enter a valid coord and return it
def valid_dir():
    print("Direction (0-H / 1-V) :", end="")
    direction = int(input())

    while direction != 0 and direction != 1: # While the direction is not 0 or 1
        print("Direction (0-H / 1-V) :", end="")
        direction = int(input())

    return direction