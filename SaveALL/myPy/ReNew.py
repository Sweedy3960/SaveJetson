import numpy as np 
import cv2 as cv
import sys
import time


class Vector2:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    def norme(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

class Vector3:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z
    def norme(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    def __str__(self) -> str:
        return f"Vector3({self.x}, {self.y}, {self.z})"


class Capture :
    def __init__(self):
        self.idCam=0
        self.capture_width=3840
        self.capture_height=2160
        self.display_width=3840
        self.display_height=2160
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
    PARAMETERS = cv.aruco.DetectorParameters_create()
    DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
    MARKER_EDGE = 0.07
    MARKER_MIDL = 0.10
    MIDL=42
    SAMPLES_T=[47,13,36,17]
    ROBOTS_T=[1,2,3,4,5,6,7,8,9,10]
    MARKER_SAMPLE=0.07
    calib_path="SaveALL/myFi/"
    CAMERA_MATRIX = np.loadtxt(calib_path+'cam12matvid.txt', delimiter=',')  
    DIST_COEFFS  = np.loadtxt(calib_path+'cam12distvid.txt', delimiter=',')
    def __init__(self):
        self.capture1 = []
        self.capture1.append(Capture())
        self.img = ImProc(self.capture1)
        self.run=True
   
    def main(self):
        while self.run:
            self.Update()
        self.img.Release_All()
        cv.destroyAllWindows()
    def Update(self) -> None:
        self.img.Update()
            #------Pour quitter "q"---------
        if cv.waitKey(1) & 0xFF == ord('q'):
            self.img.Release_All()
            self.running = False
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
        self.detected =False
        self.tagin={}
        self.pos=[0,0,0]
        self.Debug=False
        self.DebugD=False
        self.capVidD=False
        self.imgcnt=0
        for i in cap:
            self.frame.append(None)
            self.cap.append(cv.VideoCapture(i.gstreamer_pipeline(),cv.CAP_GSTREAMER))
            self.infoMarkers.append(None)  
            self.ListId.append([])
            self.gray.append(None)
            self.gauss.append(None)
            self.trhesh.append(None)
            self.found.append(None)
            self.netFil.append(None)
        self.out= cv.VideoWriter("out.avi",cv.VideoWriter_fourcc(*"MJPG"),10.0,(3840,2160))
    def ReadFrames(self):
        for i,j in enumerate(self.cap):
            ret,self.frame[i]=j.read()

           # for i in self.cap:
           #     for j in self.frame:
           #         j=i.read()
            if self.Debug:
                cv.imshow("fr{}".format(i), self.frame[i])
            
    def ToGray(self):
        for i,j in enumerate(self.frame):
            self.gray[i]=cv.cvtColor(j, cv.COLOR_BGR2GRAY)
        if self.Debug:
                cv.imshow("GR{}".format(i), self.gray[i])

       


    def Gauss(self):
        for i , j in enumerate(self.gray):
            self.gauss[i]=cv.GaussianBlur(j,(3,3),100)
        if self.Debug:
                cv.imshow("GS{}".format(i), self.gauss[i])
            
      
    
    def Trhesh(self):
        for i,j in enumerate(self.gray):
            self.trhesh[i]=self.gray[i]
            cv.threshold(j,250,255,cv.THRESH_BINARY_INV|cv.THRESH_OTSU, self.trhesh[i])
        if self.Debug:
            cv.imshow("th{}".format(i), self.trhesh[i])
    
    
    def NetFil(self):
        for i, j in enumerate(self.trhesh):
            self.netFil[i]=cv.filter2D(j,-1,np.array([[1,1,1],[1,-8,1],[1,1,1]]),borderType=cv.BORDER_DEFAULT)
        if self.Debug:
            cv.imshow("Fil{}".format(i), self.netFil[i])
    def Detect(self):
        for i,j in enumerate(self.gray):
            self.infoMarkers[i]=cv.aruco.detectMarkers(j, App.DICTIONARY, parameters = App.PARAMETERS)
            #print(self.infoMarkers[i])
            try:
                if self.infoMarkers[i][1] == None:
                    return 0
            except:
                return 1
    def SortName(self):
        #infomarker [corners][id][rejected points]
        for i,j in enumerate(self.infoMarkers):
            self.ListId[i].clear()
            for l,k in enumerate(self.infoMarkers[i][1]):
                   # print(k)
                    #print(self.infoMarkers[i][1][l])
                    #faire remplacement sur une ligne puis remplacer 
                a=(str(self.infoMarkers[i][1][l]).replace("[",""))
                a=a.replace("]","")
                    #print(a) 
                self.ListId[i].append(int(a))
                #print(self.ListId)
                    #print(self.ListId)
                   # m=str(k)
                   # #k=m[1:-1]
                   # k=m.replace("["," ")
                   # k=k.replace("]","")
                   # print(k)
                   # #self.infoMarkers[i][1][l]=list(int(k))
                   # print(self.infoMarkers[i][1][l])
            #self.found[i]=len(i[1])  
    def SortCorn(self,listcam:int,posList:int):
        #print("cam")
        #print(listcam)
        #print("pos")
        #print(posList)
        return (self.infoMarkers[listcam][0][posList])

    def TriTag(self):
        for i,j in enumerate(self.ListId):
            for k,l in enumerate(j):
                #print(k,l)
                self.tagin["tag{}".format(l)] = Tag(self.SortCorn(int(i),int(k)),self.ListId,int(l),int(k))
        return self.tagin
    
    def GetPos(self):
        a=list(self.tagin.keys())
        #print(a)
        if "tag"+str(App.MIDL) in a:
            for i in a:
                
                #print("42detected")
                #print(self.tagin["tag42"].vect2d)
                #print(self.tagin["{}".format(i)].vect2d)
                self.pos[0]=(self.tagin["tag42"].vect2d-self.tagin["{}".format(i)].vect2d).norme()
                #cv.imwrite("that{}".fromat(i),self.gray[0])
               #//self.pos[0]=(self.tagin["tag42"].x)-(self.tagin["{}".format(i)].x)
               #//self.pos[1]=(self.tagin["tag42"].y)-(self.tagin["{}".format(i)].y)
               #//self.pos[2]=(self.tagin["tag42"].z)-(self.tagin["{}".format(i)].z)
               #//x=((self.pos[0]**2)+(self.pos[1]**2)+(self.pos[2]**2)**0.5)
               #y=round(100*x,2)
                if self.DebugD:
                    print("entre 42 et {}".format(i)+"il y a {}".format(round((100*self.pos[0]),2)))
                    
    def DrawAxes(self)   :
        a=list(self.tagin.keys())
        #print(a)
        if "tag"+str(App.MIDL) in a:
            for i in a:
                
                self.gray[0] = cv.aruco.drawAxis(self.gray[0], App.CAMERA_MATRIX, App.DIST_COEFFS, self.tagin["{}".format(i)].rvecs,self.tagin["{}".format(i)].tvecs,0.10)
                
    def capVid(self):

            self.out.write(self.gray[0])#qcv.imwrite("Thataa",self.gray[0])
            cv.imwrite("mes{}.bmp".format(time.time()), self.gray[0])
            
                
            #print("{}".format(i)+str(self.tagin[i].getpos()))
    def __del__(self):
        print("coucou je delete man ")
        self.Release_All()
    def Release_All(self):
        for i in self.cap:
            i.release()
            self.out.release()
    def TagWork(self):
        self.SortName()
        self.TriTag()
        self.GetPos()
    def FrameWorking(self): 
        self.ToGray()
        self.DrawAxes()
        if self.capVidD:
            self.capVid()
        #self.Gauss()
        #self.Trhesh()
        #self.NetFil()
    def Update(self):
        self.ReadFrames()
        self.FrameWorking()
        if self.Detect():
            self.TagWork()
    
       
        #save Dictio {ID}:infomarker(propre à la caméra qui a détécté le tag)
        #save=self.TriTag()

         

class Tag:
    def __init__(self,corners:list,ListId:list,whoami:int,index:int,):
        self.posRe=(0,0)
        self.Facing=0
        self.Id=whoami
        self.tvecs=None
        self.rvecs=None
        self.tl=None
        self.tr=None
        self.bl=None
        self.br=None
        #(self.tl,self.tr,self.br,self.bl)=infoMarkers
        self.corners = corners
        self.x=0
        self.y=0
        self.z=0
        self.vect2d=None
        self.diffX=0
        self.diffY=0 
        self.debug=True
        if self.Id == App.MIDL:
            self.posRe=(1450,1200)
            self.marker_edge= App.MARKER_MIDL
        elif whoami == App.ROBOTS_T:
            self.marker_edge=App.MARKER_EDGE
        else:
            self.marker_edge=App.MARKER_EDGE
        
        self.update()
    def FindV(self):
        self.rvecs, self.tvecs, markerPoints= cv.aruco.estimatePoseSingleMarkers(self.corners,self.marker_edge, App.CAMERA_MATRIX, App.DIST_COEFFS)
         
        #return(self.rvecs,self.tvecs)
    def angles(self):
        mat_rota,jacob=cv.Rodrigues(self.rvecs)
        
    def FindD(self):
        self.x=self.tvecs[0][0][0]
        self.y=self.tvecs[0][0][1]
        self.z=self.tvecs[0][0][2]
        self.vect2d= Vector3(self.x,self.y,self.z)
    def update(self):
        self.FindV()
        self.FindD()
        if self.debug:
            print("tag{} ".format(self.Id)+"Tvec {}".format(self.vect2d)+"rvecs {}".format(self.rvecs))
            print("corners")
            print(self.corners)
            print("sa taille")
            print(self.marker_edge)
    
def main() -> int:
    app1 = App()
    app1.main()
    sys.exit(0)
   
    return 0
if __name__ == "__main__":
    main()