
""" -------------------- PATH ENVIRONEMENT ----------------------"""
#Path of the current file
import os
path = os.path.dirname(os.path.abspath(__file__))

#Avatar path
pathAvatar = path + "/game/pictures/avatar"

#Environement path
pathEnvironement = path + "/game/pictures/environement"




""" -------------------- WINDOW CONSTANTES ----------------------"""
CONSTANTE_TITLE = "dkQLearning"



""" -------------------- PICTURE CONSTANTES ----------------------"""

CONTANTE_ICONE   = pathAvatar + "/avatar"
CONTANTE_SORTIE  = pathAvatar + "/sortie"
CONTANTE_MECHANT = pathAvatar + "/méchant"
CONTANTE_COFFRE  = pathAvatar + "/coffre"
CONTANTE_SEARCH  = pathAvatar + "/search"
CONTANTE_WALL    = pathAvatar + "/wall"
CONSTANTE_BONUS  = pathAvatar + "/bonus"
CONSTANTE_SHOT   = pathAvatar + "/shot"


CONSTANTE_BACKGROUND = pathEnvironement + "/fond.jpg"
CONSTANTE_SAVEGARDE  = pathEnvironement + "/sauvegarde.png"

""" ----------------------- MAP CONSTANTES ----------------------"""

CONSTANTE_SPRITE = 30
CONSTANTE_SIZE_SPRITE = 20
CONSTANTE_WINDOW = CONSTANTE_SPRITE * CONSTANTE_SIZE_SPRITE


CONTANTE_MAP_CREATE = pathEnvironement + "/map.txt"


LISTOBJECTCOLOR = [
    (24, 202, 255), (243, 168, 0), (69, 209, 14), (88, 156, 255),
    (0, 242, 255), (200, 174, 255), (14, 255, 196)]









