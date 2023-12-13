from . import Boat
from . import Data


# Return a tab of boats with the Boats from Data.py
def initTabBoat():
    TabBoat = []

    for name, size in Data.Boats.items():
        TabBoat.append(Boat.Boat(name, size))

    return TabBoat

# Clear the screen with turtle
def clearScreen(t):
     t.clear()
        

def draw_grid(row, col, size, t):
    t.color(Data.grid_color)

    # Draw the grid
    for i in range(row + 1):
        t.penup()
        t.goto(-col * size / 2, -i * size + row * size / 2)
        t.pendown()
        t.forward(col * size)

    t.left(90)

    for j in range(col + 1):
        t.penup()
        t.goto(j * size - col * size / 2, -row * size / 2)
        t.pendown()
        t.forward(row * size)


    # Add the letters
    for i in range(row - 1):
        t.penup()
        t.goto(-col * size / 2 + size / 2, -i * size + row * size / 2 - 7/4 * size)
        t.pendown()
        t.write(chr(i + 65), align = "center", font=("Arial", 12, "bold"))
        
    # Add the numbers
    for j in range(col - 1):
        t.penup()
        t.goto(j * size - col * size / 2 + size * 3 / 2, -row * size / 2 + (col - 1) * size + size / 4)
        t.pendown()
        t.write(str(j + 1), align = "center", font=("Arial", 12, "bold"))
    
    t.right(90) # Reset the direction


# Return if the click is in the grid
def isMouseInGrid(x, y, row, col, size):
    return x >= -col * size / 2 and x <= col * size / 2 and y >= -row * size / 2 and y <= row * size / 2


# Return the tile of the click in the grid
def getTile(x, y, row, col, size):
    return (int)(((-y + row * size / 2) - (Data.tile_size / 2)) // size), (int)(((x + col * size / 2) - (Data.tile_size / 2)) // size)