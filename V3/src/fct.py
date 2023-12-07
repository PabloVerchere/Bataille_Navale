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


# DEBUG, show the grid passed
def printGrid(grid : list):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] < 10:
                print(str(0 + grid[i][j]), end = "  ")
            else:
                print(grid[i][j], end = " ")
        print()


# Ask the player to enter a valid direction and return it
def valid_dir():
    print("Direction (0-H / 1-V) :", end="")
    direction = input()

    # While direction is empty, not an int or not 0 or 1, ask again
    while len(direction) == 0 or not('0' <= direction <= '1'):
        print("Direction (0-H / 1-V) :", end="")
        direction = input()

    return int(direction)


# Return the coord of the max value in the grid (in they are multiple max, it return the higher, lefter)
def maxCoGrid(grid : list):
    max = grid[0][0]
    coord = Coordinates.Coordinates(0, 0)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] > max:
                max = grid[i][j]
                coord = Coordinates.Coordinates(i, j)

    return coord


# Return (-1, -1) if the value is not in the grid, the coord otherwise
def is_in_grid(value : int, grid : list):
    l = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == value:
                l.append(Coordinates.Coordinates(i, j))
    
    if l != []:
        return l[randint(0, len(l) - 1)] # Return a random coord in the list
    else: 
        return Coordinates.Coordinates(-1, -1)