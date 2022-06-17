import cv2 as cv 
import numpy as np 
import time as t 

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

    def readimg(self) :
        self.ret,self.frame0 = self.cap0.read()

    def Togray(self):
        #BGR to gray enleve les couleurs
        self.gray = cv.cvtColor(self.frame0,cv.COLOR_BGR2GRAY)

    def Detectmarkers(self):
        self.infoMarkers0 = cv.aruco.detectMarkers(self.gray,DICTIONARY,parameters = PARAMETERS)
        #si markers detect  vecteur de translation et rotation 

    def Estimposmarkers(self):
        for  i in enumerate(self.infoMarkers0[0]):
       # for i in self.infoMarkers0[0]:
            self.rvecs, self.tvecs, markerPoints= cv.aruco.estimatePoseSingleMarkers(i,MARKER_EDGE, CAMERA_MATRIX, DIST_COEFFS)
            #DEBUG
            #print(img.rvecs)
    def Drawaxis(self):
        self.frame0 = cv.aruco.drawAxis(self.frame0, CAMERA_MATRIX, DIST_COEFFS, self.rvecs, self.tvecs,0.10)
    def stack(self):
        k = self.infoMarkers0[1][j]
           # for i in self.infoMarkers0[1]: 
            
        self.Dict_stack[str(k)]=(self.rvecs,self.tvecs)
                #self.Dict_stack[str(i)]=(self.rvecs,self.tvecs) 
                
        #self.frame = cv.aruco.drawDetectedMarkers(self.frame, self.infoMarkers[0],self.infoMarkers[1])
        cv.imshow("frame",self.frame0)
    #origin tag 7
    def calcul(self):
        self.a=list(self.Dict_stack.keys())

        self.c=self.Dict_stack[self.a[0]][1]-self.Dict_stack[self.a[1]][1]
        
        result=((self.c[0][0][0]**2+self.c[0][0][1]**2+self.c[0][0][2]**2)**0.5)*100
        print(type(result))
        print(result)
        
        

