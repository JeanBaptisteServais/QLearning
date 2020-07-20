""" -------------------------- IMPORATIONS ------------------------"""
import pygame
from pygame.locals import *

import os
import sys
sys.path.append("..")
from constantes import *

import cv2
import pathlib

import random
import time


""" -------------------------- GENERATE WINDOW GAME ------------------------"""

class Game:

    """Class for gameplay"""

    def __init__(self):

        #Window and background of pygame env
        self.window = None
        self.background = None

        #Dico: coordinate of malus and bonus items.
        self.rewardB = {}
        self.rewardM = {}

        #List: coordinate of wall.
        self.mapWall = []

        #List: Gitem list (recuperate reverse movement
        #from qlearning + second better action)
        self.GItem   = []


        #Picture movements (méchant, coffre exit and wall).
        self.dicoPath = {
            "méchantB": CONTANTE_MECHANT + "/mechant.png",
            "coffreB" : CONTANTE_COFFRE  + "/coffre.jpg",
            "méchantM": CONTANTE_MECHANT + "/mechantM.png",
            "coffreM" : CONTANTE_COFFRE  + "/coffreM.jpg",
            "sortieM" : CONTANTE_SORTIE  + "/sortieP.png",
            "sortieP" : CONTANTE_SORTIE  + "/sortieP.png",
            "wall"    : CONTANTE_WALL    + "/wall.png",
            "bonus"   : CONSTANTE_BONUS  + "/bonus.jpg"
        }

        #Picture load in pygame
        self.wall     = None
        self.arrivée  = None
        self.méchantB = None
        self.coffreB  = None
        self.méchantM = None
        self.coffreM  = None
        self.sortieM  = None
        self.bonus    = None

        #File of the labyrinth (.txt) stock into a list
        file = open(CONTANTE_MAP_CREATE, "r")
        self.fileLaby = [ligne for ligne in file]



    """------------------------ GETTER --------------------------"""
    def getterWindow(self):
        """Recuperate the window generate from pygame"""
        return self.window

    def getterWallCoord(self):
        """Recuperate coordinates of wall for deplacement controls"""
        return self.mapWall

    def getterReward(self):
        """Recuperate coordinates of rewards for qlearning"""
        return self.rewardB, self.rewardM

    def getterGItem(self):
        """Recuperate coordinates of gItems for qlearning (avoid to be stuck)"""
        return self.GItem




    """------------------------ INIT PYGAME ENV --------------------------"""
    def initialisationWindow(self):
        """render of the window"""

        #Init pygame.
        pygame.init()

        #Init window.
        self.window = pygame.display.set_mode((CONSTANTE_WINDOW, CONSTANTE_WINDOW))

        #Init icone.
        icone = pygame.image.load(CONTANTE_ICONE + "/dk_droite.png")

        #Display icone.
        pygame.display.set_icon(icone)

        #Init title.
        pygame.display.set_caption(CONSTANTE_TITLE)


    def initialisationBackground(self):
        """Initialise background and modify the background picture
        in function of the size of the env."""

        #Cv2 for resize the background picture in function of the window size.
        img = cv2.imread(CONSTANTE_BACKGROUND)

        #Verify picture is found.
        try:
            h,w = img.shape[:-1]
        except AttributeError:
            print("verify constante no found background picture")

        #If picture isn't conform to window size, resize it
        if h != CONSTANTE_WINDOW and w != CONSTANTE_WINDOW:
            imgResize = cv2.resize(img, (CONSTANTE_WINDOW, CONSTANTE_WINDOW))
            cv2.imwrite(CONSTANTE_BACKGROUND, imgResize)

        #Load the background into pygame.
        self.background = pygame.image.load(CONSTANTE_BACKGROUND).convert()


    def displayingWindow(self):
        """Display and for refresh the window"""

        #Verify if window and background are intialized
        if self.window is None or self.background is None:
            print("no window")
            exit(1)

        self.window.blit(self.background, (0,0))




    """----------------------- INIT ITEMS IN ENV --------------------------"""

    def loadingPictures(self):
        """Loading all picture need into pygame"""

        self.wall     = pygame.image.load(self.dicoPath["wall"]).convert()
        self.arrivée  = pygame.image.load(self.dicoPath["sortieP"]).convert()
        self.méchantB = pygame.image.load(self.dicoPath["méchantB"]).convert()
        self.coffreB  = pygame.image.load(self.dicoPath["coffreB"]).convert()
        self.méchantM = pygame.image.load(self.dicoPath["méchantM"]).convert()
        self.coffreM  = pygame.image.load(self.dicoPath["coffreM"]).convert()
        self.sortieM  = pygame.image.load(self.dicoPath["sortieM"]).convert()
        self.bonus    = pygame.image.load(self.dicoPath["bonus"]).convert()



    def generatingMapFirst(self, window):
        """Put wall of the labyrinth (1) and recompense (R)"""

        for nbLine, ligne in enumerate(self.fileLaby):
            for NoCase, sprite in enumerate(ligne):

                x = NoCase * CONSTANTE_SIZE_SPRITE
                y = nbLine * CONSTANTE_SIZE_SPRITE

                toBlit = None

                if sprite != 0:

                    if sprite == "1":
                        toBlit = self.wall
                        self.mapWall.append((x, y))

                    elif sprite == "R":
                        toBlit = self.coffreB
                        self.rewardB[(x, y)] = 100

                    elif sprite == "C":
                        toBlit = self.coffreM
                        self.rewardM[(x, y)] = -100

                    elif sprite == "S":
                        toBlit = self.sortieM
                        self.rewardM[(x, y)] = -100

                    elif sprite == "G":
                        toBlit = self.méchantB
                        self.rewardB[(x, y)] = 1000
                        self.GItem.append((x, y))

                    elif sprite == "B":
                        toBlit = self.bonus
                        self.rewardB[(x, y)] = 300
                        self.GItem.append((x, y))

                    elif sprite == "M":
                        toBlit = self.méchantM
                        self.rewardM[(x, y)] = -100

                    elif sprite == "A":
                        toBlit = self.arrivée
                        self.rewardB[(x, y)] = 10000

                    if toBlit != None: 
                        if toBlit != None: window.blit(toBlit, (x, y))


    def generatingMap(self, window):
        """Put wall of the labyrinth (1) and recompense (R)"""

        for nbLine, ligne in enumerate(self.fileLaby):
            for NoCase, sprite in enumerate(ligne):

                x = NoCase * CONSTANTE_SIZE_SPRITE
                y = nbLine * CONSTANTE_SIZE_SPRITE

                toBlit = None

                if sprite != 0:

                    if sprite == "1"  : toBlit = self.wall
                    elif sprite == "R": toBlit = self.coffreB
                    elif sprite == "C": toBlit = self.coffreM
                    elif sprite == "S": toBlit = self.sortieM
                    elif sprite == "G": toBlit = self.méchantB
                    elif sprite == "M": toBlit = self.méchantM
                    elif sprite == "A": toBlit = self.arrivée
                    elif sprite == "B": toBlit = self.bonus

                    if toBlit != None: window.blit(toBlit, (x, y))



    def reverseMovement(self, coordinate):
        """If dk in an impasse find a G item, make appear an other item who's
        make him return back"""

        if coordinate in self.GItem:
            return True, 4#nb of reverse deplacements to do

        return False, 1







        





""" ----------------------------- QUIT COMMAND GAME --------------------------"""

class CommandGame:

    """Command of the game"""

    def __init__(self):
        pass

    def quitCommand(self, event):
        """Command for quit the game"""

        #Press escape, quit game
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            return False
        return True






""" -------------------------- MOVEMENT OF AVATAR GAME ------------------------"""

class PersoGame():
    """Initialize character on the background"""

    def __init__(self, mapWallCoord, rewardB, rewardM):
        """Initialize avatar pictures"""

        #Pictures.
        self.rightAvatar = None
        self.leftAvatar  = None
        self.topAvatar   = None
        self.botAvatar   = None


        #Movements.
        self.x = 1 * CONSTANTE_SIZE_SPRITE
        self.y = 1 * CONSTANTE_SIZE_SPRITE


        #Recuperate the movement of the avatar
        self.deplacement = "droite"

        #Coord wall
        self.mapWallCoord = mapWallCoord

        #Items localisation
        self.rewardB = rewardB
        self.rewardM = rewardM

        #Make movements
        self.dicoMove = {"droite": (1, 0), "gauche": (-1, 0), "haut": (0, -1), "bas":(0, 1)}


        self.sauvegardeLastCoordinate = 0

        self.rayon1 = None
        self.rayon2 = None
        self.rayon3 = None



    """----------------------- PART ENVIRONEMENT DETECTION --------------------------"""

    def controlWall(self):
        """Verify in wall List if dk is in a wall coordinate"""

        #Make variable who's imitate deplacement variables
        xVerif = self.x + self.dicoMove[self.deplacement][0] * CONSTANTE_SIZE_SPRITE
        yVerif = self.y + self.dicoMove[self.deplacement][1] * CONSTANTE_SIZE_SPRITE

        for (coordX, coordY) in self.mapWallCoord:
            if xVerif == coordX and yVerif == coordY:
                return True

        return False


    def recuperateRewards(self):
        """Verify in rewards List if dk is in a reward coordinate"""

        coord = (self.x, self.y)

        if coord in self.rewardB:
            return self.rewardB[coord]

        elif coord in self.rewardM:
            return self.rewardM[coord]

        return None



    """----------------------- PART MOVEMENTS --------------------------"""

    def restartPosition(self):
        """Reinit position to begin"""

        self.x = 1 * CONSTANTE_SIZE_SPRITE
        self.y = 1 * CONSTANTE_SIZE_SPRITE



    def controlAutomatic(self):
        """Let move dk and not if wall or border of the map
        controle by random the avatar"""

        self.deplacement = random.choice(["droite", "gauche", "haut", "bas"])

        #Verify isn't border of the map
        isWall = PersoGame.controlWall(self)

        #if isn't border make increment of variables of deplacement.
        if isWall is False:
            self.x += self.dicoMove[self.deplacement][0] * CONSTANTE_SIZE_SPRITE
            self.y += self.dicoMove[self.deplacement][1] * CONSTANTE_SIZE_SPRITE



    def controlManuel(self, move):
        """From qlearning choose the better movement"""

        deplacement = ["droite", "gauche", "haut", "bas"]

        self.deplacement = deplacement[move]

        #Verify isn't border of the map
        isWall = PersoGame.controlWall(self)

        #if isn't border make increment of variables of deplacement.
        if isWall is False:
            self.x += self.dicoMove[self.deplacement][0] * CONSTANTE_SIZE_SPRITE
            self.y += self.dicoMove[self.deplacement][1] * CONSTANTE_SIZE_SPRITE



    def getterCoordinates(self):
        """return current coordinates"""
        return (self.x, self.y)


    def getterLastMove(self):
        """Return the last deplacement of dk"""
        return self.deplacement






    """----------------------- PART DISPLAYING --------------------------"""

    def incrementInfoPerso(self):
        """Fill info of our avatar, position deaparture and picture movements"""

        #Associate picture to avatar
        self.rightAvatar, self.leftAvatar, self.topAvatar, self.botAvatar =\
        [CONTANTE_ICONE + "/dk_droite.png", CONTANTE_ICONE + "/dk_gauche.png",
         CONTANTE_ICONE + "/dk_haut.png", CONTANTE_ICONE + "/dk_bas.png"]


    def displayAvatar(self, window):
        """display the avater on the window"""

        #Recuperate pictures of avatar.
        picturesAvatar = {"droite":self.rightAvatar, "gauche":self.leftAvatar,
                          "haut":self.topAvatar, "bas":self.botAvatar}

        #Display them.
        persoLoad = pygame.image.load(picturesAvatar[self.deplacement])
        window.blit(persoLoad.convert(), (self.x, self.y))




    """----------------------- PART DETECTION SHOT --------------------------"""


    def rayon(self):

        self.rayon1  = (self.x + 2 * CONSTANTE_SIZE_SPRITE, self.y)
        self.rayon3  = (self.x + 1 * CONSTANTE_SIZE_SPRITE, self.y)
        self.rayon2  = (self.x, self.y - 1 * CONSTANTE_SIZE_SPRITE)



    def detectionShot(self, coordinateShot):

        xShot, yShot = coordinateShot

        rayon1X, rayon1Y = self.rayon1
        rayon2X, rayon2Y = self.rayon2

        if self.rayon1 == coordinateShot or self.rayon3 == coordinateShot:
            right = 1
            top = 0
            return right, top

        if self.rayon2 == coordinateShot:
            right = 0
            top = 1
            return right, top

        
        return None, None


    def movementExpress(self, moveBottom, dontMove):


        expressNo = False
        expressY = False

        if moveBottom > 0.5:

            #Make variable who's imitate deplacement variables
            yVerif = self.y + 1 * CONSTANTE_SIZE_SPRITE

            no = False
            for (coordX, coordY) in self.mapWallCoord:
                if self.x == coordX and yVerif == coordY and no == False:
                    no = True
                    break

            if no is False:
                self.y += 1 * CONSTANTE_SIZE_SPRITE

            expressY = True
 
        if dontMove > 0.5:
            expressNo = True



    def reinitRayon(self):
        self.rayon1 = None
        self.rayon2 = None
        self.rayon3 = None




class shotEnemy:


    def __init__(self):

        self.picture = None

        self.coordinates = 0

        self.x = 0
        self.y = 0

        #File of the labyrinth (.txt) stock into a list
        file = open(CONTANTE_MAP_CREATE, "r")
        self.fileLaby = [ligne for ligne in file]


    def getterCoordinates(self, exploration):
        if exploration <= 0.2:
            return self.x, self.y
        return 0, 0

    def loadPicture(self):
        shotPicture = CONSTANTE_SHOT + "/shot.png"
        self.picture = pygame.image.load(shotPicture).convert()



    def recuperateShotCoord(self):

        self.coordinates = [
            (NoCase * CONSTANTE_SIZE_SPRITE, nbLine * CONSTANTE_SIZE_SPRITE)
            for nbLine, ligne in enumerate(self.fileLaby)
            for NoCase, sprite in enumerate(ligne)
            if sprite == "C"
        ][0]



    def setterOrigineCoordinates(self):
        self.x = self.coordinates[0]
        self.y = self.coordinates[1]


    def movements(self, iteration, exploration):
        if iteration % 10 == 0 and exploration <= 0.2:
            self.x -= 1 * CONSTANTE_SIZE_SPRITE


    def blintingShot(self, window):
        window.blit(self.picture, (self.x, self.y))


    def reinitializeMovement(self):

        coordinatesEnd = (200, 140)
        if (self.x, self.y) <= coordinatesEnd:
            return True
        return False
        












