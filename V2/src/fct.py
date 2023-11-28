from . import Boat
from . import Data
from . import Coordinates

from random import randint

# Print a text with a given color
def print_color(text : str, color : str, end = True):
    if end:
        print(color + color + text + Data.colorReset)
    else:
        print(str(color) + str(color) + str(text) + Data.colorReset, end = "")


# Clear the screen
def clearScreen():
    print(Data.clear, end = "")


# Init the tab of boats with the Boats from Data.py
def initTabBoat():
    TabBoat = []

    for name, size in Data.Boats.items():
        TabBoat.append(Boat.Boat(name, size))

    return TabBoat


# Message to stop the game and show number of turns in V1
def outroV1(n : int):
        print("""
#######################################################################
################# Bravo, vous avez gagné, en""", n, """coups #################
#######################################################################""")



# Message to stop the game and show the winner in V2
def outroV2(n : int, win :str):
        print("""
#######################################################################
################# Bravo,""", win, """ a gagné en""", n, """coups ###########
#######################################################################""")



# Return the coord of the max value in the grid
def maxCoGrid(grid : list):
    max = grid[0][0]
    coord = Coordinates.Coordinates(0, 0)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] > max:
                max = grid[i][j]
                coord = Coordinates.Coordinates(i, j)

    return coord



# DEBUG, show the grid
def printGrid(grid : list):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] < 10:
                print(str(0 + grid[i][j]), end = "  ")
            else:
                print(grid[i][j], end = " ")
        print()


# Return (-1, -1) if the value is not in the grid, the coord otherwise
def is_In_Grid(value : int, grid : list):
    l = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == value:
                l.append(Coordinates.Coordinates(i, j))
    
    if l != []:
        return l[randint(0, len(l) - 1)]
    else: 
        return Coordinates.Coordinates(-1, -1)