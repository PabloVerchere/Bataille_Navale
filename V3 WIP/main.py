from src.Game import Game


game = Game() # Create a game


from src.fct import printGrid
#printGrid(game.playerList[1].initHeatmap())
#game.playerList[1].TabBoat[0].state = 1
#printGrid(game.playerList[1].initHeatmap())
game.play(1) # Play loop