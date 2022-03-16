import cv2 as cv
import numpy as np
 
#-----------------------------------------------------------------------------
PARAMETERS = cv.aruco.DetectorParameters_create()
DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
calib_path="SaveALL/myFi/"
CAMERA_MATRIX = np.loadtxt(calib_path+'cameraMatrix.txt', delimiter=',')
DIST_COEFFS  = np.loadtxt(calib_path+'cameraDistortion.txt', delimiter=',')
MARKER_EDGE =0.20
#-----------------------------------------------------------------------------
def gstreamer_pipeline(
    capture_width=3264,
    capture_height=2464,
    display_width=1000,
    display_height=1000,
    flip_method=2,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)10/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            flip_method,
            display_width,
            display_height,
        )
    )
#-----------------------------------------------------------------------------
Dict_markers = {}

img = cv.VideoCapture(gstreamer_pipeline(),cv.CAP_GSTREAMER)

while(True):
    ret,frame = img.read()
    gray= cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    im3=gray
    cv.threshold(gray,250,255,cv.THRESH_BINARY|cv.THRESH_OTSU,im3)
    cv.imshow("tresh",im3)
    corners,ids,rejctedImgPoints = cv.aruco.detectMarkers(gray,DICTIONARY,parameters = PARAMETERS)
    
    #Debug
    frame = cv.aruco.drawDetectedMarkers(frame, corners,ids)
    for i in corners:
        rvecs, tvecs, markerPoints= cv.aruco.estimatePoseSingleMarkers(i,MARKER_EDGE, CAMERA_MATRIX, DIST_COEFFS)
        #DEBUG
        frame = cv.aruco.drawAxis(frame, CAMERA_MATRIX, DIST_COEFFS, rvecs, tvecs,0.10)
    cv.line(frame,(0,0),(511,511),(0,0,255),3)
    #DEBUG
    cv.imshow("that",frame)
    #DEBUG
    #print(Dict_markers)
    print(ids)
    print(corners)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
img.release()
cv.destroyAllWindows()



