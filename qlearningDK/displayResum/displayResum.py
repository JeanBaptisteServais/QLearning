import numpy as np
import cv2

import sys
sys.path.append("..")
from constantes import *


class displayResum:

    def __init__(self, dict1, dict2):


        self.resum = {}
        for (k, v) in dict1.items(): self.resum[k] = v
        for (k, v) in dict2.items(): self.resum[k] = v


        self.img = cv2.imread(CONSTANTE_SAVEGARDE)
        self.copyScore = self.img.copy()



    def recuperateDataAvatar(self):
        
        for coordinate, score in self.resum.items():

            font = cv2.FONT_HERSHEY_SIMPLEX 
            fontScale = 0.5
            color = (255, 0, 0) 
            thickness = 1
               
            # Using cv2.putText() method 
            image = cv2.putText(self.copyScore, str(score), coordinate, font,  
                               fontScale, color, thickness, cv2.LINE_AA) 

        cv2.imshow("image avatar", self.copyScore)  
        cv2.waitKey(0)



    def searchInQtable(self, coordinate, QTableCoordinate):
        """From coordinate recuperate the index qtable"""

        for index, coord in enumerate(QTableCoordinate):
            if coord == coordinate:
                return index


    def displayRoad(self, QTableCoordinate, QTable):

        copyRoad  = self.img.copy()

        font = cv2.FONT_HERSHEY_SIMPLEX 
        fontScale = 0.2
        color = (255, 255, 255) 
        thickness = 1
           

        for index, ((x, y), score) in enumerate(zip(QTableCoordinate, QTable)):

            if round(max(score), 3) > 0:

                # Using cv2.putText() method 
                image = cv2.putText(copyRoad, str(round(max(score), 1)), (x, y), font,  
                                   fontScale, color, thickness, cv2.LINE_AA) 

            elif round(min(score), 3) < 0:
                image = cv2.putText(copyRoad, str(round(min(score), 1)), (x, y), font,  
                                   fontScale, color, thickness, cv2.LINE_AA) 


        cv2.imshow("image score", copyRoad)  
        cv2.waitKey(1)











