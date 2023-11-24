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
    
    # DEBUG, show the coord's attributs
    def print(self):
        print(self.x, self.y)