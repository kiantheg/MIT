import math
from matplotlib import pyplot as plt
import numpy as np
from constants import SPEED_OF_LIGHT, BANDWIDTH, T0, CENTERED_WAVELENGTH, CENTERED_FREQUENCY, VELOCITY
#from client import CPI 
from Point import Point


##R = tc/2

def tou(a, b):
    return 2*(a.distance(b))/SPEED_OF_LIGHT

#CPI_40000 = 0.74
#RANGE_TO_TARGET = Point(0,-15,5).distance(Point(0,0,0))
#RANGE_RESOLUTION = SPEED_OF_LIGHT/(2* BANDWIDTH)
#CROSS_RESOLUTION = CENTERED_WAVELENGTH * RANGE_TO_TARGET / (2*VELOCITY*CPI_40000)
RANGE_RESOLUTION = 0.1
CROSS_RESOLUTION = 0.1

LENGTH = 247
WIDTH = 247
#grid = np.zeros((int(LENGTH), int(WIDTH)))
#plt.imshow(grid, cmap='gray')

#print(RESOLUTION)
#print(CROSS_RESOLUTION)

#RCS = TOU
