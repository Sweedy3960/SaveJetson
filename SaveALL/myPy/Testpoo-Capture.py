import cv2 as cv
import numpy as np
import time

#modification d'un pipeline trouvé sur le net pour test de capture 
class capture :
    def __init__(self) :
        self.capture_width=3264
        self.capture_height=2464
        self.display_width=500
        self.display_height=500
        self.framerate=10
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
    img_cnt = 0 
    img = cv.VideoCapture(capture1.gstreamer_pipeline(),cv.CAP_GSTREAMER)
    while True:
       
        ret,frame = img.read()
        cv.imshow("that",frame)
        if cv.waitKey(1) & 0xFF == ord('p'):
            time.sleep(0.1)
            img.release()
            time.sleep(0.1)
            capture1.setCap(3264,2464)
            img = cv.VideoCapture(capture1.gstreamer_pipeline(),cv.CAP_GSTREAMER)
            ret,frame = img.read()
            png_name = "map2nd{}.bmp".format(img_cnt)
            cv.imwrite(png_name, frame)
            print("{} written!".format(png_name))
            img_cnt+=1
            time.sleep(0.1)
            img.release()
            time.sleep(0.1)
            capture1.setCap(500,500)
            img = cv.VideoCapture(capture1.gstreamer_pipeline(),cv.CAP_GSTREAMER)

        if cv.waitKey(1) & 0xFF == ord('q'):
         img.release()
         break

cv.destroyAllWindows()
    