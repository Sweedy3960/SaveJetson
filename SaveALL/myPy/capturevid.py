import cv2 as cv 
import numpy as np 

class capture :
    def __init__(self) :
        self.capture_width=3264
        self.capture_height=2464
        self.display_width=3264
        self.display_height=2464
        self.framerate=2
        self.flip_method=2
    def setCap(self,w,h):
        self.display_width=w
        self.display_height=h
    def gstreamer_pipeline(self):
        return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=  %d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
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
    img_cnt = 0 
    img = cv.VideoCapture(capture1.gstreamer_pipeline(),cv.CAP_GSTREAMER)
    out= cv.VideoWriter("out0.avi",cv.VideoWriter_fourcc(*"MJPG"),10.0,(3264,2464))
    while True:
        ret,frame = img.read()
        if ret==True:
            out.write(frame)
            cv.imshow("frame",frame)
            if cv.waitKey(1)&0xFF==ord('q'):
                break
    img.release()
    out.release()
    cv.destroyAllWindows() 