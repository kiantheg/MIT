from dataclasses import dataclass
import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
from alive_progress import alive_bar
from Configuration import COORDINATES, SPEED_OF_LIGHT, CROSS_RANGE_RESOLUTION, RANGE_RESOLUTION

#change this to local file
data = pkl.load(open("/Users/zxiao23/Desktop/BWSISummer/emulator/input/marathon_0.pkl", "rb"))

datalist = data['scan_data']
platformPos = data['platform_pos']
rangeBins = data['range_bins']
SCAN_COUNT = len(data['scan_data'])

def paintImage(datalist, rangeBins, platformPos, xCor, yCor, zOffset = 0):
    numX = len(xCor)
    numY = len(yCor)
    image = np.zeros((numX, numY))
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
            image += np.abs(temp).astype(int)
            bar()
    print(np.shape(image))
    return image

xPos = np.arange(COORDINATES[0],COORDINATES[1],CROSS_RANGE_RESOLUTION)
yPos = np.arange(COORDINATES[2],COORDINATES[3],RANGE_RESOLUTION)

plt.imshow(paintImage(datalist, rangeBins, platformPos, xPos, yPos), cmap='gray', origin='lower', extent=COORDINATES)
plt.colorbar()
plt.xlabel("x-axis (meters/"+str((COORDINATES[1]-COORDINATES[0])/RANGE_RESOLUTION)+" pixels)")
plt.ylabel("y-axis (meters/"+str((COORDINATES[3]-COORDINATES[2])/CROSS_RANGE_RESOLUTION)+" pixels)")
plt.title("Hello")
plt.show()