import cv2 as cv 
import numpy as np 
PARAMETERS = cv.aruco.DetectorParameters_create()
DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
img = cv.imread("/home/cpnv/Images/ResTresh.jpg")
#im3=cv.filter2D(img,-1,np.array([[0,-1,0],[-1,5,-1],[0,-1,0]]),borderType=cv.BORDER_DEFAULT)
#cv.imshow("plusnet?",im3)
#gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)  
#cv.threshold(gray,128,255,cv.THRESH_BINARY,gray)
#img=cv.filter2D(gray,-1,np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]),borderType=cv.BORDER_DEFAULT)
corners,ids,rejctedImgPoints = cv.aruco.detectMarkers(img,DICTIONARY,parameters = PARAMETERS)
img = cv.aruco.drawDetectedMarkers(img, corners,ids)
cornera = corners[0]
cornerb = corners[1]
xb=cornerb.item(0)
yb=cornerb.item(1)
x = cornera.item(0)
y = cornera.item(1)
while True:
    cv.imshow("that",img)
    print(y)
    print(x)
    print(yb)
    print(xb)
    print(ids)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break