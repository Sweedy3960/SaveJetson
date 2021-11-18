import cv2 as cv 
import numpy as np 

while True :
    map = cv.imread("/home/cpnv/Images/Trymap.png")
    img = cv.imread("/home/cpnv/Images/left_0.jpg")
    rows = map.shape[0]
    cols = map.shape[1]
    channels = map.shape[2]
    for i in range(rows):
        for j  in range(cols):
            corr=img[i,j]
        print(corr)
    
    k = img[]
   
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    cv.imshow("gray",gray)
    imthresh31=gray
    cv.threshold(gray,128,255,cv.THRESH_BINARY,imthresh31)
    im3=cv.filter2D(imthresh31,-1,np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]),borderType=cv.BORDER_DEFAULT)
    #im3_1=cv.filter2D(imthresh31,-1,np.array([[1,-3],[1,1]]),borderType=cv.BORDER_CONSTANT)
    #im3_last = im3+im3_1
    cv.imshow("trhesh31",imthresh31)
    cv.imshow("flitered",im3)
    #cv.imshow("flitered2",im3_1)
    #cv.imshow("filteredlast",im3_last)
    cv.imshow("origin",img)
    cv.imwrite("ResFilt.jpg",im3)
    cv.imwrite("ResTresh.jpg",imthresh31)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break