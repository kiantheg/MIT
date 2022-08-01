from Point import Point
import glob
import os

#Constants
SPEED_OF_LIGHT = 299792458 # (m/s)
K = 1.380649 * 10e-23 # Boltzmann constant (J/K)
T0 = 290 # Standard system temperature (K)
BANDWIDTH = 1.1 * 10e9
CENTERED_FREQUENCY = 4.3 * 10e9
CENTERED_WAVELENGTH = SPEED_OF_LIGHT/CENTERED_FREQUENCY
VELOCITY = 66.730296

list_of_files = glob.glob('/Users/kianchen/Desktop/BeaverWorks/emulator/output/*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)

CPI = 0.74
PLATFORM_POS = latest_file
#RANGE_RESOLUTION = SPEED_OF_LIGHT/(2* BANDWIDTH)
#CROSS_RANGE_RESOLUTION = CENTERED_WAVELENGTH * RANGE_TO_TARGET / (2*VELOCITY*CPI)
COORDINATES = [-130,-50,-115,-35] # x_start, x_end, y_start, y_end #img1 is -2,2 
RANGE_RESOLUTION = 0.05 #img1 is 0.05
CROSS_RANGE_RESOLUTION = RANGE_RESOLUTION

SCAN_COUNT = 1000
SCAN_START = 0 #+/-499,998 ps
SCAN_END = int(2*50e12/SPEED_OF_LIGHT) #+/-499,998 ps
SCAN_RES = 32 #1-511
BII = 8 #6-15