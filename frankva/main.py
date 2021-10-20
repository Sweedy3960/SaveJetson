import cv2 as cv
import numpy as np
import platform
#--------------------------------------------------------------






#---------------------------------------------------------------
#GST_ARGUS: Available Sensor modes :
#GST_ARGUS: 3264 x 2464 FR = 21.000000 fps Duration = 47619048 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
#GST_ARGUS: 3264 x 1848 FR = 28.000001 fps Duration = 35714284 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
#GST_ARGUS: 1920 x 1080 FR = 29.999999 fps Duration = 33333334 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
#GST_ARGUS: 1640 x 1232 FR = 29.999999 fps Duration = 33333334 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
#GST_ARGUS: 1280 x 720 FR = 59.999999 fps Duration = 16666667 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
#GST_ARGUS: 1280 x 720 FR = 120.000005 fps Duration = 8333333 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;
#modification d'un pipeline trouvé sur le net pour test de capture 
class capture :
    
    def __init__(self):
        self.idCam = 0
        self.capture_width = 3264
        self.capture_height = 1848
        self.display_width = 500
        self.display_height = 500
        self.flip_method = 2
       
    def gstreamer_pipeline(self):
        if not "x86_64":
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
        else:
            return self.idCam
    

class imgProcess :
    def __init__(self, cap):
        #frame list [0]=ret= booléen vrai si val retournée
        #[1]=image(numpy.ndarray)
        self.axe = True
        self.windows = True
        self.frame = []
        
        for i in cap:
            self.frame.append(None)
        
        self.gray = []
        for i in self.frame:
            self.gray.append(None)
        
    
        #img = type videocapture
        self.cap = []
        for i in cap:
            #capture1.gstreamer_pipeline()
            self.cap.append(cv.VideoCapture(i.gstreamer_pipeline(), cv.CAP_GSTREAMER))
            if not self.cap[-1].isOpened():
                exit()
            
        #infomarker [0]=corners [1]=ids [2]=rejectedpoints
        self.infoMarkers = []
        for i in cap:
            self.infoMarkers.append(None)
    
    def __str__(self):
        return f"{self.frame}, {self.gray}, {self.cap}, {self.infoMarkers}"
    
    def release_all(self):
        for i in self.cap:
            i.release()

    def enleve_couleur(self):
        #BGR to gray enleve les couleurs
        for i in self.frame:
            for j in self.gray:
                j = cv.cvtColor(i, cv.COLOR_BGR2GRAY)

    def read_frame(self):
        run = True
        while run:
            for i, j in enumerate(self.cap):
                (ret, self.frame[i]) = j.read()
                if not ret:
                    pass
                else:
                    run = False
               

    def read_markers(self):
        for i, j in enumerate(self.frame):
                self.infoMarkers[i] = cv.aruco.detectMarkers(j, app.DICTIONARY, parameters = app.PARAMETERS)


    def draw_axe(self):
        #si markers detect  vecteur de translation et rotation 
        for i in self.infoMarkers:
            for j in i[0]:
                (rvecs, tvecs, markerPoints) = cv.aruco.estimatePoseSingleMarkers(j, app.MARKER_EDGE, app.CAMERA_MATRIX, app.DIST_COEFFS)
                for k, l in enumerate(self.frame):
                    self.frame[k] = cv.aruco.drawAxis(l, app.CAMERA_MATRIX, app.DIST_COEFFS, rvecs, tvecs, 0.10)
    def draw_windows(self):
        for i in self.frame:
            for j in range(len(self.frame)):
               cv.imshow("cam" + str(j), i)
    def calcul_dist2(self, id_cam):
        '''
        calcule la distance entre deux tag
        '''
        if self.infoMarkers[id_cam][1] is None:
            return 0
        elif len(self.infoMarkers[id_cam][0]) < 2:
            return 0
        pos = []
        for corner in self.infoMarkers[id_cam][0:2][0]:
            (rvecs, tvecs, markerPoints) = cv.aruco.estimatePoseSingleMarkers(corner, app.MARKER_EDGE, app.CAMERA_MATRIX, app.DIST_COEFFS)

            pos.append(vector2(tvecs[0][0][0], tvecs[0][0][1]))
        return (pos[0] - pos[1]).norme()


    def calcul_dist3_list(self, id_cam):
        '''
        calcule la distance entre deux tag
        '''
        
        if self.infoMarkers[id_cam][1] is None:
            return 0
        elif len(self.infoMarkers[id_cam][0]) < 2:
            return 0
        pos = []
        for corner in self.infoMarkers[id_cam][0:2][0]:
            (rvecs, tvecs, markerPoints) = cv.aruco.estimatePoseSingleMarkers(corner, app.MARKER_EDGE, app.CAMERA_MATRIX, app.DIST_COEFFS)

            pos.append(vector3(tvecs[0][0][0], tvecs[0][0][1], tvecs[0][0][2]))
        return (pos[0] - pos[1]).norme()

    def calcul_dist3(self, id_cam, id_tag1, id_tag2):
        '''
        calcule la distance entre deux tag choisi par le id_tag
        '''
        pos = self.calcul_vect3(id_cam)

        if not ((id_tag1 in pos) and (id_tag2 in pos)):
            return 0

        return (pos[id_tag1] - pos[id_tag2]).norme()

    def calcul_vect3(self, id_cam):
        if self.infoMarkers[id_cam][1] is None:
            return {}
        else:
            pos = {}
            for i, id_mark in enumerate(self.infoMarkers[id_cam][1]):
                    corner = self.infoMarkers[id_cam][0][i]
                    (rvecs, tvecs, markerPoints) = cv.aruco.estimatePoseSingleMarkers(corner, app.MARKER_EDGE, app.CAMERA_MATRIX, app.DIST_COEFFS)

                    pos[str(int(id_mark))] = vector3(tvecs[0][0][0], tvecs[0][0][1], tvecs[0][0][2])
        
            return pos

            
    def update(self) :
        self.read_frame()
        self.enleve_couleur()
        self.read_markers()
        print(round(100 * self.calcul_dist3_list(0), 2), "cm")
        # print(round(100 * self.calcul_dist3(0, "2", "3"), 2), "cm")
        if self.axe:
            self.draw_axe()
        if self.windows:
            self.draw_windows()


class app():
    PROCESSOR = platform.processor()
    PARAMETERS = cv.aruco.DetectorParameters_create()
    DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
    MARKER_EDGE = 0.07
    #0.03
    CALIB_PATH = "SaveALL/myFi/"
    CAMERA_MATRIX = np.loadtxt(CALIB_PATH + 'cameraMatrix.txt', delimiter=',')
    DIST_COEFFS  = np.loadtxt(CALIB_PATH + 'cameraDistortion.txt', delimiter=',')
    def __init__(self):
        self.running = True
        if app.PROCESSOR != "x86_64":
            self.capture1 = []
            self.capture1.append(capture())
            #self.capture1.append(capture())
            self.capture1[0].idCam = 0
            #self.capture1[1].idCam = 1
            
        else:
            self.capture1 = []
            self.capture1.append(capture())
        self.img = imgProcess(self.capture1)

    def run(self):
        while self.running:
            self.update()
        self.img.release_all()
        cv.destroyAllWindows()
            
    def update(self):
        self.img.update()
            #------Pour quitter "q"---------
        if cv.waitKey(1) & 0xFF == ord('q'):
            self.img.release_all()
            self.running = False


class vector2():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def norme(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    def __add__(self, other):
        return vector2(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return vector2(self.x - other.x, self.y - other.y)
    def __str__(self):
        return f"({self.x}, {self.y})"


class vector3():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def norme(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
    def __add__(self, other):
        return vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self, other):
        return vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    def __str__(self):
        return f"vector3({self.x}, {self.y}, {self.z})"


def main():
    app1 = app()
    app1.run()

    
if __name__ == "__main__":
    main()