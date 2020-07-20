import os
import cv2

liste = os.listdir()

for i in liste:
    if i[-2:] != "py":
        img = cv2.imread(i)
        r = cv2.resize(img, (20, 20))
        cv2.imwrite(i, r)
