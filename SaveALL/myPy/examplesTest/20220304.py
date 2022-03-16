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
    RED=47
    BLUE=13
    GREEN=36
    ROCK=17
    MIDL=42

class TagIgSize(Enum):
    MARKER_ROBOT = 0.07
    MARKER_MIDL = 0.10
    MARKER_SAMPLE=0.05

IG = [42,10,8,9,7,1,3,17,17,36,17,13,13,17]
corn=[[100,100,110,0],]
filtered = filter(lambda score: score == ROBIGId.ROCK, IG)
for i,j in enumerate(IG):
    if i == ROBIGId.ROCK:
        print("a")

print(IG.count(ROBIGId.ROCK))
print(IG.index(17))
IG.remove(17)
print(IG.index(17))
print((list(filtered)))
