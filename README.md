# Bataille_Navale
## But du jeu
Le jeu consiste, pour un joueur, à couler tous les bateaux de l’autre joueur. Plus précisément, en début de partie, tous les navires sont placés dans une grille secrète. Les deux joueurs doivent alors chacun à leur tour, essayer de trouver et couler les bateaux de l’autre 
joueur. Pour cela, ils communiquent des coordonnées, exprimées sous la forme d’un couple (lettre, nombre). Un des deux joueurs annonce une case (par exemple « A5 »), et l’autre lui répond si le tir tombe à l'eau ou au contraire s'il touche un bateau. Dans ce dernier cas, 
il annonce « touché » s'il reste des cases intactes au bateau ciblé, et « coulé » sinon. Puis les rôles sont inversés et ainsi de suite jusqu’à la victoire de l’un des joueurs. Le vainqueur est celui qui réussit à couler tous les navires de l’autre joueur avant que les 
siens ne le soient.

> Les bateaux ne peuvent être placés que verticalement ou horizontalement.
> Il est possible de placer deux bateaux côte à côte.


## Execution
 - Pour lancer l'execution d'une version X, ouvrir puis executer le fichier main dans le fichier de la version correspondante  : ```./VX/main.py```

### Mode Debug
Dans chaque version, un mode **debug** est present et permet d'afficher les bateaux. Pour l'activer, dans ```./VX/main.py``` modifier ```game.play()``` en ```game.play(1)```

### Version Graphique
Pour la **Version 4**, la bibliothèque ***Turtle*** est requise.
Pour l'instaler sous windows, exécuter dans un invite de commande :
```bash
pip install PythonTurtle
