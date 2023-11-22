from random import randint # border included

from . import Boat
from . import Coordinates
from . import Data

class Game():
    def __init__(self):
        self.gridHide = [[Data.HNothing] * 10 for i in range(10)] # Secret grid with boats placement, MAY NOT BE NECESSARY
        self.gridPlay = [[Data.PInit] * 10 for i in range(10)] # Grid to show to the player

        self.TabBoat = initTabBoat() # List of the boats
        self.placeBoatBot(self.TabBoat) # Place the boats randomly


    # Show the grid to the player
    def showGrid(self, debug = False): # NEED TO DO A FCT FOR THE COLORS
        # Xlab
        print(" " * 3, end = "")
        for i in range(10):
            print(i + 1, " ", end = "")
        print()

        # Grid + Ylab
        for i in range(10):
            print(chr(65 + i), " ", end = "") # A to J
            
            for j in range(10):
                if debug:
                    # If there is a boat print in yellow
                    if self.gridHide[i][j] == Data.HBoat:
                        print("\033[33m", end = "")
                        print(self.gridHide[i][j], " ", end = "")
                        print("\033[0m", end = "")

                    # If missed print in blue
                    elif self.gridHide[i][j] == Data.HWater:
                        print("\033[34m", end = "")
                        print(self.gridHide[i][j], " ", end = "")
                        print("\033[0m", end = "")

                    # If touched print in green
                    elif self.gridHide[i][j] == Data.HTouch:
                        print("\033[32m", end = "")
                        print(self.gridHide[i][j], " ", end = "")
                        print("\033[0m", end = "")

                    # If sunk print in red
                    elif self.gridHide[i][j] == Data.HSunk:
                        print("\033[31m", end = "")
                        print(self.gridHide[i][j], " ", end = "")
                        print("\033[0m", end = "")
                    else:
                        print(self.gridHide[i][j], " ", end = "")

                else:
                    # If missed print in blue
                    if self.gridPlay[i][j] == Data.PMiss:
                        print("\033[34m", end = "")
                        print(self.gridPlay[i][j], " ", end = "")
                        print("\033[0m", end = "")

                    # If touched print in green
                    elif self.gridPlay[i][j] == Data.PTouch:
                        print("\033[32m", end = "")
                        print(self.gridPlay[i][j], " ", end = "")
                        print("\033[0m", end = "")

                    # If sunk print in red
                    elif self.gridPlay[i][j] == Data.PSunk:
                        print("\033[31m", end = "")
                        print(self.gridPlay[i][j], " ", end = "")
                        print("\033[0m", end = "")
                    else:
                        print(self.gridPlay[i][j], " ", end = "")
                    
            print()
    

    def intro(self):
        print("""
#######################################################################
################## Bienvenue dans ma Bataille Navale ##################
#######################################################################
        """)
        print("Vous jouez contre l'ordinateur : il a placé ses bateaux aléatoirement.")
        
        print("Il dispose d’:")
        for boat in self.TabBoat:
            print(" -", boat.name, "(", boat.size, "cases)")

        print("""
Règles :
- Les bateaux ne peuvent être disposés qu’horizontalement ou verticalement, mais jamais en diagonale.
- Deux bateaux ne peuvent ni se chevaucher, ni être collés l’un à l'autre.
              
Prêt ? C'est parti, bonne chance !
              """)


    def outro(self, n : int):
        print("""
#######################################################################
################# Bravo, vous avez gagné, en""", n, """coups #################
#######################################################################
        """)


    # Check if the boat is in the grid
    def boat_in_grid(self, boat : Boat):
        inGrid = True

        if boat.dir: # Vertical
            if boat.coord.x + boat.size > 10:
                inGrid = False

        else:
            if boat.coord.y + boat.size > 10:
                inGrid = False

        return inGrid


    # Bool return of if we can place the boat or not
    def is_occuped(self, boat : Boat): # TO DO WITHOUT THE GRID
        occ = False
        occupedTile = occupedTile() # add all the tile yet use by other boat and then compare it to the boat wished placement 
        
        if boat.dir: # Vertical
            for i in range(boat.size):
                if self.gridHide[boat.coord.x + i][boat.coord.y] != 0: # Check if all the boat's cases are empty
                    occ = True
                    break

        else: # Horizontal
            for i in range(boat.size):
                if self.gridHide[boat.coord.x][boat.coord.y + 1] != 0: # Check if all the boat's cases are empty
                    occ = True
                    break

        return occ

    # Return a list of all the tile used by all the boat placed
    def occupedTile(self):
        Tile = [] # May be a game attribut

        for boat in self.TabBoat:
            if boat.coord.x > 0: # if the boat is placed
                if boat.dir: # V
                    for i in boat.size:
                        Tile.append(boat.coord + Coordinates(i, 0))

                else:
                    for i in boat.size:
                        Tile.append(boat.coord + Coordinates(0, i))

        return Tile


    # Place the boats automatically the boats
    def placeBoatBot(self, TabBoat : list): # BUG, NEED TO CHECK IT, or simply verify if there is 17 number 1
        i = 0
        # Select boat in descending order of size
        for boat in TabBoat:
            boat.dir = randint(0, 1) # H / V
            
            boat.coord.x = randint(0, 9)
            boat.coord.y = randint(0, 9)
            
            while(not self.boat_in_grid(boat) or self.is_occuped(boat)): # While the boat can't be placed, we try another position
                boat.dir = randint(0, 1)

                boat.coord.x = randint(0, 9)
                boat.coord.y = randint(0, 9)

                i += 1

                if i > 1000: # If we try too many times, we stop
                    print("ERROR: Can't place the boat")
                    break

            # Place the boat
            if boat.dir: # Vertical
                for i in range(boat.size):
                    self.gridHide[boat.coord.x + i][boat.coord.y] = 1
            else:
                for i in range(boat.size):
                    self.gridHide[boat.coord.x][boat.coord.y + i] = 1


    # Check if a boat is sunk
    def checkBoat(self, boat : Boat): # NOT WORKING
        if boat.state == 0: # If the boat is not sunk
            allTouched = True

            if boat.dir: # Vertical
                for i in range(boat.size):
                    if self.gridHide[boat.coord.x + i][boat.coord.y] == 1: # If one of the boat's cases is not touched, the boat is not sunk
                        allTouched = False
                        break

                # Update the grid if sunk
                if allTouched:
                    boat.state = 1 # Sunk
                    for i in range(boat.size):
                        self.gridHide[boat.coord.x + i][boat.coord.y] = 4
                        

            else: # Horizontal
                for i in range(boat.size):
                    if self.gridHide[boat.coord.x][boat.coord.y + i] == 1: # If one of the boat's cases is not touched, the boat is not sunk
                        allTouched = False
                        break

                # Update the grid if sunk
                if allTouched:
                    boat.state = 1 # Sunk
                    for i in range(boat.size):
                        self.gridHide[boat.coord.x][boat.coord.y + i] = 4
                        self.gridPlay[boat.coord.x][boat.coord.y + i] = Data.PSunk


    # Check all the boats
    def checkAllBoat(self):
        for boat in self.TabBoat:
            self.checkBoat(boat)


    # Update the grid
    def updateGrid(self, coord : Coordinates):
        if self.gridHide[coord.x][coord.y] == 1: # If there is a boat, we hit it
            self.gridHide[coord.x][coord.y] = 3
            self.gridPlay[coord.x][coord.y] = Data.PTouch

        else:
            self.gridHide[coord.x][coord.y] = 2 # If there is no boat, we miss it
            self.gridPlay[coord.x][coord.y] = Data.PMiss


    # Check if the coord is in the grid
    def co_in_grid(self, coord : Coordinates):
        inGrid = True

        if (coord.x < 0 or coord.x > 9) or (coord.y < 0 or coord.y > 9):
            inGrid = False

        return inGrid


    # Check if the case is already touched
    def already_touched(self, coord : Coordinates):
        not_valid = [2, 3, 4]

        touched = False

        if self.gridHide[coord.x][coord.y] in not_valid:
            touched = True

        return touched


    # Print the result of the shoot
    def printShoot(self, co : Coordinates):
        if(self.gridHide[co.x][co.y] == Data.HWater): # If we miss
            print(" - A l'eau - ")
        
        elif(self.gridHide[co.x][co.y] == Data.HTouch): # If we touch a boat 
            print(" - Touché - ")

        elif(self.gridHide[co.x][co.y] == Data.HSunk): # If we sunk a boat
            print(" - Coulé - ")

        print()







    # Make the player play
    def play(self):
        # Ask the player to enter a coord
        coord = input("\nCoordonnées (ex: A1) : ")
        coord = coord.upper() # Upper case
        coord = coord.strip() # Remove spaces

        # Split the string into alphabetic and numeric parts
        coord = ["".join(filter(str.isalpha, coord)), "".join(filter(str.isdigit, coord))]
 
        # Convert the coord
        co = Coordinates.Coordinates(ord(coord[0]) - 65, int(coord[1]) - 1)

        # Check if the coord is valid
        while self.already_touched(co) or not self.co_in_grid(co):
            coord = input("Coordonnées (ex: A1) : ")
            coord = coord.upper()
            coord = coord.strip()

            coord = ["".join(filter(str.isalpha, coord)), "".join(filter(str.isdigit, coord))]
            co = Coordinates.Coordinates(ord(coord[0]) - 65, int(coord[1]) - 1)

        # Update the grids
        self.updateGrid(co)
        # Check if a boat is sunk
        self.checkAllBoat()
        # Print the shoot
        self.printShoot(co)


    # Check if all the boats are sunk
    def allSunk(self):
        all = True

        for boat in self.TabBoat:
            if boat.state == 0: # If at least one of the boat is not sunk
                all = False
                break
        
        return all

    # V1 version of the game, ie: player against a random boat grid
    def V1(self):
        nb = 0
        self.intro()

        while(not self.allSunk()):
            self.showGrid()
            self.play()
            nb += 1

        self.outro(nb)





def initTabBoat(): # To move in fct.py
    TabBoat = []

    for name, size in Data.Boats.items():
        TabBoat.append(Boat.Boat(name, size))

    return TabBoat