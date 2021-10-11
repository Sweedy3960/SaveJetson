import cv2 as cv
import numpy as np
#--------------------------------------------------------------
PARAMETERS = cv.aruco.DetectorParameters_create()
DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
MARKER_EDGE =0.07
calib_path="SaveALL/myFi/"
CAMERA_MATRIX = np.loadtxt(calib_path+'cameraMatrix.txt', delimiter=',')
DIST_COEFFS  = np.loadtxt(calib_path+'cameraDistortion.txt', delimiter=',')
#---------------------------------------------------------------
#GST_ARGUS: Available Sensor modes :
#GST_ARGUS: 3264 x 2464 FR = 21.000000 fps Duration = 47619048 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
#GST_ARGUS: 3264 x 1848 FR = 28.000001 fps Duration = 35714284 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
#GST_ARGUS: 1920 x 1080 FR = 29.999999 fps Duration = 33333334 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
#GST_ARGUS: 1640 x 1232 FR = 29.999999 fps Duration = 33333334 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
#GST_ARGUS: 1280 x 720 FR = 59.999999 fps Duration = 16666667 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
#GST_ARGUS: 1280 x 720 FR = 120.000005 fps Duration = 8333333 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
#modification d'un pipeline trouvé sur le net pour test de capture 
class capture :
    def __init__(self):
        self.idCam=0
        self.capture_width=3264
        self.capture_height=1848
        self.display_width=500
        self.display_height=500
        self.flip_method=2
       
    def gstreamer_pipeline(self):
        return (
            "nvarguscamerasrc sensor_id=%d ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)10/1 !"
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                self.idCam,
                self.capture_width,
                self.capture_height,
                self.flip_method,
                self.display_width,
                self.display_height,
            )
        )


class imgProcess :
    def __init__(self):
        #[1]=image(numpy.ndarray)
        self.frame0=np.ndarray
        self.frame1=np.ndarray
        self.frame=[]
        #img = type videocapture
        self.cap0 = cv.VideoCapture(capture0.gstreamer_pipeline(), cv.CAP_GSTREAMER)
        self.cap0.isOpened()
        self.cap1 = cv.VideoCapture(capture1.gstreamer_pipeline(), cv.CAP_GSTREAMER)
        self.cap1.isOpened()
        self.stitcher = cv.Stitcher.create(mode= 0)
        
        
    def imgwork(self) : 
        self.ret,self.frame0 = self.cap0.read()
        self.ret,self.frame1 = self.cap1.read()
        #BGR to gray enleve les couleurs
        self.frame.append(cv.cvtColor(self.frame0,cv.COLOR_BGR2GRAY))
        self.frame.append(cv.cvtColor(self.frame1,cv.COLOR_BGR2GRAY))
        status,self.result = self.stitcher.stitch([self.frame0,self.frame1])
        if status != cv.Stitcher_OK:
            print("ben non staus= %d" % status)
        
    
       


if __name__ == "__main__":
    
    capture0=capture()
    capture1=capture()
    capture0.idCam=0
    capture1.idCam=1
    img=imgProcess()
    while True:
        
        img.imgwork()
        cv.imshow("tada", img.result)
        #------Pour quitter "q"---------
        if cv.waitKey(1) & 0xFF == ord('q'):
            img.cap0.release()
            img.cap1.release()
            break
cv.destroyAllWindows()
    