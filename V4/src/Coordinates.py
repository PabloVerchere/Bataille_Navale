class Coordinates:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y


    # overload for coord in a coord list
    def in_list(self, list):
        for co in list:
            if co.x == self.x and co.y == self.y:
                return True
        return False
    

    # DEBUG, show the coord's attributs
    def print(self):
        print(self.x, self.y)