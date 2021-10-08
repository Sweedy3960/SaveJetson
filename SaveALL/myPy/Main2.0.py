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
        self.corners=[]
        self.ids=[]
        self.rejctedImgPoints=[]
        
        self.ret=[]
        self.img = cv.VideoCapture(capture1.gstreamer_pipeline(), cv.CAP_GSTREAMER)
        self.a = []
    def imgprocess(self) :
        self.ret,self.frame = self.img.read()
        self.gray = cv.cvtColor(self.frame,cv.COLOR_BGR2GRAY)

        self.a = cv.aruco.detectMarkers(self.gray,DICTIONARY,parameters = PARAMETERS)
        self.frame = cv.aruco.drawDetectedMarkers(self.frame, self.a[0],self.a[1])
        cv.imshow("that",self.frame)

    
    def getcorns(self):
        return(self.corners)
    def getids(self):
        return(self.ids)
    def getframe(self):
        return(self.frame)

if __name__ == "__main__":
    
    capture1=capture()
    img=imgProcess()
    Dict_markers = {}
    while True:
        img.imgprocess()
        print(img.a)
        #------Pour quitter "q"---------
        if cv.waitKey(1) & 0xFF == ord('q'):
            img.img.release()
            break
cv.destroyAllWindows()
    