import cv2 as cv
from cv2 import imshow
img=cv.imread("/images/q2mptest.png")
imshow("test",img)
class tag:
    def __init__(self,_id,_corns) -> None:
        self.id=_id
        self.corns=_corns

print(str(infomarker.count(1)))        
for i in infomarker:
    for j,k in enumerate(i[0]):
        ls.append(tag(k,i[1][j]))
    
print(ls)
for i in ls:
    print("n1")
    print(i.id)
    print(i.corns)