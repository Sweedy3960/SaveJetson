import numpy as np
#Pas de float dans range 
for i in range(1,11,1):
	print(i)
	print("petit pas")
print("STOP")

for i in np.arange(0,5.1,.8):
	print(i)
print("avec numpy")
#StartStopSteps
for i in np.linspace(1,10,5):
	print(i)
print("avec linspace")
