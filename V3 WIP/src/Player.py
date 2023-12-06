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

        # Select boat in the TabBoat list (descending order of size)
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
            
            # Add the boat's tile to the list
            self.occupedTile(occupedTile, boat)

        return occupedTile
    

    # Place the boats manually
    def placeBoatHuman(self, TabBoat : list):
        occupedTile = []
        print("Placez vos bateaux : \n")

        for boat in TabBoat:
            self.showGrid(True, occupedTile) # Show the grid with the boats already placed

            print("Placez votre", boat.name, "(", boat.size, "cases)") # Show the boat's name and size

            boat.dir = valid_dir() # Ask the direction

            boat.coord = self.askCoord()
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


    def playBotSmart(self, heatmap : list):
        touch = is_in_grid(Data.Touch, self.grid) # Check if there is at least one touch in the heatmap
        
        if touch == Coordinates.Coordinates(-1, -1): # If there is no touch in the heatmap
            print("no touch") # DEBUG
            # Shoot the coord with the max value in the heatmap
            co = maxCoGrid(heatmap)

        else: # If there is at least touch in the heatmap
            print("touch") # DEBUG

            co = self.bestTileArroundTouch(heatmap, touch) # Shoot the coord arround a random touch, where the value is the max

            i = 0
            while co == Coordinates.Coordinates(-1, -1) and i < 100: # If there is no tile available arround the touch, we choose another
                touch = is_in_grid(Data.Touch, self.grid)
                co = self.bestTileArroundTouch(heatmap, touch)
                i += 1
            
            if i >= 100: # Too many tries, we play randomly
                co = maxCoGrid(heatmap)

        # play the coord
        heatmap = self.playCo(co, heatmap)

        # Update the heatmap for the next turn
        heatmap = self.updateHeatmap(heatmap, co)

        return heatmap


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


    # Check if the boat is sunk
    def checkBoat(self, boat : Boat):
        if boat.state == 0: # If the boat is still not sunk

            if boat.dir: # Vertical
                for i in range(boat.size):
                    if self.grid[boat.coord.x + i][boat.coord.y] == Data.Init: # If one of the boat's tile is not yet touched, the boat is not sunk
                        return False

                # Update the grid if sunk
                boat.state = 1 # Sunk
                for i in range(boat.size):
                    self.grid[boat.coord.x + i][boat.coord.y] = Data.Sunk
                return True
                        

            else: # Horizontal
                for i in range(boat.size):
                    if self.grid[boat.coord.x][boat.coord.y + i] == Data.Init: # If one of the boat's tile is not yet touched, the boat is not sunk
                        return False

                # Update the grid if sunk
                boat.state = 1 # Sunk
                for i in range(boat.size):
                    self.grid[boat.coord.x][boat.coord.y + i] = Data.Sunk
                return True


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


    def playCo(self, co : Coordinates, heatmap):
        # Update the grids
        self.updateGrid(co)
        # Check if a boat is sunk
        sunk = self.checkAllBoat()
        # Print the shoot
        self.printShoot(co)

        if sunk: # if we sunk a boat, we reinit the heatmap
            heatmap = self.initHeatmap()
        
        return heatmap


    def initHeatmap(self):
        heatmap = [[0] * 10 for i in range(10)]
        tmp = Boat.Boat("", 0)

        # For each boat not sunk, we check all the possible positions and we add 1 to the heatmap
        for boat in self.TabBoat:
            if boat.state == 0: # not sunk
                tmp.copy(boat) # Copy the boat only to get the size and test all the possible coord

                for i in range(10):
                    for j in range(10):
                        tmp.coord = Coordinates.Coordinates(i, j) # Test the coord

                        tmp.dir = 1 # Vertical
                        if self.boat_in_grid(tmp) and not self.boat_already_touched(tmp): # If the boat is in the grid and not on a played tile
                            for k in range(tmp.size):
                                heatmap[tmp.coord.x + k][tmp.coord.y] += 1 # Add 1 to the heatmap for each tile of the boat

                        tmp.dir = 0 # Horizontal
                        if self.boat_in_grid(tmp) and not self.boat_already_touched(tmp): # If the boat is in the grid and not on a played tile
                            for k in range(tmp.size):
                                heatmap[tmp.coord.x][tmp.coord.y + k] += 1 # Add 1 to the heatmap for each tile of the boat

        return heatmap


    # Update the heatmap depending on the last shoot
    def updateHeatmap(self, heatmap : list, lastCo : Coordinates):
        # Shooted tile
        heatmap[lastCo.x][lastCo.y] = 0

        tmp = Boat.Boat("", 0)

        # Update arround the shooted tile (cross)
        for boat in self.TabBoat:
            if boat.state == 0: # For all the boat not sunk, we decrease the value of the tiles arround the shooted tile
                tmp.copy(boat)

                # Vertical
                tmp.dir = 1
                for i in range(-boat.size + 1, 1):
                    tmp.coord = Coordinates.Coordinates(lastCo.x + i, lastCo.y)

                    if self.boat_in_grid(tmp) and not self.boat_already_touched_except_co(tmp, lastCo):
                        for k in range(tmp.size):
                            if tmp.coord.x + k != lastCo.x or tmp.coord.y != lastCo.y:
                                heatmap[tmp.coord.x + k][tmp.coord.y] -= 1
                    
                # Horizontal
                tmp.dir = 0
                for i in range(-boat.size + 1, 1):
                    tmp.coord = Coordinates.Coordinates(lastCo.x, lastCo.y + i)

                    if self.boat_in_grid(tmp) and not self.boat_already_touched_except_co(tmp, lastCo):
                        for k in range(tmp.size):
                            if tmp.coord.x != lastCo.x or tmp.coord.y + k != lastCo.y:
                                heatmap[tmp.coord.x][tmp.coord.y + k] -= 1
        
        return heatmap


    # Check if the boat's tile are diff to Init
    def boat_already_touched(self, boat : Boat):
        if boat.dir: # Vertical
            for i in range(boat.size):
                if self.already_touched(Coordinates.Coordinates(boat.coord.x + i, boat.coord.y)):
                    return True
        
        else: # Horizontal
            for i in range(boat.size):
                if self.already_touched(Coordinates.Coordinates(boat.coord.x, boat.coord.y + i)):
                    return True
                
        return False


    # Check if the boat's tile are equal to Init but not co
    def boat_already_touched_except_co(self, boat : Boat, co : Coordinates):
        if boat.dir: # Vertical
            for i in range(boat.size):
                if self.already_touched(Coordinates.Coordinates(boat.coord.x + i, boat.coord.y)) and not Coordinates.Coordinates(boat.coord.x + i, boat.coord.y) == co:
                    return True
        
        else: # Horizontal
            for i in range(boat.size):
                if self.already_touched(Coordinates.Coordinates(boat.coord.x, boat.coord.y + i)) and not Coordinates.Coordinates(boat.coord.x, boat.coord.y + i) == co:
                    return True
                
        return False


    # Find the best tile to arround the touched tile
    def bestTileArroundTouch(self, heatmap : list, lastCo : Coordinates):
        # Heatmap value and coord of the 4 tiles arround the touched tile
        coord4 = {}

        # If the coord is in the grid and not already touch, we add it to the dict
        if self.co_in_grid(Coordinates.Coordinates(lastCo.x + 1, lastCo.y)) and not self.already_touched(Coordinates.Coordinates(lastCo.x + 1, lastCo.y)):
            coord4[heatmap[lastCo.x + 1][lastCo.y]] = Coordinates.Coordinates(lastCo.x + 1, lastCo.y)
        
        if self.co_in_grid(Coordinates.Coordinates(lastCo.x, lastCo.y + 1)) and not self.already_touched(Coordinates.Coordinates(lastCo.x, lastCo.y + 1)):
            coord4[heatmap[lastCo.x][lastCo.y + 1]] = Coordinates.Coordinates(lastCo.x, lastCo.y + 1)

        if self.co_in_grid(Coordinates.Coordinates(lastCo.x - 1, lastCo.y)) and not self.already_touched(Coordinates.Coordinates(lastCo.x - 1, lastCo.y)):
            coord4[heatmap[lastCo.x - 1][lastCo.y]] = Coordinates.Coordinates(lastCo.x - 1, lastCo.y)
        
        if self.co_in_grid(Coordinates.Coordinates(lastCo.x, lastCo.y - 1)) and not self.already_touched(Coordinates.Coordinates(lastCo.x, lastCo.y - 1)):
            coord4[heatmap[lastCo.x][lastCo.y - 1]] = Coordinates.Coordinates(lastCo.x, lastCo.y - 1)

        if coord4 == {}: # If there is no coord in the dict, we play randomly
            return Coordinates.Coordinates(-1, -1)
        else:
            return coord4[max(coord4)] # Return the coord with the max value in the dict