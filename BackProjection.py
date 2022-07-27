import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
from alive_progress import alive_bar
from Configuration import SCAN_COUNT, SPEED_OF_LIGHT, RANGE_RESOLUTION, CROSS_RANGE_RESOLUTION, PLATFORM_POS, COORDINATES, SCAN_RES

#read datalist from pickle file
datalist = pkl.load(open("/Users/rishita/bwsi22/team5/datalist.pkl", "rb"))

def readPlatformPos(filepath):
    data = pkl.load(open(filepath, "rb"))
    platformPos = data['platform_pos']
    return platformPos

'''def paintImage(datalist, platformPos, xCor, yCor, zOffset = 0):
    numX = len(xCor)
    numY = len(yCor)
    sar_image_complex = np.zeros((numY,numX))
    with alive_bar(numX) as bar:
        for x in range(numX):
            for y in range(numY):
                for scan in range(SCAN_COUNT):
                    oneWayRange = np.sqrt((xCor[x] - platformPos[scan][0])**2 + (yCor[y] - platformPos[scan][1])**2 + (zOffset - platformPos[scan][2])**2)
                    totalTime = 2 * oneWayRange * 1e12 / SPEED_OF_LIGHT
                    closestIndex = min(int(totalTime / 61), len(datalist[0])-1)
                    sar_image_complex[x][y] += datalist[scan][closestIndex]
            bar()
    sar_image_complex /= abs(sar_image_complex).max()
    return sar_image_complex'''

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
'''
print()
print()
print(message['scan_type'])
platformPos = readPlatformPos(PLATFORM_POS)
oneWayRange = np.sqrt((20)**2 + (15)**2 + (5)**2)
totalTime = 2*oneWayRange * 1e12 / SPEED_OF_LIGHT
print(totalTime / 61)
shift = int(totalTime / 61)
print(oneWayRange)
print(totalTime)
print(shift)
zoomedInData = []
for i in range(-5,6):
    zoomedInData.append(datalist[0][shift+i])
print(zoomedInData)
'''
plt.imshow(paintImage(datalist, readPlatformPos(PLATFORM_POS), xPos, yPos), cmap='gray', origin='lower')
plt.show()