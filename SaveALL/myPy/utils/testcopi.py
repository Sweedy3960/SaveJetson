"""
Essai d'une détéction de cordonée d'un tag dans le monde réel, grâce à une image
Help: Github copilot
"""
import cv2 as cv

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
        self.coordMonde = (0, 0)
        self.size = self.getSize()
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
    def send(self,_msg) -> None:
        """
        envoie un message
        """
        self.sock.send(_msg)
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
    def __init__(self):
        """
        Constructeur de la classe
        """
        self.idCam=0
        self.capture_width=3264
        self.capture_height=1848
        self.display_width=500
        self.display_height=500
        self.flip_method=2
       
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

class App:
    """
    objet de type App
    """
    def __init__(self):
        """
        Constructeur de la classe
        """
        self.NbCam=2
    def createpipe(self):
        """
        Retourne la liste des pipelines gstreamer
        """
        return [capture().gstreamer_pipeline() for i in range(self.NbCam)]

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
        Retourne la liste info des tags détécter dans les images en niveau de gris
        """
        return [cv.aruco.detectMarkers(i,cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)) for i in self.togray()]
    def tagcreate(self):
        """
        Créer les objets de type Tag avec les informations des tags détécter en paramètres
        """
        return [Tag(j[0][0][0],j[0][0][1],i) for i,j in enumerate(self.tagdetecion())]
    