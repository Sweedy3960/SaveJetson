import cv2 as cv
import numpy as np

PARAMETERS = cv.aruco.DetectorParameters_create()
DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
calib_path=""
CAMERA_MATRIX = np.loadtxt(calib_path+'cameraMatrix.txt', delimiter=',')
DIST_COEFFS  = np.loadtxt(calib_path+'cameraDistortion.txt', delimiter=',')
MARKER_EDGE =0.07
img = np.zeros((300,300,1),dtype="uint8")
img = cv.VideoCapture(0)
while(True):
    ret,frame = img.read()
    
    save=frame 
    gray= cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

    corners, ids, rejctedImgPoints = cv.aruco.detectMarkers(gray,DICTIONARY,parameters = PARAMETERS)
    
    frame = cv.aruco.drawDetectedMarkers(frame, corners,ids)
    try:
    
        rvecs, tvecs, = cv.aruco.estimatePoseSingleMarkers(corners,MARKER_EDGE, CAMERA_MATRIX, DIST_COEFFS)
        frame = cv.aruco.drawAxis(frame, CAMERA_MATRIX, DIST_COEFFS, rvecs, tvecs,0.02)
    except:
        pass
    
    try :
        if(ids.size() > 0):
            for i in range(ids.size()):
                print("la")
                print(ids.size())
               
                frame = cv.aruco.drawAxis(frame, CAMERA_MATRIX, DIST_COEFFS, rvecs[i], tvecs[i],0.02)
    except:
      pass
    cv.imshow("that",frame)
    print(str(corners))
    print("-----------------------------")
    print(type(ids))
    print(str(ids))
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
