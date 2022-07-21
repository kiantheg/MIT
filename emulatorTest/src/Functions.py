import math
from matplotlib import pyplot as plt
import numpy as np
from constants import SPEED_OF_LIGHT, BANDWIDTH, T0, CENTERED_WAVELENGTH, CENTERED_FREQUENCY, VELOCITY
from Point import Point


##R = tc/2

def tou(a, b):
    return 2*(a.distance(b))/SPEED_OF_LIGHT


#RANGE_TO_TARGET = tou(Point(-19,15,5),Point(0,0,0)) * SPEED_OF_LIGHT/2
#RESOLUTION = SPEED_OF_LIGHT/(2* BANDWIDTH)
#CROSS_RESOLUTION = CENTERED_WAVELENGTH * RANGE_TO_TARGET / (2*VELOCITY*CPI)
RANGE_RESOLUTION = 0.06
CROSS_RESOLUTION = 0.07

LENGTH = 247
WIDTH = 247
grid = np.zeros((int(LENGTH), int(WIDTH)))
plt.imshow(grid, cmap='gray')
plt.show()

#print(RESOLUTION)
#print(CROSS_RESOLUTION)

#RCS = TOU
