# Hided Grid
HNothing = 0
HBoat = 1
HWater = 2
HTouch = 3
HSunk = 4

# Playable Grid
PInit = "."
PMiss = "*"
PTouch = "+"
PSunk = "X"

# Boat
Boats = {
    "Porte-avions":5,
    "Croiseur":4,
    "Contre-torpilleur":3,
    "Sous-marin":3,
    "Torpilleur":2
}

# WE WILL ONLY USE 1 GRID, visible and boat placement will be stored in there attributs, need to do a debut fct to display them with game.showGrid()