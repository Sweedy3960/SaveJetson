import cv2 as cv
import numpy as np

PARAMETERS = cv.aruco.DetectorParameters_create()
DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
calib_path="SaveALL/myFi/"
CAMERA_MATRIX = np.loadtxt(calib_path+'matrix09.11.txt', delimiter=',')
DIST_COEFFS  = np.loadtxt(calib_path+'disto09.11.txt', delimiter=',')
MARKER_EDGE =0.07

def gstreamer_pipeline(
    capture_width=3264,
    capture_height=2464,
    display_width=100,
    display_height=100,
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
img = cv.VideoCapture(gstreamer_pipeline(),cv.CAP_GSTREAMER)
while(True):
    ret,frame = img.read()
    
    gray= cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

    corners, ids, rejctedImgPoints = cv.aruco.detectMarkers(gray,DICTIONARY,parameters = PARAMETERS)
    frame = cv.aruco.drawDetectedMarkers(frame, corners,ids)
     
    
    try :

        vector=np.transpose(corners)
        for j in range(2):    
            for i in range(np.size(ids)):
    
                Dict_corners["c1.x"]=vector[0][0]
                Dict_corners["c1.y"]=vector[1][0]
                print(Dict_corners)
        
        #test
        print("corners 1d?")
        print(type(corners))
        print("nb tot ?")
        print(len(corners))
        if(np.size(ids)>0):
            for i in range(np.size(ids)):
                print(np.size(ids))
                rvecs, tvecs, = cv.aruco.estimatePoseSingleMarkers(corners,MARKER_EDGE, CAMERA_MATRIX, DIST_COEFFS)
                frame = cv.aruco.drawAxis(frame, CAMERA_MATRIX, DIST_COEFFS, rvecs, tvecs,0.02)   
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
