import enum
import string
import numpy as np 
import cv2 as cv
import sys
import time
from enum import Enum

class Capture :
    def __init__(self,_idCam):
        self.idCam=_idCam
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
            #Possible modif de framerate si nécéssaire 
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
    #création des paramètre nécéssaires à la détéction 
    PARAMETERS = cv.aruco.DetectorParameters_create()
    DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
    NB_CAM=2
    #Id du Tag centrale
    MIDL=42
    #Plage d'id des tag pour échantillons 
    SAMPLES_T=[47,13,36,17]
    #Plage d'id des tag pour robots 
    ROBOTS_T=[1,2,3,4,5,6,7,8,9,10]
    #Position [W]ordl des coins du tag du centre 
    W_Center =np.array([(1450,1200,530),(1550,1200,530),(1550,1300,530),(1450,1300,530)], dtype="double")
    #Chemins d'accès au fichier de calibration (modifie si nécéssaire)
    CALIB_PATH="SaveALL/myFi/"
    CAMERA_MATRIX_HQ = np.loadtxt(CALIB_PATH+'cam12matvid.txt', delimiter=',')  
    DIST_COEFFS_HQ  = np.loadtxt(CALIB_PATH+'cam12distvid.txt', delimiter=',')
    CAMERA_MATRIX_FI = np.loadtxt(CALIB_PATH+'FishMat.txt', delimiter=',')  
    DIST_COEFFS_FI  = np.loadtxt(CALIB_PATH+'FishDist.txt', delimiter=',')
    def __init__(self) -> None: 
    
        self.capture1 = []
        for i in App.NB_CAM:
            self.capture1.append(Capture(i))
        self.img = ImProc(self.capture1)
        self.run=True
  
    def main(self) -> None:
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
        self.infoMarkers = []
        self.cap=[]
        self.ListId=[]
        self.tagin={}
        self.planMrot=None
        self.planTvec=None
        self.planptsimg=None
        self.WcoinsTable=[(0,0,0),(0,2000,0),(3000,2000,0),(3000,0,0)]
        self.CcoinsTable=[]
        for i in cap:
            self.frame.append(None)
            self.cap.append(cv.VideoCapture(i.gstreamer_pipeline(),cv.CAP_GSTREAMER))
            self.infoMarkers.append(None)  
            self.ListId.append([])
            self.gray.append(None)
        
   
    def __del__(self):
        """
        déconstructeur:
        si intruption quelconque fermeture des pipeline
        pour évité la surchage de pipeline ouvers ou cas ou mauvais arret de l'app 
        """
        print("coucou je deconstruit")
        self.Release_All()

    def ReadFrames(self):
        for i,j in enumerate(self.cap):
            ret,self.frame[i]=j.read()
            
    def ToGray(self):
        for i,j in enumerate(self.frame):
            self.gray[i]=cv.cvtColor(j, cv.COLOR_BGR2GRAY)

    def Detect(self):
        for i,j in enumerate(self.gray):
            self.infoMarkers[i]=cv.aruco.detectMarkers(j, App.DICTIONARY, parameters = App.PARAMETERS)
            try:
                if self.infoMarkers[i][1] == None:
                    return 0
            except:
                return 1
    
    def SortName(self):
        for i,j in enumerate(self.infoMarkers):
            self.ListId[i].clear()
            for l,k in enumerate(self.infoMarkers[i][1]):
                a=(str(self.infoMarkers[i][1][l]).replace("[",""))
                a=a.replace("]","")
                self.ListId[i].append(int(a))
              

    def SortCorn(self,listcam:int,posList:int):
        return (self.infoMarkers[listcam][0][posList])

    def TriTag(self):
        for i,j in enumerate(self.ListId):
            for k,l in enumerate(j):
                self.tagin["tag{}".format(l)] = Tag(self.SortCorn(int(i),int(k)),self.ListId,int(l),int(k))
        return self.tagin

    def Getplan(self):
        ret,rvec,tvec = cv.solvePnP(App.W_Center,self.tagin["tag42"].corners,App.CAMERA_MATRIX,App.DIST_COEFFS)
        return [rvec,tvec]

    def projecttablepoint(self):
        a=self.Getplan()
        self.planMrot,_=cv.Rodrigues(a[0])
        self.planTvec=a[1].ravel().reshape(3)
        for i in self.WcoinsTable:
            self.planptsimg,_=cv.projectPoints(i,self.planMrot,self.planTvec,App.CAMERA_MATRIX,App.DIST_COEFFS)
            b=self.planptsimg[0][0][0]
            c=self.planptsimg[0][0][1]
            z=self.gray[0]
            z= cv.circle(z,(int(b),int(c)),2,(255,0,0),thickness=3,lineType= cv.FILLED)
            z=cv.putText(z,str(i),(int(b),int(c)),fontFace=cv.FONT_HERSHEY_DUPLEX,fontScale=3.0,color=(125,245,55),thickness=3)
            self.CcoinsTable.append(b,c)

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
        xw=0
        yw=0
        zw=0
        while foundx==False or foundy==False:
            a,_=cv.projectPoints((xw,yw,zw),self.planMrot,self.planTvec,App.CAMERA_MATRIX,App.DIST_COEFFS)
            x0=a[0][0][0]
            y0=a[0][0][1]

            if x0 > (cx-2) and x0<(cx+2):
                if self.DebugPRojection:
                    print("foundx")
                foundx=True
            elif x0 > cx:
                xw=xw-1
            else:
                xw=xw+1

            if y0 >(cy-2) and y0<(cy+2):
                foundy=True
                if self.DebugPRojection:
                    print("foundy")
            elif y0 > cy:
                yw=yw-1
            else:
                yw=yw+1
                if self.DebugPRojection:
                    print([x0,y0])
                    print(cx,cy) 
                    print([xw,yw])
        return[xw,yw]


    def Release_All(self):
        for i in self.cap:
            i.release()
            self.out.release()

    def TagWork(self):
        self.SortName()
        self.TriTag()
        self.projecttablepoint()
        b= list(self.tagin.keys())
        b.remove("tag42")
        for i in b:
            a= self.recherchecentreTag(self.planptsimg,self.tagin[i].centrepix,self.planMrot,self.planTvec)
            print(a)
            self.tagin[i].irlcord=a
            print(self.tagin[i].Id,self.tagin[i].irlcord)
        

    def FrameWorking(self): 
        self.ToGray()

  
    def Update(self):
        self.ReadFrames()
        self.FrameWorking()
        if self.Detect():
            self.TagWork()
    


         

class Tag:
    def __init__(self,corners:list,ListId:list,whoami:int,index:int,):
        self.posRe=(0,0)
        self.Facing=0
        self.Id=whoami
        self.tvecs=None
        self.rvecs=None
        self.mat_rota=None
        self.corners = corners
        self.centrepix=[int(((corners[0][0][0]+corners[0][1][0]+corners[0][2][0]+corners[0][3][0])*0.25)),int(((corners[0][0][1]+corners[0][1][1]+corners[0][2][1]+corners[0][3][1])*0.25))]
        self.irlcord=(0,0)  
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
       

    def update(self):
        self.FindV()

def main() -> string:
    app1 = App()
    app1.main()
    sys.exit(0)
   
    return 0
if __name__ == "__main__":
    main()
