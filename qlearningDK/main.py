""" -------------------------- IMPORATIONS ------------------------"""
import time
import cv2
from constantes import *
from game.game import *
from displayResum.displayResum import *
from QLearning.QLearning import *
from Knn.Knn import *





"""---------------------- INITIALIZE GAME ---------------------"""
#Create object from game class.
game = Game()

#initialize window.
game.initialisationWindow()
game.initialisationBackground()
game.loadingPictures()

#recuperate window.
window = game.getterWindow()

#Recuperate wall and rewards coords on the .txt file
mapWallCoord = game.getterWallCoord()
rewardCoordB, rewardCoordM = game.getterReward()






"""---------------------- INITIALIZE QLEARNING ---------------------"""
#Create object from qlearning class.
QLearning = QLearning()
#Init qTable with rewards and '0' coords from the .txt file
QLearning.intiQtable()






"""---------------------- INITIALIZE TRAINING KNN---------------------"""
Trainning = Trainning()

epochs = 2000

dataX = []#targets
dataY = []#features

for epoch in range(epochs):

    #Simulate rayon (right or top detection)
    rayons = Trainning.simulateRayon()

    #Make target wish
    targets = Trainning.makeTarget(rayons)

    dataX.append(targets[0])
    dataY.append(rayons)

#Train model
modelMove  = Trainning.makeModel(np.array(dataX).reshape(-1, 1), np.array(dataY))





"""---------------------- INITIALIZE PERSO ---------------------"""
#Initialisze character on the map.
gameCommand = CommandGame()

#Display and refresh the window.
game.displayingWindow()

#Initialize character on the map. Recuperate wall coord and rewards coords
dkPersonnage = PersoGame(mapWallCoord, rewardCoordB, rewardCoordM)
dkPersonnage.incrementInfoPerso()

#Blit personnage into the map.
dkPersonnage.displayAvatar(window)


#Put wall and objects
game.generatingMapFirst(window)

#Refresh window
pygame.display.flip()




"""---------------------- INITIALIZE SHOT ---------------------"""
#init shot picture object shot class

shotEnemy = shotEnemy()
shotEnemy.loadPicture()
shotEnemy.recuperateShotCoord()
shotEnemy.setterOrigineCoordinates()




"""-------------- DISPLAY PICTURE & RECUPERATE INFO PERSO ------------"""
#Savegarde window for the first displaying score and for detect colors objects.
pygame.image.save(window, CONSTANTE_SAVEGARDE)

#Displaying score objects.
displayResum  = displayResum(rewardCoordB, rewardCoordM)
#displayResum.recuperateDataAvatar()




"""---------------------- LUNCH GAME ---------------------"""


"""----------- LUNCH LOOP -----------"""
#Lunch the loop game.

initialisation = True
isReversed = False
nbReversed = 1
iteration  = 1
nbExploration = 5000

while initialisation:

    #restart position of dk
    dkPersonnage.restartPosition()
    #Re - recuperate all coords execpt walls
    QLearning.intiQtable()





    """----------- LUNCH LOOP GENERATION -----------"""
    generation = True
    while generation:
        



        for iterationnbReversed in range(nbReversed):



            """-----------QUIT, LOOP PYGAME -----------"""
            #pygame.time.Clock().tick(30)
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        continuer = 0




            """----------- LUNCH WINDOW DISPLAY -----------"""
            #Reput map.
            game.displayingWindow()
            game.generatingMap(window)





            """---------EXPLORATION or EXPLOITATION ---------"""
            """      (selection of the next movement)        """

            coordinate0 = dkPersonnage.getterCoordinates()#T
            exploration = QLearning.epsilonGreedy()


            currentExplo = QLearning.getterExploration()


            """--------- KNN ---------"""
            #Recuperate coord of enemy shot.
            shotCoord = shotEnemy.getterCoordinates(currentExplo)
            #ask right and top cood of location of dk.
            dkPersonnage.rayon()
            #Detection dk enemy shot with top right coord and enemy coord.
            detectionRayon = dkPersonnage.detectionShot(shotCoord)


            """--------- MOVE FROM MODEL ---------"""
            #Verify detection
            noMove = False
            immediateMove = False

            if detectionRayon[0] != None:
                toMove = Trainning.moving(modelMove, detectionRayon)

                if   toMove[0] == 1: immediateMove = True
                elif toMove[1] == 1: noMove = True

                dkPersonnage.movementExpress(toMove[0], toMove[1])

            else:
                dkPersonnage.reinitRayon()



            """--------- E GREEDY MOVE ---------"""
            if noMove == False and immediateMove == False:

                #exploration
                if exploration is True and isReversed is False:
                    dkPersonnage.controlAutomatic()

                #Exploitation
                else:
                    betterMove = QLearning.exploitationFromTable(
                        coordinate0, isReversed, iterationnbReversed, nbReversed)
                    dkPersonnage.controlManuel(betterMove)





                """--------- MOVE AND REWARDS --------"""
                #Dk
                move        = dkPersonnage.getterLastMove()#T
                coordinate1 = dkPersonnage.getterCoordinates()#T+1
                reward      = dkPersonnage.recuperateRewards()#T+1





                """--------- QLEARNING PHASE --------"""
                if isReversed is False:
                    restart = QLearning.updateQFunction(coordinate0, coordinate1, reward, move, rewardCoordB)
                    if restart == True:
                        generation = False




            """--------- DISPLAYING SHOT --------"""
            #Shot
            shotEnemy.movements(iteration, currentExplo)
            shotEnemy.blintingShot(window)
            endRoadShot = shotEnemy.reinitializeMovement()
            if endRoadShot is True:
                shotEnemy.setterOrigineCoordinates()




            """--------- DISPLAYING DK --------"""
            #Blit personnage into the map.
            dkPersonnage.displayAvatar(window)

            pygame.display.flip()
            iteration += 1




            """--------- DISPLAYING INFO --------"""
            QTableCoordinate, QTable = QLearning.getterTables()
            displayResum.displayRoad(QTableCoordinate, QTable)



            """----------- E GREEDY REGULATION -------------"""
            if iteration % nbExploration == 0:
                if nbExploration == 5000:
                    nbExploration = 2000
                currentExplo = QLearning.getterExploration()
                QLearning.setterExploration(currentExplo - 0.1)
                currentExplo = QLearning.getterExploration()
                print("exploration done -0.1 now: ", currentExplo)
                generation = False




        """--------- GITEM MOVEMENT (hardcode movement) --------"""
        isReversed, nbReversed = game.reverseMovement(coordinate1)




        











