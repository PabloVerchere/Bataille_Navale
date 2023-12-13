from . import Player
from .fct import *

import turtle


class Game:
    def __init__(self):
        self.player = Player.Player() # Create a player

        # Turtle setup
        self.root = turtle.Screen() # Create a screen
        self.root.title("Bataille Navale") # Set the title
        self.root.setup(800, 800) # Set the size of the screen
        self.root.bgcolor(Data.bg_color) # Set the background color
        self.root.listen() # Listen to the keyboard
        self.root.tracer(0) # Don't update the screen automatically

        self.t = turtle.Turtle() # Create a turtle
        self.t.speed(0) # Set the turtle's speed to the max
        self.t.hideturtle() # Hide the turtle
        self.t.penup()


    # Player against a random boat grid with turtle
    def play(self, debug = False):
        clearScreen(self.t)
        self.player.intro(self.t) # Show the intro

        self.root.onkeypress(lambda: self.gamingLoop(debug), "Return") # If Enter is pressed, start the game
        self.root.mainloop() # Continue listening to events


    def gamingLoop(self, debug = False):
        self.root.onkeypress(None, "Return") # Disable the keypress event

        clearScreen(self.t)
        self.player.showGrid(self.t, debug) # Show the grid

        nb = [0] # Number of turns
        # nb is a list so it will be passed by reference

        self.root.onscreenclick(lambda x, y: self.player.play(x, y, self.root, self.t, nb,  debug)) # If the screen is clicked, play
        self.root.mainloop() # Continue listening to events