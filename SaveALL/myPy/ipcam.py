import cv2 as cv 

img = cv.VideoCapture("https://192.168.1.5:4343/video")
while True :
    ret,frame = img.read()
    cv.imshow("that",frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
