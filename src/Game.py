from random import randint # border included

from . import Boat
from . import Coordinates
from . import Data
from .fct import *


class Game():
    def __init__(self):
        self.grid = [[Data.Init] * 10 for i in range(10)] # Grid to show to the player

        self.TabBoat = initTabBoat() # List of the boats
        self.TabCoord = self.placeBoatBot(self.TabBoat) # Place the boats randomly and return the list of the occuped tiles


    # Show the grid to the player
    def showGrid(self, debug = False):
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
                    if Coordinates.Coordinates(i, j).in_list(self.TabCoord): 
                        if self.grid[i][j] == Data.Init: # If there is a undiscovered boat, print in Magenta
                            print_color("B  ", Data.colorMagenta, False)
                        
                        elif self.grid[i][j] == Data.Touch: # If touched print in green
                            print_color(self.grid[i][j] + "  ", Data.colorGreen, False)

                        elif self.grid[i][j] == Data.Sunk: # If sunk print in red
                            print_color(self.grid[i][j] + "  ", Data.colorRed, False)

                    elif self.grid[i][j] == Data.Miss: # If missed print in blue
                        print_color(self.grid[i][j] + "  ", Data.colorBlue, False)

                    else:
                        print(self.grid[i][j], " ", end = "")
                    

                else:
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


    # Check if the boat is in the grid
    def boat_in_grid(self, boat : Boat):
        inGrid = True

        if boat.dir: # Vertical
            if boat.coord.x + boat.size > 10:
                inGrid = False

        else: # Horizontal
            if boat.coord.y + boat.size > 10:
                inGrid = False

        return inGrid


    # Add the boat's tiles to the list
    def occupedTile(self, Tile : list, boat : Boat):
        if boat.dir: # Vertical
            for i in range(boat.size):
                Tile.append(Coordinates.Coordinates(boat.coord.x + i, boat.coord.y))

        else: # Horizontal
            for i in range(boat.size):
                Tile.append(Coordinates.Coordinates(boat.coord.x, boat.coord.y + i))


    # Place the boats automatically
    def placeBoatBot(self, TabBoat : list):
        i = 0
        occupedTile = []

        # Select boat in the TabBoat list (descending order of size)
        for boat in TabBoat:
            boat.dir = randint(0, 1) # H / V
            
            boat.coord.x = randint(0, 9)
            boat.coord.y = randint(0, 9)
            
            # While the boat can't be placed, we try another position
            while((not self.boat_in_grid(boat)) or not boat.placeable(occupedTile)):
                boat.dir = randint(0, 1)

                boat.coord.x = randint(0, 9)
                boat.coord.y = randint(0, 9)

                i += 1

                if i > 1000: # If we try too many times, we stop
                    print_color("ERREUR : Impossible de placer le bateau", Data.colorRed)
                    break
            
            # Add the boat's tile to the list
            self.occupedTile(occupedTile, boat)

        return occupedTile


    # Check if a boat is sunk
    def checkBoat(self, boat : Boat):
        if boat.state == 0: # If the boat is still not sunk
            allTouched = True

            if boat.dir: # Vertical
                for i in range(boat.size):
                    if self.grid[boat.coord.x + i][boat.coord.y] == Data.Init: # If one of the boat's cases is not yet touched, the boat is not sunk
                        allTouched = False
                        break

                # Update the grid if sunk
                if allTouched:
                    boat.state = 1 # Sunk
                    for i in range(boat.size):
                        self.grid[boat.coord.x + i][boat.coord.y] = Data.Sunk
                        

            else: # Horizontal
                for i in range(boat.size):
                    if self.grid[boat.coord.x][boat.coord.y + i] == Data.Init: # If one of the boat's cases is not yet touched, the boat is not sunk
                        allTouched = False
                        break

                # Update the grid if sunk
                if allTouched:
                    boat.state = 1 # Sunk
                    for i in range(boat.size):
                        self.grid[boat.coord.x][boat.coord.y + i] = Data.Sunk


    # Check all the boats
    def checkAllBoat(self):
        for boat in self.TabBoat:
            self.checkBoat(boat)


    # Update the grid with the coord played
    def updateGrid(self, coord : Coordinates):
        if coord.in_list(self.TabCoord):
            self.grid[coord.x][coord.y] = Data.Touch # If there is a boat, we hit it
        else:
            self.grid[coord.x][coord.y] = Data.Miss # If there is no boat, we miss it


    # Check if the coord is in the grid
    def co_in_grid(self, coord : Coordinates):
        inGrid = True

        if (coord.x < 0 or coord.x > 9) or (coord.y < 0 or coord.y > 9):
            inGrid = False

        return inGrid


    # Check if the tile is already touched
    def already_touched(self, coord : Coordinates):
        return self.grid[coord.x][coord.y] != Data.Init


    # Print the result of the shoot
    def printShoot(self, co : Coordinates):
        if(self.grid[co.x][co.y] == Data.Miss): # If we miss
            print_color(" - A l'eau - ", Data.colorBlue)
        
        elif(self.grid[co.x][co.y] == Data.Touch): # If we touch a boat
            print_color(" - Touché - ", Data.colorGreen)

        elif(self.grid[co.x][co.y] == Data.Sunk): # If we sunk a boat
            print_color(" - Coulé - ", Data.colorRed)

        print()


    def askCoord(self):
        # Ask the player to enter a coord
        coord = input("\nCoordonnées (ex: A1) : ")
        coord = coord.upper() # Upper case
        coord = coord.strip() # Remove spaces

        # Split the string into alphabetic and numeric parts
        coord = ["".join(filter(str.isalpha, coord)), "".join(filter(str.isdigit, coord))]
 
        # Convert the coord
        co = Coordinates.Coordinates(ord(coord[0]) - 65, int(coord[1]) - 1)

        # Check if the coord is valid
        while (not self.co_in_grid(co)) or self.already_touched(co):
            coord = input("Coordonnées (ex: A1) : ")
            coord = coord.upper()
            coord = coord.strip()

            coord = ["".join(filter(str.isalpha, coord)), "".join(filter(str.isdigit, coord))]
            co = Coordinates.Coordinates(ord(coord[0]) - 65, int(coord[1]) - 1)

        return co


    # Make the player play
    def play(self):
        co = self.askCoord()

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
            self.showGrid(True)
            self.play()
            nb += 1

        self.outro(nb)





