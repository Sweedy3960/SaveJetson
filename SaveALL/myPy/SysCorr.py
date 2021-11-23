import numpy as np 
import cv2 as cv 

map = cv.imread("/home/cpnv/Images/ResFilt01.bmp",0)
rows = map.shape[0]
cols = map.shape[1]
corr=np.array
cv.imshow("test",map)
for i in range(rows):
    for j  in range(cols):
        corr[i][j].append(None)      
print(corr)


