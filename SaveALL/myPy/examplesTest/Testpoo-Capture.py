import cv2 as cv
import numpy as np
import time

#modification d'un pipeline trouvé sur le net pour test de capture 
class capture :
    def __init__(self) :
        self.idCam=0
        self.capture_width=3264
        self.capture_height=2464
        self.display_width=500
        self.display_height=500
        self.framerate=20
        self.flip_method=0
    def setCap(self,w,h):
        self.display_width=w
        self.display_height=h
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
    imgR = cv.VideoCapture(capture1.gstreamer_pipeline(),cv.CAP_GSTREAMER)
    imgL = cv.VideoCapture(capture2.gstreamer_pipeline(),cv.CAP_GSTREAMER)
    while True:
       
        ret,frame = imgL.read()
        ret,frame0=imgR.read()
        cv.imshow("that",frame)
        cv.imshow("this",frame0)
        if cv.waitKey(1) & 0xFF == ord('p'):
            time.sleep(1)
            imgL.release()
            imgR.release()
            time.sleep(1)
            capture1.setCap(3840,2160)
            capture2.setCap(3840,2160)
            imgR = cv.VideoCapture(capture1.gstreamer_pipeline(),cv.CAP_GSTREAMER)
            imgL = cv.VideoCapture(capture2.gstreamer_pipeline(),cv.CAP_GSTREAMER)
            ret,frame = imgL.read()
            ret,frame0=imgR.read()
            png_name = "mesurecalibR{}.jpg".format(img_cnt)
            png_name0 = "mesurecalibL{}.jpg".format(img_cnt)
            cv.imwrite(png_name, frame)
            cv.imwrite(png_name0, frame0)

            print("{} written!".format(png_name))
            img_cnt+=1
            time.sleep(1)
            imgR.release()
            imgL.release()qqqqq
            time.sleep(1)
            capture1.setCap(500,500)
            capture2.setCap(500,500)
            imgR = cv.VideoCapture(capture1.gstreamer_pipeline(),cv.CAP_GSTREAMER)
            imgL = cv.VideoCapture(capture2.gstreamer_pipeline(),cv.CAP_GSTREAMER)

        if cv.waitKey(1) & 0xFF == ord('q'):
            imgR.release()
            imgL.release()
            break

cv.destroyAllWindows()
    