import cv2 as cv
import numpy as np
#modification d'un pipeline trouvé sur le net pour test de capture 
class capture :
    def __init__(self) :
        self.capture_width=1680,
        self.capture_height=1050,
        self.display_width=500,
        self.display_height=500,
        self.framerate=10,
        self.flip_method=2,
    def setCap(self):
        self.capture_width=int(input("Largeur en pixels SVP :"))
        self.capture_height=int(input("hauteur en pixels SVP :"))
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
    while True:
        mod = input("voullez vous modifier les dimensions de capture? y/n")
        if mod == "y":
            capture1.setCap(capture1)
        rdy = input("Voullez vous enregistrer une image ? y/n")
        if rdy == "y":
            img = cv.VideoCapture(capture1.gstreamer_pipeline(capture1),cv.CAP_GSTREAMER)
            ret,frame = img.read()
            #DEBUG/VISUAL
            #cv.imshow("test", frame)
            png_name = "opencv_frame_{}.png".format(img_cnt)
            cv.imwrite(png_name, frame)
            print("{} written!".format(png_name))
            img_cnt+=1
        #------Pour quitter "q"---------
        if cv.waitKey(1) & 0xFF == ord('q'):
         break

cv.destroyAllWindows()
    