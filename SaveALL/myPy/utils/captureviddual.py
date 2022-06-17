import cv2 as cv
import numpy as np
import datetime
import time 
#modification d'un pipeline trouvé sur le net pour test de capture 
class capture :
    def __init__(self) :
        self.idCam=0
        self.capture_width=3264
        self.capture_height=2464
        self.display_width=3264
        self.display_height=2464
        self.framerate=5
        self.flip_method=0
    def setCap(self,w,h):
        self.display_width=w
        self.display_height=h
        self.capture_width=w
        self.capture_height=h
    def gstreamer_pipeline(self):
        return (
            "nvarguscamerasrc sensor_id=%d ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                self.idCam,
                self.capture_width,
                self.capture_height,
                self.framerate,
                self.flip_method,
                self.display_width,
                self.display_height,
            )
        )
if __name__ == "__main__":
    capture1=capture()
    capture2=capture()
    capture2.idCam=1
    img_cnt = 0 
    capture1.setCap(3264,2464)
    capture2.setCap(3840,2160)
    startime=datetime.datetime.now()
    print(startime)

    imgR = cv.VideoCapture(capture1.gstreamer_pipeline(),cv.CAP_GSTREAMER)
    imgL = cv.VideoCapture(capture2.gstreamer_pipeline(),cv.CAP_GSTREAMER)
    outR= cv.VideoWriter("OutR{}.avi".format(time.time()),cv.VideoWriter_fourcc("M","P","E","G"),5.0,(3840,2160))
    outL= cv.VideoWriter("OutL{}.avi".format(time.time()),cv.VideoWriter_fourcc("M","P","E","G"),5.0,(3264,2464))
    while True:
       
        ret,frame = imgL.read()
        ret,frame0=imgR.read()
        stoptime=datetime.datetime.now()
        a=stoptime-startime
        outR.write(frame)
        outL.write(frame0)
        if a.min == 45 :
                print("stopped")
                imgR.release()
                imgL.release()
                outR.release()
                outL.release()
                break

cv.destroyAllWindows()
    
