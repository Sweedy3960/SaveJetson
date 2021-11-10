import cv2 as cv
import numpy as np
import time
import glob
img_cnt = 0 


# =========================================
# Calculate fisheye calibration from images
# OpenCV expects number of interior vertices in the checkerboard,
# not number of squares. Let's adjust for that.
vtxCount = [9,6]

# -------------------------------------------------
# Determine checkerboard coordinates in image space
while True:
    imgSize = None
    corners2D = []
    images = glob.glob('*.jpg')
    for imgName in images:
        print(imgName)
        # Load input image and do some sanity check
        img = cv.imread(imgName)
        curImgSize = (img.shape[1], img.shape[0])
    
        if imgSize == None:
            imgSize = curImgSize
        elif imgSize != curImgSize:
            exit("All images must have the same size")
    
        # Find the checkerboard pattern on the image, saving the 2D
        # coordinates of checkerboard vertices in cbVertices.
        # Vertex is the point where 4 squares (2 white and 2 black) meet.
        found, corners = cv.findChessboardCorners(img, tuple(vtxCount), flags=cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE)
        if found:
            # Needs to perform further corner refinement?
            corners2D.append(corners)
        else:
            exit("Warning: checkerboard pattern not found in image {}".format(imgName))
    
    # Create the vector that stores 3D coordinates for each checkerboard pattern on a space
    # where X and Y are orthogonal and run along the checkerboard sides, and Z==0 in all points on
    # checkerboard.
    cbCorners = np.zeros((1, vtxCount[0]*vtxCount[1], 3))
    cbCorners[0,:,:2] = np.mgrid[0:vtxCount[0], 0:vtxCount[1]].T.reshape(-1,2)
    corners3D = [cbCorners.reshape(-1,1,3) for i in range(len(corners2D))]
    
    # ---------------------------------------------
    # Calculate fisheye lens calibration parameters
    camMatrix = np.eye(3)
    coeffs = np.zeros((4,))
    rms, camMatrix, coeffs, rvecs, tvecs = cv.fisheye.calibrate(corners3D, corners2D, imgSize, camMatrix, coeffs, flags=cv.fisheye.CALIB_FIX_SKEW)
    
    # Print out calibration results
    print("rms error: {}".format(rms))
    print("Fisheye coefficients: {}".format(coeffs))
    print("Camera matrix:")
    print(camMatrix)
    #----------------------------------------------------------
    def gstreamer_pipeline(
        capture_width=1632 ,
        capture_height=1232,
        display_width=500,
        display_height=500,
        framerate=10,
        flip_method=2,
    ):
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
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
        )
  
    img = cv.VideoCapture(gstreamer_pipeline(flip_method=2), cv.CAP_GSTREAMER)
    if rms >10:
        cap=True
    else:
        cap =False  
    while cap == True: 
        ret,frame = img.read()
        cv.imshow("that",frame)
        if cv.waitKey(1) & 0xFF == ord('p'):
            time.sleep(0.1)
            img.release()
            time.sleep(0.1)
            img = cv.VideoCapture(gstreamer_pipeline(display_width=1632,display_height=1232),cv.CAP_GSTREAMER)
            ret,frame = img.read()
            png_name = "AD_ed_{}.jpg".format(img_cnt)
            cv.imwrite(png_name, frame)
            print("{} written!".format(png_name))
            img_cnt+=1
            time.sleep(0.1)
            img.release()
            time.sleep(0.1)
            img = cv.VideoCapture(gstreamer_pipeline(display_width=500,display_height=500),cv.CAP_GSTREAMER)
        if cv.waitKey(1) & 0xFF == ord('c'):
            img.release()
            cap=False

        if cv.waitKey(1) & 0xFF == ord('q'):
            img.release()
            break
    
        