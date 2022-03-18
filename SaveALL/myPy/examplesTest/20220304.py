from enum import Enum
class ROBIGId(Enum):
    ROB0=1
    ROB1=2
    ROB2=3
    ROB3=4
    ROB4=5
    ROB5=6
    ROB6=7
    ROB7=8
    ROB8=9
    ROB9=10
    ROB=[0,1,2,3,4,5,6,7,8,9,10]
    RED=47
    BLUE=13
    GREEN=36
    ROCK=17
    MIDL=42

class TagIgSize(Enum):
    MARKER_ROBOT = 0.07
    MARKER_MIDL = 0.10
    MARKER_SAMPLE=0.05

igF = [42,1,4,47,13,47,36,13,17,17]
igHQ = [42,4,17,17,17,17,17,17,13,13,13,36,13,36,36]
corn=[[[100,100,110,0],[100,100,110,0],[100,100,110,0],[100,100,110,0]],[[100,100,110,0],[100,100,110,0],[100,100,110,0],[100,100,110,0]]]

filtered = filter(lambda score: score == 17, igF)
for i,j in enumerate(igF):
    if j == ROBIGId.ROCK.value:
        print("a")
    if j == 17:
        print("b")
nbRob=0
nbRock=0
nbRed=0
nbGreen=0
nbBlue=0
nbCenter=0
cam0=0
cam1=1
sorted=[]
tagin={}
pos=0
for i in igF:
        igHQ.insert(len(igHQ),i)
for i,j in enumerate(igHQ):

        for k,l in enumerate(ROBIGId.ROB.value):
            if j==k:
                nbRob+=1
                if nbCenter>1:
                    tagin["tag{}".format(l)] = "Tag(self.SortCorn(int(i),int(k)),self.ListId,int(l),int(k),cam0,l)"
                else:
                    tagin["tag{}".format(l)] = "Tag(self.SortCorn(int(i),int(k)),self.ListId,int(l),int(k),cam1,l)"
        if j == ROBIGId.GREEN.value:  
            nbGreen+=1
            if nbCenter>1:
                tagin["tag{}".format(j)+"_{}".format(nbGreen)] = "Tag(self.SortCorn(int(i),int(k)),self.ListId,int(l),int(k),cam0,nbGreen)"
            else:
                tagin["tag{}".format(j)+"_{}".format(nbGreen)] = "Tag(self.SortCorn(int(i),int(k)),self.ListId,int(l),int(k),cam1,nbGreen)"

        if j == ROBIGId.RED.value:  
            nbRed+=1
            if nbCenter>1:
                tagin["tag{}".format(j)+"_{}".format(nbRed)] = "Tag(self.SortCorn(int(i),int(k)),self.ListId,int(l),int(k),cam0,nbRed)"
            else:
                tagin["tag{}".format(j)+"_{}".format(nbRed)] = "Tag(self.SortCorn(int(i),int(k)),self.ListId,int(l),int(k),cam1,nbRed)"
                
        if j == ROBIGId.BLUE.value:  
            nbBlue+=1
            if nbCenter>1:
                tagin["tag{}".format(j)+"_{}".format(nbBlue)] = "Tag(self.SortCorn(int(i),int(k)),self.ListId,int(l),int(k),cam0,nbBlue)"
            else:
                tagin["tag{}".format(j)+"_{}".format(nbBlue)] = "Tag(self.SortCorn(int(i),int(k)),self.ListId,int(l),int(k),cam1,nbBlue)"
                
        if j == ROBIGId.ROCK.value:  
            nbRock+=1  
            if nbCenter>1:
                tagin["tag{}".format(j)+"_{}".format(nbRock)] = "Tag(self.SortCorn(int(i),int(k)),self.ListId,int(l),int(k),cam0,nbRock)"
            else:
                tagin["tag{}".format(j)+"_{}".format(nbRock)] = "Tag(self.SortCorn(int(i),int(k)),self.ListId,int(l),int(k),cam1,nbRock)"
                 
        if j == ROBIGId.MIDL.value:
            nbCenter+=1
        



print(nbRob)
print(tagin)
print(ROBIGId.ROB.value)
print(type(ROBIGId.ROB.value))
print(igF.count(ROBIGId.ROCK.value))
print(igF.index(ROBIGId.ROCK.value))
igF.remove(ROBIGId.ROCK.value)
print(igF.index(ROBIGId.ROCK.value))
print((list(filtered)))
def assemblist(self):
    for i in igF:
        igHQ.insert(len(igHQ),i)
