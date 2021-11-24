import numpy as np 
import cv2 as cv 


map = cv.imread("/home/cpnv/Documents/SaveJetson/Resqa23.11.last.bmp",0)
rows = map.shape[0]
cols = map.shape[1]
corr= []
for i in range(rows):
    for j  in range(cols):
        corr.append(None)
map=np.asarray(corr)
map.shape=(3264,2464)



