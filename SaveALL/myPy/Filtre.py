import cv2 as cv 
import numpy as np
cnt=0
corr=[]
while True :
    img = cv.imread("/home/cpnv/Documents/SaveJetson/map2nd2.bmp",1)
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    cv.imshow("gray",gray)
    #im2=cv.GaussianBlur(gray,(31,31),100)
    #cv.imshow("nette?",im2)
    imthresh31=gray
    cv.threshold(gray,250,255,cv.THRESH_BINARY_INV|cv.THRESH_OTSU,imthresh31)
    im3=cv.filter2D(imthresh31,-1,np.array([[1,1,1],[1,-8,1],[1,1,1]]),borderType=cv.BORDER_DEFAULT)
    im2=cv.GaussianBlur(im3,(9,9),100)
    im2=cv.filter2D(im2,-1,np.array([[0,0,0],[0,-4,0],[0,0,0]]),borderType=cv.BORDER_DEFAULT)
    cv.imshow("trhesh31",imthresh31)
    cv.imshow("flitered",im3)
    cv.imshow("gaussed",im2)
    cv.imwrite("Res23.11.last{}.bmp".format(cnt),imthresh31)
    cv.imwrite("Res23.11.last.bmp",im3)
    cv.imwrite("Res23.11.last.bmp",im2)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break