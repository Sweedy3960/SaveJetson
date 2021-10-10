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
      self.capture_width=3264
      self.capture_height=1848
      self.display_width=500
      self.display_height=500
      self.flip_method=2
       
    def gstreamer_pipeline(self):
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
               self.capture_width,
               self.capture_height,
               self.flip_method,
               self.display_width,
               self.display_height,
            )
        )

    def setCap(self):
        self.capture_width=int(input("Largeur en pixels SVP :"))
        self.capture_height=int(input("hauteur en pixels SVP :"))

class imgProcess :
    def __init__(self):
        #frame list [0]=ret= booléen vrai si val retournée
        #[1]=image(numpy.ndarray)
        self.frame=[]
        #img = type videocapture
        self.img = cv.VideoCapture(capture1.gstreamer_pipeline(), cv.CAP_GSTREAMER)
        #infomarker [0]=corners [1]=ids [2]=rejectedpoints
        self.infoMarkers = []
    def imgwork(self) :
        self.frame = self.img.read()
        #BGR to gray enleve les couleurs
        self.gray = cv.cvtColor(self.frame[1],cv.COLOR_BGR2GRAY)
        self.infoMarkers = cv.aruco.detectMarkers(self.gray,DICTIONARY,parameters = PARAMETERS)
        #si markers detect  vecteur de translation et rotation 
        for i in self.infoMarkers[0]:
            self.rvecs, self.tvecs, markerPoints= cv.aruco.estimatePoseSingleMarkers(i,MARKER_EDGE, CAMERA_MATRIX, DIST_COEFFS)
            #DEBUG
            #print(img.rvecs)
            #self.frame = cv.aruco.drawAxis(self.frame, CAMERA_MATRIX, DIST_COEFFS, self.rvecs, self.tvecs,0.10)
        #debug
        #self.frame = cv.aruco.drawDetectedMarkers(self.frame, self.infoMarkers[0],self.infoMarkers[1])
        cv.imshow("that",self.frame[1])


if __name__ == "__main__":
    
    capture1=capture()
    img=imgProcess()
    while True:
        img.imgwork()
        #------Pour quitter "q"---------
        if cv.waitKey(1) & 0xFF == ord('q'):
            img.img.release()
            break
cv.destroyAllWindows()
    