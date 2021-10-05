import cv2 as cv
import numpy as np

PARAMETERS = cv.aruco.DetectorParameters_create()
DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
calib_path=""
CAMERA_MATRIX = np.loadtxt(calib_path+'cameraMatrix.txt', delimiter=',')
DIST_COEFFS  = np.loadtxt(calib_path+'cameraDistortion.txt', delimiter=',')
MARKER_EDGE =0.07

def gstreamer_pipeline(
    capture_width=5000,
    capture_height=5000,
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
Dict_corners = {"c1.x":0,"c1.y":0}
img = cv.VideoCapture(gstreamer_pipeline(flip_method=0), cv.CAP_GSTREAMER)
while(True):
    ret,frame = img.read()
    #gray= cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

    corners, ids, rejctedImgPoints = cv.aruco.detectMarkers(frame,DICTIONARY,parameters = PARAMETERS)
    frame = cv.aruco.drawDetectedMarkers(frame, corners,ids)
    try :

        vector=np.transpose(corners)
        for j in range(2):
            print("a")
            for i in range(np.size(ids)):
                print("b")
                Dict_corners["c1.x"]=vector[0][0]
                Dict_corners["c1.y"]=vector[1][0]
                print(Dict_corners)

        print("C1")
        print(c1)
        print("len c1")
        print(len(c1))
        print("c1 type")
        print(type(c1))
        print("-----------------")
        print(vector)
        print("len vector")
        print(len(vector))
        print("vector type")
        print(type(vector))

        #test
        print("corners 1d?")
        print(corners[0][0][0][0])
        print(corners[0][0][0][1])
        print(corners[0][0][1][0])
        print("type de corners")
        print(type(corners))
        print("nb tot ?")
        print(len(corners))
        if(np.size(ids)>0):
            for i in range(np.size(ids)):
                print("la")
                print(np.size(ids))
                rvecs, tvecs, = cv.aruco.estimatePoseSingleMarkers(corners,MARKER_EDGE, CAMERA_MATRIX, DIST_COEFFS)
                frame = cv.aruco.drawAxis(frame, CAMERA_MATRIX, DIST_COEFFS, rvecs, tvecs,0.02)
                print("rvecs 1d?")
                print(rvecs)
                print("type de rvecs")
                print(type(rvecs))
                print("nb tot ?")
                print(len(rvecs))
    except:
      pass
    cv.imshow("that",frame)
    print(str(corners))
    print("-----type de corner")
    print(type(corners))
    print(str(ids))
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
