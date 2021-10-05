#tentativePoopython
#utilisation des libraires:
#opencv-python/module aruco
#numpi
import cv2 as cv
import numpy as np
#Definition et variable globales?
PARAMETERS = cv.aruco.DetectorParameters_create()
DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
#POSITION ???
def gstreamer_pipeline(
    capture_width=500,
    capture_height=500,
    display_width=500,
    display_height=500,
    framerate=10,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )
def detect():
        ret,frame = img.read()
        
        gray= cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        try:
            corners, ids, rejctedImgsPoints = cv.aruco.detectMarkers(frame,DICTIONARY,parameters = PARAMETERS)
            print(ids)
        except:
            print("EH non !")
            pass
#Création d'un marqueur
class marker:
    #avec ces positions
    def __init__(self):
        self.x=0
        self.y=0
       
        #dessine sur lui meme (debug)
    def draw(self,frame):
        frame = cv.aruco.drawDetectedMarkers(frame,his.corners,his.id)
     #distribue les info en fct du nom d'objet
    def tri(marker,frame):
        vector=np.transpose(corners)
        self.marker.self.x = vector[0][0]
        self.marker.self.y = vector[1][0]  
if __name__=="__main__":
    img = cv.VideoCapture(gstreamer_pipeline(flip_method=2), cv.CAP_GSTREAMER)
    while (True):
        try:
            print("aa")
            saveidsize = np.size(ids)
            print("save size ok ")
            print(ids)
            
        except:
            pass
        detect()
        print("detect ok ")
        try:
            #création marker si nécéssaire?
            print("crea")
            if((np.size(ids)>0)):
                print("test ajout marker ok ")
                markers0 = marker()
                print("marker0 ok ")
        except:
            pass
        try:
            print("bb")
            markers0.draw(self,frame)
            print("draw marker0 ok")
            cv.imshow("that",frame)
            print(ids)
        except:
            pass
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
cv.destroyAllWindows()
