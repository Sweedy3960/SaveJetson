import cv2 as cv
import numpy as np
#--------------------------------------------------------------
PARAMETERS = cv.aruco.DetectorParameters_create()
DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
MARKER_EDGE =0.07
calib_path=""
CAMERA_MATRIX = np.loadtxt(calib_path+'cameraMatrix.txt', delimiter=',')
DIST_COEFFS  = np.loadtxt(calib_path+'cameraDistortion.txt', delimiter=',')
#---------------------------------------------------------------

#modification d'un pipeline trouvé sur le net pour test de capture 
class capture :
    def __init__(self) :
        self.capture_width=1680,
        self.capture_height=1050,
        self.display_width=500,
        self.display_height=500,
        self.framerate=5,
        self.flip_method=2,
    def setCap(self):
        self.capture_width=int(input("Largeur en pixels SVP :"))
        self.capture_height=int(input("hauteur en pixels SVP :"))
    def gstreamer_pipeline(self):
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
                self.capture_width,
                self.capture_height,
                self.framerate,
                self.flip_method,
                self.display_width,
                self.display_height,
            )
        )


class imgProcess :
    def __init__(self):
        self.corners=[]
        self.ids=[]
        self.rejctedImgPoints=[]
        self.frame
        self.ret=[]
        self.img = cv.VideoCapture(capture1.gstreamer_pipeline(), cv.CAP_GSTREAMER)

    def imgprocess(self) :
        self.ret,self.frame = self.img.read()
        self.corners, self.ids, self.rejctedImgPoints = cv.aruco.detectMarkers(self.frame,DICTIONARY,parameters = PARAMETERS)
    def draw(self):
        self.frame = cv.aruco.drawDetectedMarkers(self.frame, self.corners,self.ids)
        cv.imshow("that",self.frame)
    def swap(self):
        self.gray = cv.cvtColor(self.frame,cv.COLOR_BGR2GRAY)
    def getcorns(self,i):
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
        img.imgprocess(img)
        for i in img.getcorns(img):
            Dict_markers.append({("marker_"+str([i])) : img.getcorns(img,i)})
            #DEBUG
            img.draw(img)
        print(Dict_markers)
        #------Pour quitter "q"---------
        if cv.waitKey(1) & 0xFF == ord('q'):
         break

cv.destroyAllWindows()
    