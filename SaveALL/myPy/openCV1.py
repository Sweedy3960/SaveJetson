dispH = 500
dispW = 500 
flip = 2
#Utilisation du programme gstreamer 
camset=camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
#Création d'un objet camera
cam = cv.VideoCapture(camset)
while True :
    #Prise d'une frame
    ret,frame = cam.read()
    #montre la frame dans une fenetre
    cv.imshow("that",frame)
    #attend1ms pour savoir si quit 
    if cv.waitKey(1) == ord("q"):
        break
#Libère la caméra
cam.release()
#détruit les fenetres
cv.destroyAllWindows()