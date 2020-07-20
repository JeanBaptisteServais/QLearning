import random
import numpy as np
import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsClassifier


class Trainning:

    def __init__(self):
        pass




    def simulateRayon(self):
        """We can have 2 detections of enemy shot right and top"""

        rayonPos = random.choice(["haut", "droite"])

        if rayonPos == "haut":
            rayonDroite = 0
            RayonHaut = 1

        elif rayonPos == "droite":
            rayonDroite = 1
            RayonHaut = 0


        return [rayonDroite, RayonHaut]



    def makeTarget(self, rayon):
        """If rayon is top we want no move target, if rayon
        right we want bottom move"""

        rayonDroite, RayonHaut = rayon

        if rayonDroite == 1:
            targetDroite = 1
            targetHaut   = 0

        elif RayonHaut == 1:
            targetDroite = 0
            targetHaut   = 1 

        return [targetDroite, targetHaut]


    def makeModel(self, X, Y):
        """Fit Knn model"""

        model = KNeighborsClassifier()

        model.fit(X, Y)
        scoring = model.score(X, Y)
        print(scoring)
 
        return model

    
    def moving(self, model, detectionRayon):
        """Make the prediction from the model"""

        rayonDroite, RayonHaut = detectionRayon
        x = np.array(rayonDroite).reshape(1, 1)

        prediction = model.predict(x)

        return prediction[0]
        








































