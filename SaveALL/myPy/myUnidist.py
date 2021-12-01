import numpy as np 
import cv2 as cv
from numpy.matrixlib.defmatrix import matrix

calib_path="/home/cpnv/Documents/SaveJetson/SaveALL/myFi/"
mtx= np.loadtxt(calib_path+'intrinsic30.11.txt', delimiter=',')
dist= np.loadtxt(calib_path+'calib30.11.txt', delimiter=',')
img = cv.imread("/home/cpnv/Documents/imgResult/map2nd.bmp")
h,w=img.shape[:2]
newcameramatrix,roi = cv.getOptimalNewCameraMatrix(mtx,dist,(h,w),cv.INTER_NEAREST,(w,h))
dst = cv.undistort(img,mtx,dist,None,newcameramatrix)
x,y,w,h =roi
dst=dst[y:y+h,x:x+w]
mapx,mapy = cv.initUndistortRectifyMap(mtx,dist,None,newcameramatrix,(w,h),5)
dst2=cv.remap(img,mapx,mapy,cv.INTER_LINEAR)
dst2=dst2[y:y+h,x:x+w]
cv.imwrite("t1.bmp",dst)
cv.imwrite("t2.bmp",dst2)