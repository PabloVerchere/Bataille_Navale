class Coordinates:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y


    # + operator overload
    def __add__(self, other):
        return Coordinates(self.x + other.x, self.y + other.y)
    
    # = operator overload
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # overload for coord in coord list
    def in_list(self, list):
        for co in list:
            if co.x == self.x and co.y == self.y:
                return True
        return False
    

    def copy(self):
        return Coordinates(self.x, self.y)
    
    # DEBUG, show the coord's attributs
    def print(self):
        print(self.x, self.y)


    def direction(self, other):
        # Up
        if self.x - 1 == other.x and self.y == other.y:
            return 0
        # Right
        elif self.x == other.x and self.y + 1 == other.y:
            return 1
        # Down
        elif self.x + 1 == other.x and self.y == other.y:
            return 2
        # Left
        elif self.x == other.x and self.y - 1 == other.y:
            return 3
