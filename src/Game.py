from random import randint # border included

from . import Boat

class Game():
    def __init__(self):
        self.gridHide = [[0] * 10 for i in range(10)] # Secret grid with boats placement
        self.gridPlay = [["."] * 10 for i in range(10)] # Grid to show to the player

        self.TabBoat = self.initTabBoat() # List of the boats
        self.placeBoatBot(self.TabBoat) # Place the boats randomly


    def initTabBoat(self): # Self not needed...
        TabBoat = []

        TabBoat.append(Boat.Boat("porte-avions", 5))
        TabBoat.append(Boat.Boat("croiseur", 4))
        TabBoat.append(Boat.Boat("contre-torpilleur", 3))
        TabBoat.append(Boat.Boat("sous-marin", 3))
        TabBoat.append(Boat.Boat("torpilleur", 2))

        return TabBoat


    # Show the grid to the player
    def showGrid(self, showHide = False):
        # Xlab
        print(" " * 3, end = "")
        for i in range(10):
            print(i, " ", end = "")
        print()

        # Grid + Ylab
        for i in range(10):
            print(chr(65 + i), " ", end = "") # A to J
            
            for j in range(10):
                if showHide:
                    # If there is a boat print in yellow
                    if self.gridHide[i][j] == 1:
                        print("\033[33m", end = "")
                        print(self.gridHide[i][j], " ", end = "")
                        print("\033[0m", end = "")
                    else:
                        print(self.gridHide[i][j], " ", end = "")
                else:
                    # If there is a boat, print in yellow
                    if self.gridPlay[i][j] == 1:
                        print("\033[33m", end = "")
                        print(self.gridPlay[i][j], " ", end = "")
                        print("\033[0m", end = "")
                    else:
                        print(self.gridPlay[i][j], " ", end = "")
            print()
    



    # Check if the boat is in the grid
    def is_in_grid(self, boat : Boat):
        inGrid = True

        if boat.dir: # Vertical
            if boat.coord.x + boat.size > 10:
                inGrid = False

        else:
            if boat.coord.y + boat.size > 10:
                inGrid = False

        return inGrid


    # Bool return of if we can place the boat
    def is_occuped(self, boat : Boat):
        occ = False
        
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


    # Place the boats automatically the boats
    def placeBoatBot(self, TabBoat : list):
        i = 0
        # Select boat in descending order of size
        for boat in TabBoat:
            boat.dir = randint(0, 1) # H / V
            
            boat.coord.x = randint(0, 9)
            boat.coord.y = randint(0, 9)
            
            while(not self.is_in_grid(boat) or self.is_occuped(boat)): # While the boat can't be placed, we try another position
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
    def checkBoat(self, boat : Boat):
        if boat.state == 0: # If the boat is not sunk
            if boat.dir: # Vertical
                for i in range(boat.size):
                    if self.gridHide[boat.coord.x + i][boat.coord.y] != 3: # If all the boat's cases are touched, the boat is sunk
                        boat.state = 1
                        break
                # Update the grid
                for i in range(boat.size):
                    self.gridHide[boat.coord.x + i][boat.coord.y] = 4
                        

            else: # Horizontal
                for i in range(boat.size):
                    if self.gridHide[boat.coord.x][boat.coord.y + i] != 3: # If all the boat's cases are touched, the boat is sunk
                        boat.state = 1
                        break
                # Update the grid
                for i in range(boat.size):
                    self.gridHide[boat.coord.x][boat.coord.y + i] = 4