import math
from constants import SPEED_OF_LIGHT, BANDWIDTH, T0, CENTERED_WAVELENGTH, CENTERED_FREQUENCY, VELOCITY
from Point import Point
from client import CPI, scanCount

##R = tc/2

def tou(a, b):
    return 2*(a.distance(b))/SPEED_OF_LIGHT


RANGE_TO_TARGET = tou((-19,15,5),(0,0,0)) * SPEED_OF_LIGHT/2
RESOLUTION = SPEED_OF_LIGHT/(2* BANDWIDTH)
CROSS_RESOLUTION = CENTERED_WAVELENGTH * RANGE_TO_TARGET / (2*VELOCITY*CPI)



#RCS = TOU
