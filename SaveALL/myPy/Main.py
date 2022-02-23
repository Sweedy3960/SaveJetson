import cv2 as cv
import numpy as np
#-----------------------------------------------------------------------------
PARAMETERS = cv.aruco.DetectorParameters_create()
PARAMETERS.polygonalApproxAccuracyRate = 0.03
PARAMETERS.minMarkerPerimeterRate = 0.02
DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
calib_path="SaveALL/myFi/"
CAMERA_MATRIX = np.loadtxt(calib_path+'cam12matvid.txt', delimiter=',')
DIST_COEFFS  = np.loadtxt(calib_path+'cam12distvid.txt', delimiter=',')
MARKER_EDGE =0.07
#-----------------------------------------------------------------------------
def gstreamer_pipeline(
    idCam=0,
    capture_width=3264,
    capture_height=1848,
    display_width=3264,
    display_height=1848,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor_id=%d ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)10/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            idCam,
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
    corners,ids,rejctedImgPoints = cv.aruco.detectMarkers(gray,DICTIONARY,parameters = PARAMETERS)
    #Debug
    #frame = cv.aruco.drawDetectedMarkers(frame, corners,ids)
    for i in corners:
        rvecs, tvecs, markerPoints= cv.aruco.estimatePoseSingleMarkers(i,MARKER_EDGE, CAMERA_MATRIX, DIST_COEFFS)
        #DEBUG
        frame = cv.aruco.drawAxis(frame, CAMERA_MATRIX, DIST_COEFFS, rvecs, tvecs,0.10)
    #DEBUG
    cv.imwrite("this23_02_2.png",frame)
    #DEBUG
    #print(Dict_markers)
    print(ids)  
    print(corners)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
img.release()
cv.destroyAllWindows()
