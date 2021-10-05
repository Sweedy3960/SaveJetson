import cv2 as cv
import numpy as np
#-----------------------------------------------------------------------------
PARAMETERS = cv.aruco.DetectorParameters_create()
DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
calib_path=""
CAMERA_MATRIX = np.loadtxt(calib_path+'cameraMatrix.txt', delimiter=',')
DIST_COEFFS  = np.loadtxt(calib_path+'cameraDistortion.txt', delimiter=',')
MARKER_EDGE =0.07
#-----------------------------------------------------------------------------
def gstreamer_pipeline(
    capture_width=1680,
    capture_height=1050,
    display_width=500,
    display_height=500,
    framerate=10,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )
#-----------------------------------------------------------------------------
Dict_markers = {}

img = cv.VideoCapture(gstreamer_pipeline(flip_method=0), cv.CAP_GSTREAMER)
while(True):
    ret,frame = img.read()
    gray= cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    corners, ids, rejctedImgPoints = cv.aruco.detectMarkers(frame,DICTIONARY,parameters = PARAMETERS)
    frame = cv.aruco.drawDetectedMarkers(frame, corners,ids)
    for i in corners:
        rvecs, tvecs, = cv.aruco.estimatePoseSingleMarkers(corners,MARKER_EDGE, CAMERA_MATRIX, DIST_COEFFS)
        Dict_markers.append(ids[i],[corners[i],rvecs,tvecs])
        #DEBUG
        #frame = cv.aruco.drawAxis(frame, CAMERA_MATRIX, DIST_COEFFS, rvecs, tvecs,0.02)
    #DEBUG
    #cv.imshow("that",frame)
    #DEBUG
    #print(Dict_markers)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
