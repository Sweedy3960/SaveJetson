import cv2 as cv

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

infomarker=[[[6,4,42],["c1","c2"]],[[42,13,4],["c1","c2"]]]
class tag:
    def __init__(self,_id,_corns,_cam) -> None:
        self.id=_id
        self.corns=_corns
        self.cam=_cam
ls={}
'''
for i in infomarker:
    for j in i[0]:
        ls.append(None)
        '''
new=[infomarker[0][0]+(infomarker[0][0]),[infomarker[0][1]+(infomarker[0][1])]]
<<<<<<< HEAD
'''
=======

>>>>>>> local
print(new) 
def tri():
    for i in infomarker:
        for j,k in enumerate(i[0]):
<<<<<<< HEAD
=======
        
>>>>>>> local
            ls[str(k)+"_"+str(i)]=tag(k,i[1][j],i)
      
tri()

<<<<<<< HEAD
'''
=======

>>>>>>> local
print(ls)
'''
for i in ls:
    print("n1")
    print(i.id)
    print(i.corns)
if 2 in IgId.ROB:
    print("2yest")
'''