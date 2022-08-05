import pickle as pkl
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
from alive_progress import alive_bar
from Configuration import SCAN_COUNT, SPEED_OF_LIGHT, RANGE_RESOLUTION, CROSS_RANGE_RESOLUTION, COORDINATES, SCAN_RES, USER_SYSTEM

datalist = pkl.load(open("datalist.pkl", "rb"))

imgNum = input("What is the number of the hide and seek image?: ")

def readPlatformPos():
    dir = os.path.dirname(__file__)
    platPath = ""
    if USER_SYSTEM == 'w':
        platPath = os.path.join(dir, '..\emulator\output\*')
    else:
        platPath = os.path.join(dir, '../emulator/output/*')
    list_of_files = glob.glob(platPath) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    data = pkl.load(open(latest_file, "rb"))
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
            image[:] += datalist[scan][np.minimum(temp, np.full((numX,numY),len(datalist[0])-1)).astype(int)]
            bar()
    return image

xPos = np.arange(COORDINATES[0],COORDINATES[1],CROSS_RANGE_RESOLUTION)
yPos = np.arange(COORDINATES[2],COORDINATES[3],RANGE_RESOLUTION)

image = paintImage(datalist, readPlatformPos(), xPos, yPos)
saveDic = {'img': image, 'x': xPos, 'y': yPos}
with open('hide_and_seek_images/imagedicts/hide_and_seek_{}_img.pkl'.format(imgNum), 'wb') as f:
    pkl.dump(saveDic, f)

plt.imshow(image, cmap='gray', origin='lower', extent=COORDINATES)
plt.colorbar()
plt.xlabel("x-axis (meters/"+str((COORDINATES[1]-COORDINATES[0])/RANGE_RESOLUTION)+" pixels)")
plt.ylabel("y-axis (meters/"+str((COORDINATES[3]-COORDINATES[2])/CROSS_RANGE_RESOLUTION)+" pixels)")
plt.title('hide_and_seek_{}_thumbnail'.format(imgNum))
plt.savefig("hideandseek_images/finalimages/hide_and_seek_{}_img.pkl")
plt.show()