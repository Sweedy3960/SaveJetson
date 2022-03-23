class Capture:
    ''' pipeline de capture video gstreamer
        résolution:
        3840x2160px,
        id de la caméra,
        orientation
    '''
    def __init__(self, _idCam):
        self.idCam = _idCam
        self.capture_width = 3840
        self.capture_height = 2160
        self.display_width = 3840
        self.display_height = 2160
        self.flip_method = 2

    def gstreamer_pipeline(self):
        return (
            "nvarguscamerasrc sensor_id=%d ! "

            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            #Possible modif de framerate si nécéssaire
            "format=(string)NV12, framerate=(fraction)15/1 !"
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                self.idCam,
                self.capture_width,
                self.capture_height,
                self.flip_method,
                self.display_width,
                self.display_height,
            )
        )
