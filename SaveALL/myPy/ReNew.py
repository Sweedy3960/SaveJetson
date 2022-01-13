import numpy as np 
import cv2 as cv
import sys
import time
import math

from numpy.lib.function_base import interp


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
            "format=(string)NV12, framerate=(fraction)15/1 !"
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
    W_Center =np.array([(1450,1200,0),(1450,1300,0),(1550,1300,0),(1550,1200,0)], dtype="double")
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
        self.DebugPRojection=True
        self.planMrot=None
        self.planTvec=None
        self.planptsimg=None
        self.cntcap=0
        self.WcoinsTable=[(0,0,0),(0,2000,0),(3000,2000,0),(3000,0,0)]
        self.CcoinsTable=[]
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
        #disself.out= cv.VideoWriter("out.avi",cv.VideoWriter_fourcc(*"MJPG"),10.0,(3840,2160))
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
        b=list
        #print(a)
        if "tag"+str(App.MIDL) in a:
            for i in a:
                print("relations entre 42 et {}".format(i))
                b=self.RelativePos(self.tagin["tag42"].rvecs,self.tagin["tag42"].tvecs,self.tagin["{}".format(i)].rvecs,self.tagin["{}".format(i)].tvecs)
                #print("Rvec Comp")
                #print(b[0])
                #print("Tvec Comp")
               # print(b[1])
                
                #*********************************************************
                #b=self.Planestimation()
                #print("laaa")
                #print(b)
                #b=self.RelativePos(b[0],b[1],self.tagin["{}".format(i)].rvecs,self.tagin["{}".format(i)].tvecs)
                #*************************
                #print("42detected")sa
                #print(self.tagin["tag42"].vect2d)
                #print(self.tagin["{}".format(i)].vect2d)
                #self.pos[0]=(self.tagin["tag42"].vect2d-self.tagin["{}".format(i)].vect2d).norme()
                #cv.imwrite("that{}".fromat(i),self.gray[0])
               #//self.pos[0]=(self.tagin["tag42"].x)-(self.tagin["{}".format(i)].x)
               #//self.pos[1]=(self.tagin["tag42"].y)-(self.tagin["{}".format(i)].y)
               #//self.pos[2]=(self.tagin["tag42"].z)-(self.tagin["{}".format(i)].z)
               #//x=((self.pos[0]**2)+(self.pos[1]**2)+(self.pos[2]**2)**0.5)
               #y=round(100*x,2)
                #if self.DebugD:
                #    print("entre 42 et {}".format(i)+"il y a {}".format(round((100*self.pos[0]),2)))
                print("diff en X:{}".format((b[1][0]*100))+"cm")
                print("diff en Y:{}".format((b[1][1]*100))+"cm")
                    
    def DrawAxes(self)   :
        a=list(self.tagin.keys())
        #print(a)
        if "tag"+str(App.MIDL) in a:
            for i in a:
                self.gray[0] = cv.aruco.drawAxis(self.gray[0], App.CAMERA_MATRIX, App.DIST_COEFFS, self.tagin["{}".format(i)].rvecs,self.tagin["{}".format(i)].tvecs,0.10)

    def RelativePos(self,rvec1,tvec1,rvec2,tvec2):
        info=list
        #print(tvec1,tvec2)
        composedRvec=None
        composedTvec=None
        rvec1,tvec1=rvec1.reshape((3,1)),tvec1.reshape((3,1))
        rvec2,tvec2=rvec2.reshape((3,1)),tvec2.reshape((3,1))
        #print(tvec1,tvec2)
        #inverse le deuxieme marker 
        invRvec, invTvec=self.InvPersp(rvec1,tvec1)
        #print(invTvec,tvec2)
        info= cv.composeRT(rvec2,tvec2,invRvec,invTvec)
        composedRvec=info[0]
        composedTvec=info[1]
        #print(composedRvec)
        #print(composedTvec)
        #print(type(composedRvec))
    
        composedRvec=composedRvec.reshape((3,1))
        composedTvec=composedTvec.reshape((3,1))
        return composedRvec,composedTvec

    def DiffPos(self,composedRvec,composedTvec,Rvec,Tvec):
        info=[0,0]
        if composedRvec is not None and composedTvec is not None:
            cv.composeRT(composedRvec,composedTvec,Rvec,Tvec,info[0],info[1])
            TcompR,TcompT = info[0],info[1]
            return TcompR,TcompT


    def InvPersp(self,rvec1,tvec1):
        R,_=cv.Rodrigues(rvec1)
        R=np.matrix(R).T
        invTvec=np.dot(R,np.matrix(-tvec1))
        invRvec,_=cv.Rodrigues(R)
        #print(invTvec,invRvec)
        return invRvec,invTvec

    def capVid(self):
            #self.out.write(self.gray[0])#qcv.imwrite("Thataa",self.gray[0])
            cv.imwrite("mes{}.bmp".format(time.time()), self.gray[0]) 
            print(time.time())
            #print("{}".format(i)+str(self.tagin[i].getpos()))
    def Getplan(self):
        ret,rvec,tvec = cv.solvePnP(App.W_Center,self.tagin["tag42"].corners,App.CAMERA_MATRIX,App.DIST_COEFFS)
        return [rvec,tvec]

    def projecttablepoint(self):
        a=self.Getplan()
        self.planMrot,_=cv.Rodrigues(a[0])
        self.planTvec=a[1].ravel().reshape(3)
        for i in self.WcoinsTable:
            self.planptsimg=cv.projectPoints(i,self.planMrot,self.planTvec,App.CAMERA_MATRIX,App.DIST_COEFFS)
            #cv.circle(self.gray[0],(self.planptsimg[0],self.planptsimg[1]),10,(255,0,0),cv.FILLED,cv.LINE_8)
            #self.gray[0]=cv.putText(self.gray[0],str(i),(self.planptsimg[0],self.planptsimg[1]),fontFace=cv.FONT_HERSHEY_DUPLEX,fontScale=3.0,color=(125,245,55),thickness=3)
        if self.DebugPRojection:
            cv.imwrite("Table?.png",self.gray[0])
    def recherchecentreTag(self,plantimg,centrepix,Mrot,Tvec):
        foundx=False
        foundy=False
        #coordonée dans img
        cx=int(centrepix[0])
        cy=int(centrepix[1])
        #position fixtive dans limage
        x0=0
        y0=0
        #coordonée irl
        xw=1500
        yw=1000
        zw=0

        
        while foundx==False and foundy==False:
            a,_=cv.projectPoints((xw,yw,zw),self.planMrot,self.planTvec,App.CAMERA_MATRIX,App.DIST_COEFFS)
            x0=a[0][0][0]
            y0=a[0][0][1]
            #print("working")
            if x0 < (cx+2) and x0 > (cx-2):
                #print("foundx")
                foundx=True
            elif x0 > cx:
                xw=xw-1
            else:
                xw=xw+1

            if y0 < (cy+2) and y0 > (cy-2):
                foundx=True
                #print("foundy")
            elif x0 > cx:
                yw=yw-1
            else:
                yw=yw+1
            #print([x0,y0])
            #print(cx,cy)
        return[xw,yw]
        





    def __del__(self):
        print("coucou je deconstruit")
        self.Release_All()

    def Release_All(self):
        for i in self.cap:
            i.release()
            self.out.release()

    def TagWork(self):
        self.SortName()
        self.TriTag()
        self.projecttablepoint()
        #self.GetPos()
        b= list(self.tagin.keys())
        b.remove("tag42")
        #print(b)
        for i in b:
            a= self.recherchecentreTag(self.planptsimg,self.tagin[i].centrepix,self.planMrot,self.planTvec)
            self.tagin[i].irlcord=a
            print(self.tagin[i].Id,self.tagin[i].irlcord)
        

    def FrameWorking(self): 
        self.ToGray()
        self.cntcap=self.cntcap +1
        if self.capVidD :
            if self.cntcap ==10:
                self.capVid()
                self.cntcap=0

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
        self.mat_rota=None
        #(self.tl,self.tr,self.br,self.bl)=infoMarkers
        self.corners = corners
        self.centrepix=[int(((corners[0][0][0]+corners[0][1][0]+corners[0][2][0]+corners[0][3][0])*0.25)),int(((corners[0][0][1]+corners[0][1][1]+corners[0][2][1]+corners[0][3][1])*0.25))]

        self.irlcord=(0,0)
        self.yall=0
        self.pitch=0
        self.roll=0    
        self.vect2d=None
        self.diffX=0
        self.diffY=0 
        self.debug=False
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
        (self.rvecs-self.tvecs).any()
        #return(self.rvecs,self.tvecs)
    def anglesCam(self):
        self.mat_rota,jacob=cv.Rodrigues(self.rvecs)
        #[X]
        roll=math.degrees(math.atan2(self.mat_rota[2][1],self.mat_rota[2][2]))
        #[Y]
        pitch=math.degrees(math.atan2(-self.mat_rota[2][0],(((self.mat_rota[2][1]**2)+(self.mat_rota[2][2]**2))**0.5)))
        #[Z]
        yall=math.degrees(math.atan2(self.mat_rota[1][0],self.mat_rota[0][0]))
        return yall,pitch,roll
   
    def poscam(self):
        campos=-self.mat_rota*self.tvecs
        return campos
    def getYallPitchRoll(self):
        #MatRot=np.zeros(shape=(3,3))
        #cv.Rodrigues(self.rvecs,MatRot,jacobian=0)
        #ypr=cv.RQDecomp3x3(MatRot)
        

        self.mat_rota=cv.Rodrigues(self.rvecs)[0]
        #print(self.mat_rota)
        #print(self.tvecs)
        #P=np.hstack((self.mat_rota,np.matrix(self.tvecs)))
        #eulerRad= -cv.decomposeProjectionMatrix(P)[6]
        #eulerDeg= 180*eulerRad/math.pi
        #pitch,yaw,roll = [math.radians(_) for _ in eulerRad]
        ##yaw= 180*eulerRad[1,0]/math.pi
        ##pitch= 180*((eulerRad[0,0]+math.pi/2)*math.cos(eulerRad[1,0]))/math.pi
        ##roll= 180*((-(math.pi/2)-eulerRad[0,0])*math.sin(eulerRad[1,0])+eulerRad[2,0])/math.pi
        #pitch=math.degrees(math.asin(math.sin(pitch)))
        #yaw=-math.degrees(math.asin(math.sin(roll)))
        #roll=math.degrees(math.asin(math.sin(yaw)))
        #return F"({yaw},{pitch},{roll})"
    def FindD(self):
        self.x=self.tvecs[0][0][0]
        self.y=self.tvecs[0][0][1]
        self.z=self.tvecs[0][0][2]
        self.vect2d= Vector3(self.x,self.y,self.z)

    def update(self):
        self.FindV()
        self.FindD()
        self.yall, self.pitch, self.roll =self.anglesCam()
        if self.debug:
            print("tag{} ".format(self.Id)+"/n Tvec {}".format(self.vect2d)+"rvecs {}".format(self.rvecs))
            print("corners{}".format(self.corners))
            print("sa taille{}".format(self.marker_edge))
            print("yall[Z]:{}".format(self.yall)+"pitch[Y]:{}".format(self.pitch)+"roll[X]:{}".format(self.roll))
            #print("position irl{}".format(self.irlcord))
            #print(self.getYallPitchRoll())
            #self.poscam()
    
def main() -> int:
    app1 = App()
    app1.main()
    sys.exit(0)
   
    return 0
if __name__ == "__main__":
    main()