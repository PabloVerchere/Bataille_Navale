from src.Game import Game


""" V1
Ecrire un jeu de bataille navale où seul le joueur (humain) doit essayer de trouver et couler tous les
bateaux placés par l’ordinateur dans la grille secrète.
"""
# Enfin, il est impossible de placer deux bateaux côte à côte.
# A faire... 



game = Game()


game.V1()

"""
a faire
grillle secrete, grille des tir
placer les beateaux
saisir les tirs, afficher les tirs effectue
+ resultat du dernier
avertir le joueur quand il gange
"""


"""
Indication : os.system("clear") permet d’effacer l’écran.
"""

"""
Fonction placerBateaux(grille :list) , list
Cette fonction prend une grille dans laquelle les bateaux doivent être placés et les place dessus
de manière aléatoire. Une fois ces derniers placés, elle renvoie la grille actualisée (1 s’il y a un
bateau, 2 autour des bateaux par exemple).
Pour placer un bateau, il faut tenir compte de sa longueur, du sens dans lequel on veut le placer
et de l’endroit où on veut le mettre (ses coordonnées). Il est conseillé d’utiliser un dictionnaire
pour connaître la longueur de chaque type de bateau. Avoir une liste par type de bateau afin de
connaître ses coordonnées facilitera les traitements par la suite.
"""