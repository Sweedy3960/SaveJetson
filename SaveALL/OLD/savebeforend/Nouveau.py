import cv2 as cv
import numpy as np
import imutils as im


#Tentatide de undistorde une image (apartir d'une image) plus tard d'un flux video
PARAMETERS = cv.aruco.DetectorParameters_create()
DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)

img = cv.imread("disto.jpg")
img = im.resize(img,width=600)

while(True):    
    gray= cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    corners, ids, reject = cv.aruco.detectMarkers(gray,DICTIONARY,parameters = PARAMETERS)
    img = cv.aruco.drawDetectedMarkers(img, corners,ids)
    img = cv.undistort_image(img,)
    cv.imshow("that",img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    print(ids,corners)
cv.destroyAllWindows()


