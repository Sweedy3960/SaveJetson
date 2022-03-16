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

igF = [42,17,17,10,10]
igHQ = [42,12,14,6,13,14,13,17,17,10,10]
corn=[[[100,100,110,0],[100,100,110,0],[100,100,110,0],[100,100,110,0]],[[100,100,110,0],[100,100,110,0],[100,100,110,0],[100,100,110,0]]]

filtered = filter(lambda score: score == ROBIGId.ROCK, igF)
for i,j in enumerate(igF):
    if j == ROBIGId.ROCK.value:
        print("a")
    if j == 17:
        print("b")
print(ROBIGId.ROCK.value)
print(igF.count(ROBIGId.ROCK.value))


print(igF.index(ROBIGId.ROCK.value))
igF.remove(10)
print(igF.index(10))
print((list(filtered)))
