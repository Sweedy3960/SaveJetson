# import the necessary packages
import numpy as np
import argparse
import cv2

def order_points(pts):
	rect = np.zeros((4, 2), dtype = "float32")
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	# return the ordered coordinates
	return rect
def four_point_transform(image, pts):
    	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	# return the warped image
	return warped

L=3264
H=2464
rendu=[]
image = cv2.imread("/home/cpnv/Images/left_0.jpg")
pts = [np.array(eval("[(0,0),(10,1632),(1632,1232),(1232,0)]"), dtype = "float32"),np.array(eval("[(1632,0),(0,3624),(3624,1232),(1632,1232)]"), dtype = "float32"),np.array(eval("[(1632,1232),(1232,3264),(3264,2464),(1632,2464)]"), dtype = "float32"),np.array(eval("[(1632,1232),(1232,3264),(0,2464),(0,1232)]"), dtype = "float32")]
# apply the four point tranform to obtain a "birds eye view" of
# the image
for i in pts:
	warped=four_point_transform(image, i)
	rendu.append(warped)
# show the original and warped images
cv2.imshow("Original", image)

for i in rendu :
	cv2.imshow("Warped%d" %int(rendu.index(i)),i)
#cv2.imwrite("Wrapped1D.bmp",warped)
cv2.waitKey(0)