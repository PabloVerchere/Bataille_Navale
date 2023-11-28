from . import Coordinates


class Boat:
    def __init__(self, name : str, size : int):
        self.name = name

        self.state = 0 # 0 is OK, 1 is sunk
        self.size = size
        self.dir = 0 # 0 is Horizontal, 1 is Vertical

        self.coord = Coordinates.Coordinates() # Left Up Corner


    # Return if the boat will not have any tile in common with the list
    def placeable(self, list : list):
        if self.dir: # Vertical
            for i in range(self.size):
                if Coordinates.Coordinates(self.coord.x + i, self.coord.y).in_list(list):
                    return False
                
        else: # Horizontal
            for i in range(self.size):
                if Coordinates.Coordinates(self.coord.x, self.coord.y + i).in_list(list):
                    return False
                
        return True


    def copy(self, other):
        self.name = other.name
        self.state = other.state
        self.size = other.size
        self.dir = other.dir
        self.coord = other.coord.copy()


    # DEBUG, show the boat's attributs
    def print(self):
        print(self.name)
        
        print("State: ", end = "")
        if self.state:
            print("Sunk")
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