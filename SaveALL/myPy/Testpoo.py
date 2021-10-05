import cv2 as cv
import numpy as np
class capture :
    def __init__(self) :
        self.capture_width=1680,
        self.capture_height=1050,
        self.display_width=500,
        self.display_height=500,
        self.framerate=10,
        self.flip_method=2,
    def gstreamer_pipeline(self):
        self.capture_width=1680
        self.capture_height=1050
        self.display_width=500
        self.display_height=500
        self.framerate=10
        self.flip_method=2
    def getvalue(self):
        self.capture_width=int(input("hauteur svp : "))
        self.capture_height=int(input("hauteur svp : "))
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
    