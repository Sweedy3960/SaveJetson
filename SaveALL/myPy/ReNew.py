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
    #Glob
    DEBUG = False
    PARAMETERS = cv.aruco.DetectorParameters_create()
    DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
    MARKER_EDGE = 0.07
    MARKER_MIDL = 0.10
    MIDL=42
    MARKER_SAMPLE=0.05
    calib_path="SaveALL/myFi/"
    CAMERA_MATRIX = np.loadtxt(calib_path+'intrinsic30.11.txt', delimiter=',')  
    DIST_COEFFS  = np.loadtxt(calib_path+'calib30.11.txt', delimiter=',')
    def __init__(self):
        self.capture1 = []
        self.capture1.append(Capture())
        self.img = ImProc(self.capture1)
        self.run=True
    def Update(self) -> None:
        self.img.Update()
            #------Pour quitter "q"---------
        if cv.waitKey(1) & 0xFF == ord('q'):
            self.img.Release_All()
            self.running = False
    def main(self):
        while self.run:
            self.Update()
        self.img.Release_All()
        cv.destroyAllWindows()

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
        self.found=[]
        self.tagin={}
        self.Debug=False
        for i in cap:
            self.frame.append(None)
            self.cap.append(cv.VideoCapture(i.gstreamer_pipeline(),cv.CAP_GSTREAMER))
            self.infoMarkers.append(None)  
            self.ListId.append(None)
            self.gray.append(None)
            self.gauss.append(None)
            self.found.append(None)

    def ReadFrames(self):
        for i,j in enumerate(self.cap):
            ret,self.frame[j]=i.read()
           # for i in self.cap:
           #     for j in self.frame:
           #         j=i.read()
            
    def ToGray(self):
        for i,j in enumerate(self.frame):
            self.gray[j]=cv.cvtColor(self.frame[i], cv.COLOR_BGR2GRAY)
            

    def Gauss(self):
        for i , j in enumerate(self.gray)
            self.gauss[j]=cv.GaussianBlur(i,(31,31),100)
      
    
    def Trhesh(self):
        for i,j in enumerate(self.gauss):
            cv.threshold(i,250,255,cv.THRESH_BINARY_INV|cv.THRESH_OTSU, self.thresh[j])

    
    
    def NetFil(self):
        for i, j in enumerate(self.thresh):
            self.netFil[j]=cv.filter2D(i,-1,np.array([[1,1,1],[1,-8,1],[1,1,1]]),borderType=cv.BORDER_DEFAULT)

    def Detect(self):
        for i,j in enumerate(self.thresh):
            self.infoMarkers[j]=cv.aruco.detectMarkers(i, App.DICTIONARY, parameters = App.PARAMETERS)
        for i in self.infoMarkers:
            for j in i[1]:
                k=str(j)
                i[1][j]=k[1:-1]
            self.found[i]=len(i[1])    
    def TriTag(self):
        for i in self.infoMarkers:
            for j in i[1]:
                self.tagin["tag{}".format(j)] = Tag(i,int(j))
        return self.tagin



    def Release_All(self):
        for i in self.cap:
            i.release()
    def FrameWorking(self):
        self.ToGray()
        self.Gauss()
        self.Trhesh()
        self.NetFil()
    def Update(self):
        self.ReadFrames()
        self.FrameWorking()
        self.Detect()
        #save Dictio {ID}:infomarker(propre à la caméra qui a détécté le tag)
        save=self.TriTag()

         

class Tag:
    def __init__(self,infoMarkers:list,whoami:int):
        
        if whoami == App.MIDL:
            self.pos=(1450,1200)
            self.marker_cenrte=0.1
        
        self.Id=infoMarkers[1][whoami]
        self.tvecs=None
        self.rvecs=None
        self.corn=infoMarkers[0]
        

    def GetVect(self):
        
        self.rvecs, self.tvecs, markerPoints= cv.aruco.estimatePoseSingleMarkers(self.corn,App.MARKER_EDGE, App.CAMERA_MATRIX, App.DIST_COEFFS)
