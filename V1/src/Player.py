from random import randint # border included

from . import Boat
from . import Coordinates
from . import Data
from .fct import *


class Player():
    def __init__(self):
        self.grid = [[Data.Init] * 10 for i in range(10)] # Grid to show to the player
        self.TabBoat = initTabBoat() # List of the boats
        self.TabCoord = self.placeBoat(self.TabBoat) # Place the boats randomly and return the list of the occuped tiles


    # Place the boats automatically
    def placeBoat(self, TabBoat : list):
        i = 0
        occupedTile = []

        # Select boat in the TabBoat list
        for boat in TabBoat:
            boat.dir = randint(0, 1) # H / V
            
            boat.coord.x = randint(0, 9)
            boat.coord.y = randint(0, 9)
            
            # While the boat can't be placed, we try another position
            while((not self.boat_in_grid(boat)) or not boat.placeable(occupedTile)): # We verify if all the boat's tile are in the grid and if all the tile are not occuped
                boat.dir = randint(0, 1)

                boat.coord.x = randint(0, 9)
                boat.coord.y = randint(0, 9)

                i += 1

                if i > 1000: # If we try too many times, we stop
                    print_color("ERREUR : Impossible de placer le bateau", Data.colorRed)
                    break
            
            # Add the boat's tile to the list, for the next boat
            self.occupedTile(occupedTile, boat)

        return occupedTile
    

    # Add the boat's tiles to the list
    def occupedTile(self, Tile : list, boat : Boat):
        if boat.dir: # Vertical
            for i in range(boat.size):
                Tile.append(Coordinates.Coordinates(boat.coord.x + i, boat.coord.y))

        else: # Horizontal
            for i in range(boat.size):
                Tile.append(Coordinates.Coordinates(boat.coord.x, boat.coord.y + i))


    # Make the player play
    def play(self):
        co = self.askCoord()

        self.updateGrid(co)
        self.checkAllBoat()
        self.printShoot(co)


    # Ask the player to enter a coord
    def askCoord(self):
        valid = False # Init at False to enter the while loop

        while not valid:
            # Ask the coord
            coord = input("Coordonnées (ex: A1) : ")
            coord = coord.upper() # Upper case
            coord = coord.strip() # Remove spaces

            # Split the string into alphabetic and numeric parts
            coord = ["".join(filter(str.isalpha, coord)), "".join(filter(str.isdigit, coord))]

            # Verify if the coord in format "A1"
            if len(coord[0]) == 1 and (len(coord[1]) == 1 or len(coord[1]) == 2):
                # Convert the coord from string to Coordinates
                co = Coordinates.Coordinates(ord(coord[0]) - 65, int(coord[1]) - 1)

                # Verify if the coord is in the grid and if it's not already touched
                if self.co_in_grid(co) and not self.already_touched(co):
                    valid = True # If the coord is valid, we can exit the while loop

        return co


    # Check if the tile is already touched
    def already_touched(self, coord : Coordinates):
        return self.grid[coord.x][coord.y] != Data.Init


    # Check if the coord is in the grid
    def co_in_grid(self, coord : Coordinates):
        inGrid = True

        if (coord.x < 0 or coord.x > 9) or (coord.y < 0 or coord.y > 9):
            inGrid = False

        return inGrid
    

    # Check if the boat is in the grid
    def boat_in_grid(self, boat : Boat):
        inGrid = True

        if boat.dir: # Vertical
            if boat.coord.x + boat.size > 10: # If the bottom of the boat is out of the grid (we test for the top when asking the coord)
                inGrid = False

        else: # Horizontal
            if boat.coord.y + boat.size > 10: # If the right side of the boat is out of the grid (we test for the left when asking the coord)
                inGrid = False

        return inGrid
    

    # Update the grid with the coord played
    def updateGrid(self, coord : Coordinates):
        if coord.in_list(self.TabCoord):
            self.grid[coord.x][coord.y] = Data.Touch # If there is a boat, we hit it
        else:
            self.grid[coord.x][coord.y] = Data.Miss # If there is no boat, we miss it


    # Check if the boat is sunk
    def checkBoat(self, boat : Boat):
        if boat.state == 0: # If the boat is still not sunk

            if boat.dir: # Vertical
                for i in range(boat.size):
                    if self.grid[boat.coord.x + i][boat.coord.y] == Data.Init: # If one of the boat's tile is not yet touched, the boat is not sunk
                        break

                # Update the grid if sunk
                if allTouched:
                    boat.state = 1 # Sunk
                    for i in range(boat.size):
                        self.grid[boat.coord.x + i][boat.coord.y] = Data.Sunk
                        

            else: # Horizontal
                for i in range(boat.size):
                    if self.grid[boat.coord.x][boat.coord.y + i] == Data.Init: # If one of the boat's tile is not yet touched, the boat is not sunk
                        break

                # Update the grid if sunk
                if allTouched:
                    boat.state = 1 # Sunk
                    for i in range(boat.size):
                        self.grid[boat.coord.x][boat.coord.y + i] = Data.Sunk

        return boat.state


    # Check all the boats
    def checkAllBoat(self):
        for boat in self.TabBoat:
            if self.checkBoat(boat):
                return True
        return False


    # Print the result of the shoot
    def printShoot(self, co : Coordinates):
        print("Coordonnées:", chr(co.x + 65), int(co.y + 1))
        
        if(self.grid[co.x][co.y] == Data.Miss): # If we miss a boat
            print_color(" - A l'eau - ", Data.colorBlue)
        
        elif(self.grid[co.x][co.y] == Data.Touch): # If we touch a boat
            print_color(" - Touché - ", Data.colorGreen)

        elif(self.grid[co.x][co.y] == Data.Sunk): # If we sunk a boat
            print_color(" - Coulé - ", Data.colorRed)

        print()


    # Show the grid to the player
    def showGrid(self, debug = False):
        # Xlab
        print(" " * 3, end = "")
        for i in range(10):
            print(i + 1, " ", end = "")
        print()

        # Grid + Ylab
        for i in range(10):
            # Ylab
            print(chr(65 + i), " ", end = "") # A to J
            
            # Grid
            for j in range(10):
                if debug: # Show the grid with the boats
                    if Coordinates.Coordinates(i, j).in_list(self.TabCoord): # If there is a undiscovered boat
                        if self.grid[i][j] == Data.Init: # print the boat in Magenta
                            print_color(Data.Debug, Data.colorMagenta, False)
                        
                        elif self.grid[i][j] == Data.Touch: # If touched print in green
                            print_color(self.grid[i][j] + "  ", Data.colorGreen, False)

                        elif self.grid[i][j] == Data.Sunk: # If sunk print in red
                            print_color(self.grid[i][j] + "  ", Data.colorRed, False)

                    elif self.grid[i][j] == Data.Miss: # If missed print in blue
                        print_color(self.grid[i][j] + "  ", Data.colorBlue, False)

                    else:
                        print(self.grid[i][j], " ", end = "") # If there is nothing
                    

                else: # Show the grid without the boats
                    # If missed print in blue
                    if self.grid[i][j] == Data.Miss:
                        print_color(self.grid[i][j] + "  ", Data.colorBlue, False)

                    # If touched print in green
                    elif self.grid[i][j] == Data.Touch:
                        print_color(self.grid[i][j] + "  ", Data.colorGreen, False)

                    # If sunk print in red
                    elif self.grid[i][j] == Data.Sunk:
                        print_color(self.grid[i][j] + "  ", Data.colorRed, False)

                    else:
                        print(self.grid[i][j], " ", end = "")
                    
            print()
    

    # Show the text intro, boats in the game and rules
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
- Deux bateaux ne peuvent pas se chevaucher, mais peuvent être collés l’un à l'autre.
              
Prêt ? C'est parti, bonne chance !
              """)


    # Check if all the boats are sunk
    def allSunk(self):
        all = True

        for boat in self.TabBoat:
            if boat.state == 0: # If at least one of the boat is not sunk
                all = False
                break
        
        return all