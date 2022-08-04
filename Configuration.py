import os

#Constants
SPEED_OF_LIGHT = 299792458 # (m/s)
K = 1.380649 * 10e-23 # Boltzmann constant (J/K)
T0 = 290 # Standard system temperature (K)
BANDWIDTH = 1.1 * 10e9
CENTERED_FREQUENCY = 4.3 * 10e9
CENTERED_WAVELENGTH = SPEED_OF_LIGHT/CENTERED_FREQUENCY
VELOCITY = 66.730296

USER_SYSTEM = input("Which system are you running on? (w/m): ")
dir = os.path.dirname(__file__)
PLAT_PATH = ""
if USER_SYSTEM == 'w':
    PLAT_PATH = os.path.join(dir, '..\emulator\output\*')
else:
    PLAT_PATH = os.path.join(dir, '../emulator/output/*')


CPI = 0.74
#RANGE_RESOLUTION = SPEED_OF_LIGHT/(2* BANDWIDTH)
#CROSS_RANGE_RESOLUTION = CENTERED_WAVELENGTH * RANGE_TO_TARGET / (2*VELOCITY*CPI)
COORDINATES = [-120,-20,-150,-50] # x_start, x_end, y_start, y_end #img1 is -2,2 
RANGE_RESOLUTION = 0.05 #img1 is 0.05
CROSS_RANGE_RESOLUTION = RANGE_RESOLUTION

SCAN_COUNT = 1000
SCAN_START = 0 #in meters
SCAN_END = 50 #in meters
SCAN_RES = 32 #1-511
BII = 8 #6-15