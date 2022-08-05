import os
import numpy as np
import pickle as pkl
import matplotlib.pyplot as plt
from alive_progress import alive_bar
from Configuration import COORDINATES, CROSS_RANGE_RESOLUTION, RANGE_RESOLUTION, USER_SYSTEM

#change this to local file
filePath = ""
dir = os.path.dirname(__file__)
filePath = ""
if USER_SYSTEM == 'w':
    filePath = os.path.join(dir, '..\emulator\input\\')
else:
    filePath = os.path.join(dir, '../emulator/input/')

fileNumber = input('Enter the file number: ')
fileName = "marathon_"+ fileNumber + ".pkl"
data = pkl.load(open(filePath + fileName, "rb"))

datalist = data['scan_data']
platformPos = data['platform_pos']
rangeBins = data['range_bins']
SCAN_COUNT = len(data['scan_data'])

pixeldata = {}

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
    return np.abs(image)

xPos = np.arange(COORDINATES[0],COORDINATES[1],CROSS_RANGE_RESOLUTION)
yPos = np.arange(COORDINATES[2],COORDINATES[3],RANGE_RESOLUTION)
pixeldata["x"] = xPos
pixeldata["y"] = yPos


plt.imshow(paintImage(datalist, rangeBins, platformPos, xPos, yPos), cmap='gray', origin='lower', extent=COORDINATES)
plt.colorbar()
plt.xlabel("x-axis (meters/"+str((COORDINATES[1]-COORDINATES[0])/RANGE_RESOLUTION)+" pixels)")
plt.ylabel("y-axis (meters/"+str((COORDINATES[3]-COORDINATES[2])/CROSS_RANGE_RESOLUTION)+" pixels)")
plt.title(fileName)
plt.savefig("marathon_images/finalimages/marathon_{}_thumbnail.jpg".format(fileNumber)) #save as jpg

with open('marathon_images/imagedicts/marathon_{}_image.pkl'.format(fileNumber), 'wb') as f:
        pkl.dump(pixeldata, f)

plt.show()