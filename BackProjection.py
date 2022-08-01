import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
from alive_progress import alive_bar
from Configuration import SCAN_COUNT, SPEED_OF_LIGHT, RANGE_RESOLUTION, CROSS_RANGE_RESOLUTION, PLATFORM_POS, COORDINATES, SCAN_RES, USER

filePath=""
#read datalist from pickle file
if USER == 'k':
    filePath = "/Users/kianchen/Desktop/BeaverWorks/team5/datalist.pkl"
elif USER == 'am':
    filePath = "/Users/zxiao23/Desktop/BWSISummer/team5/datalist.pkl"
elif USER == 'r':
    filePath = "/Users/rishita/bwsi22/team5/datalist.pkl"
elif USER == 'g':
    filePath = r"C:\Users\gheat\Documents\GitHub\team5\datalist.pkl"
else:
    filePath = r"\Users\xiaoz\Documents\BWSISummer\team5\datalist.pkl"

datalist = pkl.load(open(filePath, "rb"))

fileName = input("Which file are you back projecting?: ")

def readPlatformPos(filepath):
    data = pkl.load(open(filepath, "rb"))
    platformPos = data['platform_pos']
    return platformPos

def paintImage(datalist, platformPos, xCor, yCor, zOffset = 0):
    numX = len(xCor)
    numY = len(yCor)
    image = np.zeros((numX, numY))
    with alive_bar(SCAN_COUNT) as bar:
        for scan in range(SCAN_COUNT):
            xNP = np.asarray((xCor[:] - platformPos[scan][0])**2)
            yNP = np.asarray((yCor[:] - platformPos[scan][1])**2)
            temp = np.zeros((numX, numY))
            temp = xNP[np.newaxis,:] + yNP[:, np.newaxis]
            temp = np.sqrt(temp+(zOffset - platformPos[scan][2])**2) * 2e12 / SPEED_OF_LIGHT / (SCAN_RES*1.907)
            #closestIndex = np.array(2*np.sqrt((xCor[:] - platformPos[scan][0])**2 + (yCor[:] - platformPos[scan][1])**2 + (zOffset - platformPos[scan][2])**2) * 1e12 / SPEED_OF_LIGHT / 61)
            image[:] += datalist[scan][np.minimum(temp, np.full((numX,numY),len(datalist[0])-1)).astype(int)]
            bar()
    print(image)
    print(np.shape(image))
    return image

xPos = np.arange(COORDINATES[0],COORDINATES[1],CROSS_RANGE_RESOLUTION)
yPos = np.arange(COORDINATES[2],COORDINATES[3],RANGE_RESOLUTION)

plt.imshow(paintImage(datalist, readPlatformPos(PLATFORM_POS), xPos, yPos), cmap='gray', origin='lower', extent=COORDINATES)
plt.colorbar()
plt.xlabel("x-axis (meters/"+str((COORDINATES[1]-COORDINATES[0])/RANGE_RESOLUTION)+" pixels)")
plt.ylabel("y-axis (meters/"+str((COORDINATES[3]-COORDINATES[2])/CROSS_RANGE_RESOLUTION)+" pixels)")
plt.title(fileName)
plt.show()