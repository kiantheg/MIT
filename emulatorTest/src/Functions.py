import math
from matplotlib import pyplot as plt
import numpy as np
from constants import SPEED_OF_LIGHT, BANDWIDTH, T0, CENTERED_WAVELENGTH, CENTERED_FREQUENCY, VELOCITY
from Point import Point


##R = tc/2

def tou(a, b):
    return 2*(a.distance(b))/SPEED_OF_LIGHT

RANGE_TO_TARGET = tou(Point(-19,15,5),Point(0,0,0)) * SPEED_OF_LIGHT/2
CPI = 0.74
#RANGE_RESOLUTION = SPEED_OF_LIGHT/(2* BANDWIDTH)
#CROSS_RANGE_RESOLUTION = CENTERED_WAVELENGTH * RANGE_TO_TARGET / (2*VELOCITY*CPI)

RANGE_RESOLUTION = 0.1
CROSS_RANGE_RESOLUTION = 0.1

LENGTH = 247
WIDTH = 247
#grid = np.zeros((int(LENGTH), int(WIDTH)))
#plt.imshow(grid, cmap='gray')

#print(RESOLUTION)
#print(CROSS_RESOLUTION)

#RCS = TOU
