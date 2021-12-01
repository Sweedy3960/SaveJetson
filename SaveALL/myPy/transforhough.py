import cv2 as cv 
from matplotlib.pyplot import *
import numpy 
import math 

img1=cv.imread("/home/cpnv/Documents/SaveJetson/Resqa23.11.last.bmp") 
black,white,red=cv.split(img1)
figure(figsize=(8,6))
cv.imshow(white,cmap=cm.gray)