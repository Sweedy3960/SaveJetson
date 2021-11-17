import cv2 as cv 

img = cv.VideoCapture("http://192.168.1.2:4747/video")
while True :
    ret,frame = img.read()
    cv.imshow("that",frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
