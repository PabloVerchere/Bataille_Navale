from . import Boat
from . import Data

# Print a text with a given color
def print_color(text : str, color : str, end = True):
    if end:
        print(color + color + text + Data.colorReset)
    else:
        print(str(color) + str(color) + str(text) + Data.colorReset, end = "")


# Init the tab of boats with the data from Data.py
def initTabBoat():
    TabBoat = []

    for name, size in Data.Boats.items():
        TabBoat.append(Boat.Boat(name, size))

    return TabBoat


# Message to stop the game and show number of turns
def outro(self, n : int):
        print("""
#######################################################################
################# Bravo, vous avez gagné, en""", n, """coups #################
#######################################################################
        """)
        if n <= 17:
            print("###########################   Tricheur !!   ###########################")
            print("#######################################################################")
