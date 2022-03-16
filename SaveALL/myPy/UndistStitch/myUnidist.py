import numpy as np 
import cv2 as cv
import vpi

imgSize=(3264,2464)
calib_path="/home/cpnv/Documents/SaveJetson/SaveALL/myFi/"
camMatrix= np.loadtxt(calib_path+'intrinsic30.11.txt', delimiter=',')
coeffs= np.loadtxt(calib_path+'calib30.11.txt', delimiter=',')
# Create an uniform grid
grid = vpi.WarpGrid(imgSize)
 
#undist_map = vpi.WarpMap.fisheye_correction(grid,
  #                                          K=camMatrix[0:2,:], X=np.eye(3,4), coeffs=coeffs,
   #                                         mapping=vpi.FisheyeMapping.EQUIDISTANT)

img = cv.imread("/home/cpnv/Documents/imgResult/map2nd.bmp")
h,w=img.shape[:2]
newcameramatrix,roi = cv.getOptimalNewCameraMatrix(camMatrix,coeffs,(h,w),cv.INTER_NEAREST,(w,h))
dst = cv.undistort(img,camMatrix,coeffs,None,newcameramatrix)
x,y,w,h =roi
dst=dst[y:y+h,x:x+w]
mapx,mapy = cv.initUndistortRectifyMap(camMatrix,coeffs,None,newcameramatrix,(w,h),5)
dst2=cv.remap(img,mapx,mapy,cv.INTER_NEAREST)
dst2=dst2[y:y+h,x:x+w]
#with vpi.Backend.CUDA:
    # Convert image to NV12_ER, apply the undistortion map and convert image back to RGB8
 #   imgCorrected = vpi.asimage(img).convert(vpi.Format.NV12_ER).remap(undist_map, interp=vpi.Interp.CATMULL_ROM).convert(vpi.Format.RGB8)
cv.imwrite("t1.bmp",dst)
cv.imwrite("t2.bmp",dst2)
#cv.imwrite("t3.bmp",imgCorrected)