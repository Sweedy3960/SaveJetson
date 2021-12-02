import cv2 as cv
import numpy as np
#--------------------------------------------------------------
PARAMETERS = cv.aruco.DetectorParameters_create()
DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
MARKER_EDGE =0.07
calib_path="SaveALL/myFi/"
CAMERA_MATRIX = np.loadtxt(calib_path+'intrinsic30.11.txt', delimiter=',')  
DIST_COEFFS  = np.loadtxt(calib_path+'calib30.11.txt', delimiter=',')
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
        self.capture_height=2464
        self.display_width=3264
        self.display_height=2464
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

    def setCap(self):
        self.capture_width=int(input("Largeur en pixels SVP :"))
        self.capture_height=int(input("hauteur en pixels SVP :"))

class imgProcess :
    def __init__(self):
        #frame list [0]=ret= booléen vrai si val retournée
        #[1]=image(numpy.ndarray)
        self.frame0=np.ndarray
        #img = type videocapture
        self.cap0 = cv.VideoCapture(capture0.gstreamer_pipeline(), cv.CAP_GSTREAMER)
        self.cap0.isOpened()
        #infomarker [0]=corners [1]=ids [2]=rejectedpoints
        self.infoMarkers0 = []
        self.Dict_stack = {}
        self.a=[]
        self.tveclist=[]
        self.Centre_Id = 42
        self.Centre_Tvec=0
    def imgwork(self) :
        self.ret,self.frame0 = self.cap0.read()
      
        #BGR to gray enleve les couleurs
        self.gray = cv.cvtColor(self.frame0,cv.COLOR_BGR2GRAY)
        self.infoMarkers0 = cv.aruco.detectMarkers(self.gray,DICTIONARY,parameters = PARAMETERS)
        #si markers detect  vecteur de translation et rotation 
        for j, i in enumerate(self.infoMarkers0[0]):
       # for i in self.infoMarkers0[0]:
            self.rvecs, self.tvecs, markerPoints= cv.aruco.estimatePoseSingleMarkers(i,MARKER_EDGE, CAMERA_MATRIX, DIST_COEFFS)
            #DEBUG
            #print(img.rvecs)
            self.frame0 = cv.aruco.drawAxis(self.frame0, CAMERA_MATRIX, DIST_COEFFS, self.rvecs, self.tvecs,0.10)
            
            k = self.infoMarkers0[1][j]
           # for i in self.infoMarkers0[1]: 
            k=str(k)
            k=k.replace("[","")
            k=k.replace("]","")
            self.Dict_stack[str(k)]=(self.rvecs,self.tvecs)
                #self.Dict_stack[str(i)]=(self.rvecs,self.tvecs) 
        self.a=list(self.Dict_stack.keys())
              
        #self.frame = cv.aruco.drawDetectedMarkers(self.frame, self.infoMarkers[0],self.infoMarkers[1])
        #cv.imshow("frame",self.frame0)
     
    def calcul(self):
        for j, i in enumerate(self.a):
            print(self.a)
            #distance (diagonale si plusieur plan entre deux tag)
            print(self.Dict_stack[str(int(i))][1])
            print(self.Dict_stack[str(self.Centre_Id)][1])
            self.c=self.Dict_stack[int(i)][1]-self.Dict_stack[str(self.Centre_Id)][1]
            result=((self.c[0][0][0]**2+self.c[0][0][1]**2+self.c[0][0][2]**2)**0.5)*100
            #récup de id 
            print(self.a[j][1])
            print("entre {} et {} est de {} cm".format(int(self.a[j]),int(self.a[j+1]),result))
         


if __name__ == "__main__":
    
    capture0=capture()
    capture0.idCam=0
    img=imgProcess()
    while True:
        #print("alive")
        img.imgwork()
        #print("alive")
        img.calcul()
        #------Pour quitter "q"---------
        if cv.waitKey(1) & 0xFF == ord('q'):
            img.cap0.release()
            break
cv.destroyAllWindows()
