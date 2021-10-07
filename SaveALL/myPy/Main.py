import cv2 as cv
import numpy as np
#-----------------------------------------------------------------------------
PARAMETERS = cv.aruco.DetectorParameters_create()
DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
calib_path="/home/cpnv/Desktop/pypro/SaveJetson/SaveALL/myFi/"
CAMERA_MATRIX = np.loadtxt(calib_path+'cameraMatrix.txt', delimiter=',')
DIST_COEFFS  = np.loadtxt(calib_path+'cameraDistortion.txt', delimiter=',')
MARKER_EDGE =0.07
#-----------------------------------------------------------------------------
def gstreamer_pipeline(
    capture_width=1680,
    capture_height=1050,
    display_width=500,
    display_height=500,
    framerate=5,
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
            framerate,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
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
    #gray= cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    corners,ids,rejctedImgPoints = cv.aruco.detectMarkers(frame,DICTIONARY,parameters = PARAMETERS)
    for i in corners:
        rvecs, tvecs, markerPoints= cv.aruco.estimatePoseSingleMarkers(corners[i],MARKER_EDGE, CAMERA_MATRIX, DIST_COEFFS)
        #DEBUG
        frame = cv.aruco.drawDetectedMarkers(frame, corners,ids)
        frame = cv.aruco.drawAxis(frame, CAMERA_MATRIX, DIST_COEFFS, rvecs, tvecs,0.02)
    #DEBUG
    cv.imshow("that",frame)
    #DEBUG
    #print(Dict_markers)
    print(Dict_markers)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
