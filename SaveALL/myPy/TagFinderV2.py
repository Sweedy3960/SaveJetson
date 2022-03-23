import enum
import string
import numpy as np
import cv2 as cv
import libCap as cap
import LibImPro as im

class IgId():
    '''Tag in game, tag possible d'être perçus par l'app d'uanrt le match'''
    ROB0 = 1
    ROB1 = 2
    ROB2 = 3
    ROB3 = 4
    ROB4 = 5
    ROB5 = 6
    ROB6 = 7
    ROB7 = 8
    ROB8 = 9
    ROB9 = 10
    ROB = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    RED = 47
    BLUE = 13
    GREEN = 36
    ROCK = 17
    MIDL = 42


class TagIgSize():
    MARKER_ROBOT = 0.07
    MARKER_MIDL = 0.10
    MARKER_SAMPLE = 0.05


class App:
    #création des paramètre nécéssaires à la détéction
    PARAMETERS = cv.aruco.DetectorParameters_create()
    DICTIONARY = cv.aruco.Dictionary_get(cv.aruco.DICT_4X4_100)
    NB_CAM = 2
    #Position [W]ordl des coins du tag du centre
    W_Center = np.array([(1450, 1200, 530), (1550, 1200, 530),
                        (1550, 1300, 530), (1450, 1300, 530)], dtype="double")
    #Chemins d'accès au fichier de calibration (modifie si nécéssaire)
    CALIB_PATH = "SaveALL/myFi/"
    CAMERA_MATRIX_HQ = np.loadtxt(CALIB_PATH+'cam12matvid.txt', delimiter=',')
    DIST_COEFFS_HQ = np.loadtxt(CALIB_PATH+'cam12distvid.txt', delimiter=',')
    CAMERA_MATRIX_FI = np.loadtxt(CALIB_PATH+'FishMat.txt', delimiter=',')
    DIST_COEFFS_FI = np.loadtxt(CALIB_PATH+'FishDist.txt', delimiter=',')
    MAT = [CAMERA_MATRIX_HQ, CAMERA_MATRIX_FI]
    DIST = [DIST_COEFFS_HQ, DIST_COEFFS_FI]

    def __init__(self) -> None:

        self.capture1 = []
        for i in App.NB_CAM:
            self.capture1.append(cap.Capture(i))
        self.img = im.ImProc(self.capture1)
        self.run = True

    def main(self) -> None:
        while self.run:
            self.Update()
        self.img.Release_All()
        cv.destroyAllWindows()

    def Update(self) -> None:
        self.img.Update()
        #------Pour quitter "q"---------
        if cv.waitKey(1) & 0xFF == ord('q'):
            self.img.Release_All()
            self.running = False





class Tag:
    def __init__(self,):
        self.posRe = (0, 0)
        self.Facing = 0
        self.Id = whoami
        self.tvecs = None
        self.rvecs = None
        self.mat_rota = None
        self.corners = corners
        self.centrepix = [int(((corners[0][0][0]+corners[0][1][0]+corners[0][2][0]+corners[0][3][0])*0.25)),
                          int(((corners[0][0][1]+corners[0][1][1]+corners[0][2][1]+corners[0][3][1])*0.25))]
        self.irlcord = (0, 0)
        self.debug = False
        self.edge = taille

        if self.Id == App.MIDL:
            self.posRe = (1450, 1200)
            self.marker_edge = App.MARKER_MIDL
        elif whoami == App.ROBOTS_T:
            self.marker_edge = App.MARKER_EDGE
        else:
            self.marker_edge = App.MARKER_EDGE
        self.update()

    def FindV(self):
        self.rvecs, self.tvecs, markerPoints = cv.aruco.estimatePoseSingleMarkers(
            self.corners, self.marker_edge, App.CAMERA_MATRIX, App.DIST_COEFFS)

    def update(self):
        self.FindV()


def main() -> string:
    app1 = App()
    app1.main()
    sys.exit(0)

    return 0


if __name__ == "__main__":
    main()
