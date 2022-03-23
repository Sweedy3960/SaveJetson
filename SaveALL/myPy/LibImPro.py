
class ImProc:

    def __init__(self, cap: list):
        self.frame = []
        self.gray = []
        self.infoMarkers = []
        self.cap = []
        self.ListId = []
        self.tagin = []
        self.planMrot = []
        self.planTvec = []
        self.planptsimg = []
        self.WcoinsTable = [(0, 0, 0), (0, 2000, 0),
                            (3000, 2000, 0), (3000, 0, 0)]
        self.CcoinsTable = []
        for i in cap:
            self.frame.append(None)
            self.cap.append(cv.VideoCapture(
                i.gstreamer_pipeline(), cv.CAP_GSTREAMER))
            self.infoMarkers.append(None)
            self.ListId.append([])
            self.gray.append(None)

    def __del__(self):
        """
        déconstructeur:
        si intruption quelconque fermeture des pipeline
        pour évité la surchage de pipeline ouvers ou cas ou mauvais arret de l'app 
        """
        print("coucou je deconstruit")
        self.Release_All()

    def ReadFrames(self):
        for i, j in enumerate(self.cap):
            ret, self.frame[i] = j.read()

    def ToGray(self):
        for i, j in enumerate(self.frame):
            self.gray[i] = cv.cvtColor(j, cv.COLOR_BGR2GRAY)

    def Detect(self):
        for i, j in enumerate(self.gray):
            self.infoMarkers[i] = cv.aruco.detectMarkers(
                j, App.DICTIONARY, parameters=App.PARAMETERS)
            try:
                if self.infoMarkers[i][1] == None:
                    return 0
            except:
                return 1

    def SortName(self):
        for i, j in enumerate(self.infoMarkers):
            self.ListId[i].clear()
            for l, k in enumerate(self.infoMarkers[i][1]):
                a = (str(self.infoMarkers[i][1][l]).replace("[", ""))
                a = a.replace("]", "")
                self.ListId[i].append(int(a))

    def SortCorn(self, listcam: int, posList: int):
        return (self.infoMarkers[listcam][0][posList])

    def TriTag(self):
        for i in self.infoMarkers:
            for j,k in enumerate(i[0]):
                self.tagin.append(Tag(k,i[1][j]))
        return self.tagin

    def Getplan(self):
        rvec = []
        tvec = []
        for i in range(App.NB_CAM):
            rvec.append(None)
            tvec.append(None)
            ret, rvec[i], tvec[i] = cv.solvePnP(
                App.W_Center, self.tagin["tag42_{}".format(i)].corners, App.MAT[i], App.DIST[i])
        return [rvec, tvec]

    def projecttablepoint(self):
        a = self.Getplan()
        for i, j in enumerate(a[0]):
            self.planMrot[i], _ = cv.Rodrigues(j[i])
            self.planTvec[i] = a[1][i].ravel().reshape(3)
            ########################################
        for i in self.WcoinsTable:
            self.planptsimg, _ = cv.projectPoints(
                i, self.planMrot, self.planTvec, App.CAMERA_MATRIX, App.DIST_COEFFS)
            b = self.planptsimg[0][0][0]
            c = self.planptsimg[0][0][1]
            z = self.gray[0]
            z = cv.circle(z, (int(b), int(c)), 2, (255, 0, 0),
                          thickness=3, lineType=cv.FILLED)
            z = cv.putText(z, str(i), (int(b), int(
                c)), fontFace=cv.FONT_HERSHEY_DUPLEX, fontScale=3.0, color=(125, 245, 55), thickness=3)
            self.CcoinsTable.append(b, c)

    def recherchecentreTag(self, plantimg, centrepix, Mrot, Tvec):
        foundx = False
        foundy = False
        #coordonée dans img
        cx = int(centrepix[0])
        cy = int(centrepix[1])
        #position fixtive dans limage
        x0 = 0
        y0 = 0
        #coordonée irl
        xw = 0
        yw = 0
        zw = 0
        while foundx == False or foundy == False:
            a, _ = cv.projectPoints(
                (xw, yw, zw), self.planMrot, self.planTvec, App.CAMERA_MATRIX, App.DIST_COEFFS)
            x0 = a[0][0][0]
            y0 = a[0][0][1]

            if x0 > (cx-2) and x0 < (cx+2):
                if self.DebugPRojection:
                    print("foundx")
                foundx = True
            elif x0 > cx:
                xw = xw-1
            else:
                xw = xw+1

            if y0 > (cy-2) and y0 < (cy+2):
                foundy = True
                if self.DebugPRojection:
                    print("foundy")
            elif y0 > cy:
                yw = yw-1
            else:
                yw = yw+1
                if self.DebugPRojection:
                    print([x0, y0])
                    print(cx, cy)
                    print([xw, yw])
        return[xw, yw]

    def Release_All(self):
        for i in self.cap:
            i.release()
            self.out.release()

    def TagWork(self):
        self.SortName()
        self.TriTag()
        self.projecttablepoint()
        b = list(self.tagin.keys())
        b.remove("tag42_{}".format(*))
        b.remove("tag42_1")
        for i in b:
            a = self.recherchecentreTag(
                self.planptsimg, self.tagin[i].centrepix, self.planMrot, self.planTvec)
            print(a)
            self.tagin[i].irlcord = a
            print(self.tagin[i].Id, self.tagin[i].irlcord)

    def FrameWorking(self):
        self.ToGray()

    def Update(self):
        self.ReadFrames()
        self.FrameWorking()
        if self.Detect():
            self.TagWork()