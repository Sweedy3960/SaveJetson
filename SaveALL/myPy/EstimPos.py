import cv2 as cv 
import numpy as np 
class capture:
    def __init__(self):
        self.capture_width=3264,
        self.capture_height=2640,
        self.display_width=3264,
        self.display_height=2640,
        self.flip_method=2,

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
class ImgWork:
    def __init__(self):
        self.Result = []
        self.DEBUG =False
    def detect(self):
        self.result = cv.aruco.detectMarkers(self.frame,self.DICTIONARY,parameters = self.PARAMETERS)
    def assignat (self):
        self.corners = self.result[0]
        self.ids = self.result[1]

    def Draw(self):
        if self.DEBUG != False:
            for i in self.cap:
                self.frame[i] = cv.aruco.drawDetectedMarkers(self.frame[i],self.corners,self.ids)

class app : 
    def __init__(self):
        self.idCam = 0
        self.cap = []
        self.frame = []
    
        self.ret= 0
        self.PARAMETERS = cv.aruco.DetectorParameters_create()
        self.DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
        self.isRunning = 0
    def createList(self):
        for i in self.cap:
            self.frame.append(None)
    def assigncap(self):
        for i in self.idCam:
            self.cap.append(None)
    def readCap(self):
        for i in self.cap :
            self.ret,self.frame[i]=cv.self.cap[i].read()
    def update(self):
        self.readCap()

    def main (self):
        self.createList()
        while isRunning == True :
            self.update()

