from dataclasses import dataclass
from fileinput import filename
import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
from alive_progress import alive_bar
from Configuration import COORDINATES, CROSS_RANGE_RESOLUTION, RANGE_RESOLUTION, USER, USER_SYSTEM

#change this to local file
filePath = ""
if USER == 'k':
    filePath = "/Users/kianchen/Desktop/BeaverWorks/emulator/input/"
elif USER == 'am':
    filePath = "/Users/zxiao23/Desktop/BWSISummer/emulator/input/"
elif USER == 'r':
    filePath = "/Users/rishita/bwsi22/emulator/input/"
elif USER == 'g':
    filePath = r"C:\Users\gheat\Documents\GitHub\emulator\input\\"
elif USER == 'aw':
    filePath = r"\Users\xiaoz\Documents\BWSISummer\emulator\input\\"
else:
    filePath = input("Please enter your path to the source folder of the data: ")
    if USER_SYSTEM == 'w':
        filePath = repr(filePath)

fileName = "marathon_"+ input('Enter the file number: ') + ".pkl"
data = pkl.load(open(filePath + fileName, "rb"))

datalist = data['scan_data']
platformPos = data['platform_pos']
rangeBins = data['range_bins']
SCAN_COUNT = len(data['scan_data'])

def paintImage(datalist, rangeBins, platformPos, xCor, yCor, zOffset = 0):
    numX = len(xCor)
    numY = len(yCor)
    image = np.zeros((numX, numY),dtype='complex128')
    with alive_bar(SCAN_COUNT) as bar:
        for scan in range(SCAN_COUNT):
            xNP = np.asarray((xCor[:] - platformPos[scan][0])**2)
            yNP = np.asarray((yCor[:] - platformPos[scan][1])**2)
            distance = np.zeros((numX, numY))
            distance = xNP[np.newaxis,:] + yNP[:, np.newaxis]
            distance = np.sqrt(distance+(zOffset - platformPos[scan][2])**2)
            #needs to change temp = np.sqrt(temp+(zOffset - platformPos[scan][2])**2) * 2e12 / SPEED_OF_LIGHT / (SCAN_RES*1.907)
            #closestIndex = np.array(2*np.sqrt((xCor[:] - platformPos[scan][0])**2 + (yCor[:] - platformPos[scan][1])**2 + (zOffset - platformPos[scan][2])**2) * 1e12 / SPEED_OF_LIGHT / 61)
            #image[:] += datalist[scan][np.argmin(np.abs(distance - rangeBins))]
            temp = np.interp(distance, rangeBins, datalist[scan])
            image += temp
            bar()
    print(np.shape(image))
    return np.abs(image)

xPos = np.arange(COORDINATES[0],COORDINATES[1],CROSS_RANGE_RESOLUTION)
yPos = np.arange(COORDINATES[2],COORDINATES[3],RANGE_RESOLUTION)

plt.imshow(paintImage(datalist, rangeBins, platformPos, xPos, yPos), cmap='gray', origin='lower', extent=COORDINATES)
plt.colorbar()
plt.xlabel("x-axis (meters/"+str((COORDINATES[1]-COORDINATES[0])/RANGE_RESOLUTION)+" pixels)")
plt.ylabel("y-axis (meters/"+str((COORDINATES[3]-COORDINATES[2])/CROSS_RANGE_RESOLUTION)+" pixels)")
plt.title(fileName)
plt.show()