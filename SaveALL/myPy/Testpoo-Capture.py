import cv2 as cv
import numpy as np

#modification d'un pipeline trouvé sur le net pour test de capture 
class capture :
    def __init__(self) :
        self.capture_width=1640
        self.capture_height=1232
        self.display_width=1640
        self.display_height=1232
        self.framerate=10
        self.flip_method=2
    def setDisp(self):
        self.disp_width =500
        self.disp_height = 500
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
    cap=[]
    img=[]
    cap.append(capture())
    cap.append(capture())
    img_cnt = 0 
    cap[0].setDisp()
    img.append(cv.VideoCapture(cap[0].gstreamer_pipeline(),cv.CAP_GSTREAMER))
    img.append(cv.VideoCapture(cap[1].gstreamer_pipeline(),cv.CAP_GSTREAMER))
    while True:
       
        ret,frame = img[1].read()
        ret1,frame1 = img[0].read()
        cv.imshow("that",frame1)
        if cv.waitKey(1) & 0xFF == ord('p'):
            png_name = "left_{}.jpg".format(img_cnt)
            cv.imwrite(png_name, frame)
            print("{} written!".format(png_name))
            img_cnt+=1
            

        if cv.waitKey(1) & 0xFF == ord('q'):
         img[0].release()
         img[1].release()
         break

cv.destroyAllWindows()
    