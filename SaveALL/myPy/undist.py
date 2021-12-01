
import numpy as np
import cv2
import sys
calib_path="/home/cpnv/Documents/SaveJetson/SaveALL/myFi/"

# You should replace these 3 lines with the output in calibration step

K= np.loadtxt(calib_path+'intrinsic30.11.txt', delimiter=',')
D= np.loadtxt(calib_path+'calib30.11.txt', delimiter=',')

def undistort():
    balance =1 
    dim2=None 
    dim3=None
    DIM=(3264,2464)
    img = cv2.imread("/home/cpnv/Documents/SaveJetson/map2nd.bmp",1)
    dim1 = img.shape[:2][::-1]  #dim1 is the dimension of input image to un-distort
    print(dim1)
    print(DIM)
    assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1
    scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
    scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0
        # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_32FC1)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

    cv2.imwrite("undistorted30.11.bmp", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__':
        undistort()