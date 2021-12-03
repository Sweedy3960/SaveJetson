import numpy as np 
import cv2 as cv

class Capture :
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
class App:
    DEBUG = False
    PARAMETERS = cv.aruco.DetectorParameters_create()
    DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
    MARKER_EDGE = 0.07
    calib_path="SaveALL/myFi/"
    CAMERA_MATRIX = np.loadtxt(calib_path+'intrinsic30.11.txt', delimiter=',')  
    DIST_COEFFS  = np.loadtxt(calib_path+'calib30.11.txt', delimiter=',')
    def __init__(self):
        self.capture1 = []
        self.capture1.append(Capture())
        self.img = ImProc(self.capture1)

class ImProc:

    def __init__(self,cap: list):
        self.frame = []
        self.gray = []
        self.gauss=[]
        self.infoMarkers = []
        self.cap=[]
        self.trhesh=[]
        self.netFil=[]
        self.ListId=[]
        self.Debug=False
        for i in cap:
            self.frame.append(None)
            self.cap.append(cv.VideoCapture(i.gstreamer_pipeline(),cv.CAP_GSTREAMER))
            self.infoMarkers.append(None)  
            self.ListId.append(None)
        for i in self.cap:
            self.gray.append(None)
            self.gauss.append(None)

    def ReadFrames(self):
        for i,j in enumerate(self.cap):
            ret,self.frame[j]=i.read()
           # for i in self.cap:
           #     for j in self.frame:
           #         j=i.read()
            
    def ToGray(self):
        for i,j in enumerate(self.frame):
            self.gray[j]=(cv.cvtColor(self.frame[i], cv.COLOR_BGR2GRAY))
            # for i in self.frame:
            #     for j in self.gray:
            #         j=(cv.cvtColor(i, cv.COLOR_BGR2GRAY))
            

    def Gauss(self):
        for i in self.gray:
            for j in self.gauss:
                j=cv.GaussianBlur(i,(31,31),100)
    
    def Trhesh(self):
        for i in self.gauss:
            for j in self.thresh:
                cv.threshold(i,250,255,cv.THRESH_BINARY_INV|cv.THRESH_OTSU,j)
    
    def NetFil(self):
        for i in self.thresh:
            for j in self.netFil:
                J=cv.filter2D(i,-1,np.array([[1,1,1],[1,-8,1],[1,1,1]]),borderType=cv.BORDER_DEFAULT)

    def Detect(self):
        for i in self.thresh:
            for j in self.infoMarkers:
                j=cv.aruco.detectMarkers(i, App.DICTIONARY, parameters = App.PARAMETERS)
                self.ListId[i].append(j[1])
    def IdWork(self):
        for i in self.ListId:
            for j in i:
                j=str(j)
                j=j.replace("[","")
                j=j.replace("]","")
    def Release_All(self):
        for i in self.cap:
            i.release()

class Tag:
    def __init__(self,infoMarkers:list,ListId:list):
        self.pos=(0,0)
        self.tvecs=None
        self.rvecs=None
        self.corn=None
        self.Id=None

        for i in infoMarkers:
            for j in i[0]:
                self.tvecs,self.rvecs=cv.aruco.estimatePoseSingleMarkers(j, App.MARKER_EDGE, App.CAMERA_MATRIX, App.DIST_COEFFS)
    
        for i in infoMarkers:
            for j in i[0]:
                self.Id=i[1][j]
