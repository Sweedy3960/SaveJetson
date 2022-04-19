import enum
import string
import numpy as np
import cv2 as cv
import sys



class Capture:
    '''
     pipeline de capture video gstreamer
     probriété:
        résolution:
        3840x2160px,
        id de la caméra,
        orientation
    '''
    def __init__(self, _idCam):
        """
        constructeur de la classe
        """
        self.idCam = _idCam
        if self.idCam == 0:
            self.capture_width = 3840
            self.capture_height = 2160
            self.display_width = 3840
            self.display_height = 2160
        elif self.idCam == 1:
            self.capture_width = 3264
            self.capture_height = 2464
            self.display_width = 3264
            self.display_height = 2464
        self.flip_method = 2

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


class Tag:
    planMrot = [0, 0] # id 0 hq, id 1 fisheye
    planTvec = [0, 0]
    def __init__(self,_id,_corns,_cam):
        self.id = _id
        print(self.id)
        self.cam = _cam
        self.tvecs = None
        self.rvecs = None
        self.corners = _corns
        self.centrepix = [int((( self.corners[0][0][0]+ self.corners[0][1][0]+ self.corners[0][2][0]+ self.corners[0][3][0])*0.25)),
                          int((( self.corners[0][0][1]+ self.corners[0][1][1]+ self.corners[0][2][1]+ self.corners[0][3][1])*0.25))]
        self.irlcord = (0, 0)

        if self.id == IgId.MIDL:
            self.posRe = (1450, 1200)
            self.marker_edge = TagIgSize.MIDL
            self.getPlan()
        elif self.id in IgId.ROB:
            self.marker_edge = TagIgSize.ROBOT
        else:
            self.marker_edge = TagIgSize.SAMPLE
       

    def findV(self):
        self.rvecs, self.tvecs, markerPoints = cv.aruco.estimatePoseSingleMarkers(
            self.corners, self.marker_edge, App.MAT[self.cam], App.DIST[self.cam])

    def getPlan(self): 

        ret, rvec, tvec = cv.solvePnP(App.W_Center,self.corners[0], App.MAT[self.cam], App.DIST[self.cam])
        Tag.planMrot[self.cam], _ = cv.Rodrigues(rvec)
        Tag.planTvec[self.cam] = tvec.ravel().reshape(3)
        

    def getWpos(self):
        """
        trouve la position dans le monde réel du tag
        """
        if self.id == IgId.MIDL:
            return (1450, 1200)
        foundx = False
        foundy = False
        #coordonée dans img
        cx = int(self.centrepix[0])
        cy = int(self.centrepix[1])
        #position fixtive dans limage
        x0 = 0
        y0 = 0
        #coordonée irl
        xw = 0
        yw = 0
        zw = 0
        while foundx != True or foundy != True: # not(fonownx and foundy)
                a, _ = cv.projectPoints(
                (xw, yw, zw), Tag.planMrot[self.cam], Tag.planTvec[self.cam],App.MAT[self.cam], App.DIST[self.cam])
                x0 = a[0][0][0]
                y0 = a[0][0][1]
                if x0 > (cx-2) and x0<(cx+2): # (cx - 2) < x0 < (cx + 2):
                    foundx = True
                elif x0 > cx:
                    xw = xw-1
                else:
                    xw = xw+1

                if y0 >(cy-2) and y0<(cy+2): # (cy - 2) < y0 < (cy + 2):
                    foundy = True
                elif y0 > cy:
                    yw = yw-1
                else:
                    yw = yw+1
                self.irlcord = (xw, yw) 
                print("image:", cx, cy, "trouvé:", x0, y0, "irl:", xw, yw)
        self.irlcord = (xw, yw)

    def __str__(self):
        return "Tag" + str(self.id) + str(self.irlcord)

    def update(self):
        self.getWpos()
        self.findV()

class IgId():
    '''Tag in game, tag possible d'être perçus par l'app d'uanrt le match'''
    ROB0 = 1
    ROB1 = 2
    ROB2 = 3
    ROB3 = 4
    ROB4 = 5
    ROB5 = 6
    ROB6 = 7
    ROB7 = 8
    ROB8 = 9
    ROB9 = 10
    ROB = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    RED = 47
    BLUE = 13
    GREEN = 36
    ROCK = 17
    MIDL = 42


class TagIgSize():
    ROBOT = 0.07
    MIDL = 0.10
    SAMPLE = 0.05


class App:
    #création des paramètre nécéssaires à la détéction
    PARAMETERS = cv.aruco.DetectorParameters_create()
    DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
    NB_CAM = 2
    #Position [W]ordl des coins du tag du centre
    W_Center = np.array([(1450, 1200, 530), (1550, 1200, 530),
                        (1550, 1300, 530), (1450, 1300, 530)], dtype="double")
    #Chemins d'accès au fichier de calibration (modifie si nécéssaire)
    CALIB_PATH = "SaveALL/myFi/"
    CAMERA_MATRIX_HQ = np.loadtxt(CALIB_PATH+'cam12matvid.txt', delimiter=',')
    DIST_COEFFS_HQ = np.loadtxt(CALIB_PATH+'cam12distvid.txt', delimiter=',')
    CAMERA_MATRIX_FI = np.loadtxt(CALIB_PATH+'FishMat.txt', delimiter=',')
    DIST_COEFFS_FI = np.loadtxt(CALIB_PATH+'FishDist.txt', delimiter=',')
    MAT = [CAMERA_MATRIX_HQ, CAMERA_MATRIX_FI]
    DIST = [DIST_COEFFS_HQ, DIST_COEFFS_FI]

    def __init__(self) -> None:

        self.capture1 = []
        for i in range(App.NB_CAM):
            self.capture1.append(Capture(i))
        self.img = ImProc(self.capture1)
        self.run = True

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

    def __init__(self, cap: list):
        self.frame = []
        self.gray = []
        self.infoMarkers = []
        self.cap = []
        self.tagin = []
        self.planMrot = []
        self.planTvec = []
        self.planptsimg = []
        self.WcoinsTable = [(0, 0, 0), (0, 2000, 0),
                            (3000, 2000, 0), (3000, 0, 0)]
        self.CcoinsTable = []

        for i in cap:
            self.frame.append(None)
            self.cap.append(cv.VideoCapture(
                i.gstreamer_pipeline(), cv.CAP_GSTREAMER))
            self.infoMarkers.append(None)
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
        for i, j in enumerate(self.cap):
            ret, self.frame[i] = j.read()

    def ToGray(self):
        for i, j in enumerate(self.frame):
            self.gray[i] = cv.cvtColor(j, cv.COLOR_BGR2GRAY)

    def Detect(self):
        for i, j in enumerate(self.gray):
            self.infoMarkers[i] = cv.aruco.detectMarkers(
                j, App.DICTIONARY, parameters=App.PARAMETERS)
            try:
                if self.infoMarkers[i][1] == None:
                    return 0
            except:
                return 1

  
    def SortCorn(self, listcam: int, posList: int):
        return (self.infoMarkers[listcam][0][posList])

    def TriTag(self):
        '''
        création des tags dans une liste 
        '''
        self.tagin.clear()
        for idCam, infoCam in enumerate(self.infoMarkers):
            if infoCam[1] is not None:
                for index, id in enumerate(infoCam[1]):
                    self.tagin.append(Tag(id, infoCam[0][index], idCam)) # ici après on fait update
            
    def Tri(self):
        '''
        obselte
        tri des tags pour avoir les tags centraux au début de la liste
        '''
        a = []
        b = []
        for i, j in enumerate(self.tagin):
            if j.id == IgId.MIDL:
                a.append(self.tagin.pop(i))
        b = a+self.tagin
        self.tagin = b

    def Release_All(self):
        for i in self.cap:
            i.release()
            self.out.release()

    def TagWork(self):
        self.TriTag()
        self.Tri()
        '''
        modif data serv tcp to send
        '''
        for tag in self.tagin:
            tag.update()
        print(self.tagin)

    def FrameWorking(self):
        self.ToGray()

    def Update(self):
        self.ReadFrames()
        self.FrameWorking()
        if self.Detect():
            self.TagWork()


def main() -> string:
    app1 = App()
    app1.main()
    sys.exit(0)

    return 0


if __name__ == "__main__":
    main()
