from . import Coordinates


class Boat:
    def __init__(self, name : str, size : int):
        self.name = name

        self.state = 0 # 0 is OK, 1 is sunk
        self.size = size
        self.dir = 0 # 0 is Horizontal, 1 is Vertical

        self.coord = Coordinates.Coordinates() # Left Up Corner
        

    # DEBUG, show the boat's attributes
    def print(self):
        print(self.name)
        
        print("State: ", end = "")
        if self.state:
            print("sunk")
        else:
            print("OK")
            
            
        print("Size:", self.size)
        
        print("Direction: ", end = "")
        if self.dir:
            print("Horizontal")
        else:
            print("Vertical")
            
        print("Original co:", self.coord.x, self.coord.y)
        print()