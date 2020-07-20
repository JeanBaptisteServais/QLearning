
import random
import sys
sys.path.append("..")
from constantes import *



class QLearning:

    def __init__(self):


        self.QTableCoordinate = []
        self.QTable = []

        self.exploration = 1

        self.n = 1

        self.max = 0
        self.last = 0
        self.tookObject = []
        self.historicRoad = []
        self.finisher = 0



    def setterExploration(self, exploration):
        self.exploration  = exploration


    def getterExploration(self):
        return self.exploration


    def getterTables(self):
        return self.QTableCoordinate, self.QTable





    def searchInQtable(self, coordinate):
        """From coordinate recuperate the index qtable"""

        for index, coord in enumerate(self.QTableCoordinate):
            if coord == coordinate:
                return index



    def updateQFunction(self, coordinate0, coordinate1, reward, move, rewardCoordB):

        """Update qTable who's [0, 0, 0, 0]
        recuperate coordinate for the index in qtable,
        recuperate reward for replace the score,
        recuperate move for the index in the line of the qtable"""


        deplacement = {"droite":0, "gauche":1, "haut":2, "bas":3}
        if reward == None: reward = 0

        if coordinate1 in self.historicRoad and reward != 0:
            reward = 0

        if coordinate1 not in self.tookObject and coordinate1 in rewardCoordB:
            self.tookObject.append(coordinate1)
            

        #Search line of coordinates of the Qtable (0 - len(QTable))
        indexQtable0 = QLearning.searchInQtable(self, coordinate0)
        indexQtable1 = QLearning.searchInQtable(self, coordinate1)


        #Search the index of the line of qtable (0 - 3)
        movement = deplacement[move]
        maxScore = self.QTable[indexQtable1].index(max(self.QTable[indexQtable1]))


        #Recuperate score of the index (-10 - 10)
        QT    = self.QTable[indexQtable0][movement]
        QTOne = self.QTable[indexQtable1][maxScore]


        self.QTable[indexQtable0][movement] = QT + 0.1*(reward + ((0.9**self.n)*QTOne) - QT)


        if coordinate1 == self.finisher:
            return True


        if reward == 100 or reward == 2000 and coordinate1 not in self.historicRoad:
            self.n += 2
            self.historicRoad.append(coordinate1)

        return False




    def exploitationFromTable(self, coordinate, isReversed, currentIterationNbReverse, nbReversed):
        """From the coordinate, recuperate the Qtable line,
        return the best arg"""

        #In qtable recuperate scores
        indexQtable = QLearning.searchInQtable(self, coordinate)

        possibilities = self.QTable[indexQtable]


        highterValue  = possibilities.index(max(possibilities))



        if isReversed is True and currentIterationNbReverse != (nbReversed - 1):

            if highterValue == 0:
                highterValue = 1
            elif highterValue == 1:
                highterValue = 0
            elif highterValue == 2:
                highterValue = 3
            elif highterValue == 3:
                highterValue = 2

        elif isReversed is True and currentIterationNbReverse == (nbReversed - 1):
            num  = sorted(possibilities)
            num  = num[-2]
            highterValue = possibilities.index(num)


        return highterValue




    def epsilonGreedy(self):
        """definate if next move is exploration"""

        explo = random.uniform(0, 1)
        if explo <= self.exploration:
            return True




    def intiQtable(self):

        """Recuperate coordinates
        initialize qTable (right, left, top, bot move from the case"""


        with open(CONTANTE_MAP_CREATE, "r") as file:
            for nbLine, ligne in enumerate(file):
                for NoCase, sprite in enumerate(ligne):

                    if sprite not in ("1"):

                        x = NoCase * CONSTANTE_SIZE_SPRITE
                        y = nbLine * CONSTANTE_SIZE_SPRITE

                        self.QTable.append([0 for i in range(4)])
                        self.QTableCoordinate.append((x, y))
  
                        if sprite in ("A"):
                            self.finisher = (x, y)



