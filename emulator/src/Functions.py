import math
from matplotlib import pyplot as plt
import numpy as np
from constants import SPEED_OF_LIGHT
from Point import Point


##R = tc/2

def tou(a, b):
    return 2*(a.distance(b))/SPEED_OF_LIGHT
#grid = np.zeros((int(LENGTH), int(WIDTH)))
#plt.imshow(grid, cmap='gray')

#print(RESOLUTION)
#print(CROSS_RESOLUTION)

#RCS = TOU