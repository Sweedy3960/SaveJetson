
import numpy as np
import cv2
import sys
calib_path="SaveALL/myFi/"

# You should replace these 3 lines with the output in calibration step
DIM=(1632, 1232)
K=np.loadtxt(calib_path+'intrinsic_matrix500x500.txt', delimiter=',')
D= np.loadtxt(calib_path+'distortion_matrix500x500.txt', delimiter=',')
def undistort(img_path):
    img = cv2.imread(img_path)
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imwrite("undistorted.jpg", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__':
        undistort("SaveALL/myPy/te.jpg")