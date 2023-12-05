from random import randint # border included

from . import Boat
from . import Coordinates
from . import Data
from .fct import *


class Player():
    def __init__(self, human = True):
        self.grid = [[Data.Init] * 10 for i in range(10)] # Grid to show to the player

        self.TabBoat = initTabBoat() # List of the boats

        if human:
            self.TabCoord = self.placeBoatHuman(self.TabBoat) # Ask the player to place the boats and return the list of the occuped tiles
        else:
            self.TabCoord = self.placeBoatBot(self.TabBoat) # Place the boats randomly and return the list of the occuped tiles


    # Place the boats automatically
    def placeBoatBot(self, TabBoat : list):
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
    

    # Place the boats manually
    def placeBoatHuman(self, TabBoat : list):
        occupedTile = []

        for boat in TabBoat:
            self.showGrid(True, occupedTile) # Show the grid with the boats already placed

            print("Placez votre", boat.name, "(", boat.size, "cases)") # Show the boat's name and size

            boat.dir = valid_dir() # Ask the direction

            boat.coord = self.askCoord() # Ask the coord
            print()

            # While the boat can't be placed, we ask another position
            while((not self.boat_in_grid(boat)) or not boat.placeable(occupedTile)):
                boat.dir = valid_dir()

                boat.coord = self.askCoord()
                print()


            # Add the boat's tile to the list
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


    # Make the bot play
    def playBot(self):
        co = Coordinates.Coordinates(randint(0, 9), randint(0, 9))

        while (self.already_touched(co)):
            co = Coordinates.Coordinates(randint(0, 9), randint(0, 9))

        # Update the grids
        self.updateGrid(co)
        # Check if a boat is sunk
        self.checkAllBoat()
        # Print the shoot
        self.printShoot(co)


    # Make the human play
    def playHuman(self):
        co = self.askCoord()

        # Update the grids
        self.updateGrid(co)
        # Check if a boat is sunk
        self.checkAllBoat()
        # Print the shoot
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


    # Check if the tile is already touched (touch, miss or sunk)
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


    # Check if a boat is sunk
    def checkBoat(self, boat : Boat):
        if boat.state == 0: # If the boat is still not sunk

            if boat.dir: # Vertical
                for i in range(boat.size):
                    if self.grid[boat.coord.x + i][boat.coord.y] == Data.Init: # If one of the boat's cases is not yet touched, the boat is not sunk
                        break

                # Update the grid if sunk
                if allTouched:
                    boat.state = 1 # Sunk
                    for i in range(boat.size):
                        self.grid[boat.coord.x + i][boat.coord.y] = Data.Sunk
                        

            else: # Horizontal
                for i in range(boat.size):
                    if self.grid[boat.coord.x][boat.coord.y + i] == Data.Init: # If one of the boat's cases is not yet touched, the boat is not sunk
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

        if(self.grid[co.x][co.y] == Data.Miss): # If we miss
            print_color(" - A l'eau - ", Data.colorBlue)
        
        elif(self.grid[co.x][co.y] == Data.Touch): # If we touch a boat
            print_color(" - Touché - ", Data.colorGreen)

        elif(self.grid[co.x][co.y] == Data.Sunk): # If we sunk a boat
            print_color(" - Coulé - ", Data.colorRed)

        print()


    # Show the grid to the player
    def showGrid(self, debug = False, CoordList = None): # If TabBoat is empty, use a List of Coordinates pass in parameter
        if CoordList == None:
            CoordList = self.TabCoord

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
                    if Coordinates.Coordinates(i, j).in_list(CoordList): 
                        if self.grid[i][j] == Data.Init: # If there is a undiscovered boat, print in Magenta
                            print_color(Data.Debug, Data.colorMagenta, False)
                        
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
- Deux bateaux ne peuvent ni se chevaucher, ni être collés l’un à l'autre.
              
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