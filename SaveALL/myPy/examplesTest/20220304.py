from enum import Enum
class ROBIGId(Enum):
    ROB0=1,
    ROB1=2,
    ROB2=3,
    ROB3=4,
    ROB4=5,
    ROB5=6,
    ROB6=7,
    ROB7=8,
    ROB8=9,
    ROB9=10,
    RED=47,
    BLUE=13,
    GREEN=36,
    ROCK=17,
    MIDL=42,

class TagIgSize(Enum):
    MARKER_ROBOT = 0.07
    MARKER_MIDL = 0.10
    MARKER_SAMPLE=0.05

ig = [42,10,10]
corn=[[[100,100,110,0],[100,100,110,0],[100,100,110,0],[100,100,110,0]],[[100,100,110,0],[100,100,110,0],[100,100,110,0],[100,100,110,0]]]

filtered = filter(lambda score: score == ROBIGId.ROCK, ig)
for i,j in enumerate(ig):
    if i == ROBIGId.ROCK:
        print("a")

print(ig.count(ROBIGId.ROCK))
print(ig.index(10))
ig.remove(10)
print(ig.index(10))
print((list(filtered)))
