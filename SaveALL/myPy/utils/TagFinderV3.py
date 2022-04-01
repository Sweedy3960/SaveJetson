"""
Essai d'une détéction de cordonée d'un tag dans le monde réel, grâce à une image
Help: Github copilot
"""
import cv2 as cv
import numpy as np

class IgId():
    """
    class list contenant les Tag visible dans une partie
    """
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
    RED = 47
    BLUE = 13
    GREEN = 36
    ROCK = 17
    MIDL = 42
    ROBOT = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    SAMPLE = [47, 13, 36, 17]
    
    
class Size():
    """
    class liste des tailles des tags
    """
    ROBOT = 0.07
    MIDL = 0.10
    SAMPLE = 0.05

class Tag:
    """
    objet de type Tag
    Propriété:
    - id: int
    - corn: liste de liste de int
    - cam: int
    - coordImg: liste de int
    - coordMonde: liste de int
    Méthode:
    - 
    """
    def __init__(self,_id,_corns,_cam) -> None:
        """¨
        constructeur de la classe Tag
        """
        self.id=_id
        self.corns=_corns
        self.cam=_cam
        self.coordImg = (0, 0)
        self.pixelcentralImg =[int((( self.corns[0][0][0]+ self.corns[0][1][0]+ self.corns[0][2][0]+ self.corns[0][3][0])*0.25)),
                          int((( self.corns[0][0][1]+ self.corns[0][1][1]+ self.corns[0][2][1]+ self.corns[0][3][1])*0.25))]
        self.size = self.getSize()
        if self.id == IgId.MIDL:
            self.coordMondeCorns = App.W_Center
            self.PosMonde =(1450, 1200,0)
            App.PLAN.append(Plan(self.coordMonde,self.coordImg,App.MAT[self.cam], App.DIST[self.cam]))
        else:
            self.PosMonde = self.searchWoldPos()
    def getSize(self):
        """
        retourne la taille du tag
        """
        if self.id in IgId.ROBOT:
            return Size.ROBOT
        elif self.id in IgId.MIDL:
            return Size.MIDL
        elif self.id in IgId.SAMPLE:
            return Size.SAMPLE
        else:
            return None
    def searchWoldPos(self):
        """
        Cherche la position du tag dans le monde
        utilisation de la foction de projection pour trouver des cordonée dans une image
        """
        xw=0
        yw=0
        zw=0
        xc=self.pixelcentralImg[0]
        yc=self.pixelcentralImg[1]
        while foundx == False or foundy == False:
            a, _ = cv.projectPoints(
                    (xw, yw, zw), Tag.planMrot[self.cam], Tag.planTvec[self.cam], App.MAT[self.cam], App.DIST[self.cam])
            x0 = a[0][0][0]
            y0 = a[0][0][1]

            if x0 > (xc-2) and x0 < (xc+2):
                foundx = True
            elif x0 > (xc+2):
                xw += 0.01
            elif x0 < (xc-2):             
                xw -= 0.01
            
            if y0 > (yc-2) and y0 < (yc+2):
                foundy = True
            elif y0 > (yc+2):
                yw += 0.01
            elif y0 < (yc-2): 
                yw -= 0.01
        return (xw, yw, zw)
    
class servTCP:
    """
    class de service de communication TCP
    """
    def __init__(self,_ip,_port) -> None:
        """
        constructeur de la classe
        """
        self.ip=_ip
        self.port=_port
        self.sock=None
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((self.ip,self.port))
    def bind(self,_ip,_port) -> None:
        """
        bind la connexion
        """
        self.sock.bind((_ip,_port))
    def listen(self,_n) -> None:
        """
        ecoute sur un port
        """
        self.sock.listen(_n)
    def encode(self,_msg) -> bytes:
        """
        encode un message
        """
        return _msg.encode()
    def send(self,_msg) -> None:
        """
        envoie un message
        """
        self.sock.send(self.encode(_msg))
    def recv(self) -> None:
        """
        recoit un message
        """
        self.sock.recv(1024)
    def close(self) -> None:
        """
        ferme la connexion
        """
        self.sock.close()

class capture:
    """
    objet de type capture
    """
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
        """
        Retourne le pipeline gstreamer
        """
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
class Plan:
    """
    class avec les infos plans
    """
    def __init__(self,_coord,_coordImg,_mat,_dist) -> None:
        ret, self.rvec, self.tvec = cv.solvePnP( _coord, _coordImg, _mat, _dist)
        self.planMrot[self.cam], _ = cv.Rodrigues(self.rvec)
        self.planTvec[self.cam] = self.tvec.ravel().reshape(3)
class App:
    """
    objet de type App
    """
    CALIB_PATH = "SaveALL/myFi/"
    CAMERA_MATRIX_HQ = np.loadtxt(CALIB_PATH+'cam12matvid.txt', delimiter=',')
    DIST_COEFFS_HQ = np.loadtxt(CALIB_PATH+'cam12distvid.txt', delimiter=',')
    CAMERA_MATRIX_FI = np.loadtxt(CALIB_PATH+'FishMat.txt', delimiter=',')
    DIST_COEFFS_FI = np.loadtxt(CALIB_PATH+'FishDist.txt', delimiter=',')
    MAT = [CAMERA_MATRIX_HQ, CAMERA_MATRIX_FI]
    DIST = [DIST_COEFFS_HQ, DIST_COEFFS_FI]
    #Position [W]ordl des coins du tag du centre
    W_Center = np.array([(1450, 1200, 530), (1550, 1200, 530),
                        (1550, 1300, 530), (1450, 1300, 530)], dtype="double")
    PLAN=[]
    def __init__(self):
        """
        Constructeur de la classe
        """

        self.NbCam=2
        self.ip=""
        self.port=0
        self.launchServer()
    def launchServer(self):
        """
        Lance le serveur
        """
        serv=servTCP(self.ip,self.port)
        serv.bind(self.ip,self.port)
        serv.listen(1)
    
        
    def createpipe(self):
        """
        Retourne la liste des pipelines gstreamer
        """
        return [capture(i).gstreamer_pipeline() for i in range(self.NbCam)]

    def createcapture(self):
        """
        Retourne la liste des captures
        """
        return [cv.VideoCapture(i) for i in self.createpipe()]
    def readcapture(self):
        """
        Retourne la liste des images
        """
        return [i.read()[1] for i in self.createcapture()]
    def closecapture(self):
        """
        Ferme les captures
        """
        for i in self.createcapture():
            i.release()
    def togray(self):
        """
        Retourne la liste des images en niveau de gris
        """
        return [cv.cvtColor(i, cv.COLOR_BGR2GRAY) for i in self.readcapture()]

    def tagdetecion(self):
        """
        Retourne une liste d'objet tags detectés dans chaque image
        """
        return [cv.aruco.detectMarkers(i, cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_50)) for i in self.togray()]
    def tri(self):
        """
        Retourne une liste d'objet tags trié
        """
        a=self.tagdetecion()

        
    
    