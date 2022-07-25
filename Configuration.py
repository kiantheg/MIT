from Point import Point

#Constants
SPEED_OF_LIGHT = 299792458 # (m/s)
K = 1.380649 * 10e-23 # Boltzmann constant (J/K)
T0 = 290 # Standard system temperature (K)
BANDWIDTH = 1.1 * 10e9
CENTERED_FREQUENCY = 4.3 * 10e9
CENTERED_WAVELENGTH = SPEED_OF_LIGHT/CENTERED_FREQUENCY
VELOCITY = 66.730296

CPI = 0.74
PLATFORM_POS = "/Users/kianchen/Desktop/BeaverWorks/emulator/output/20220725T115842_5_point_scatter_platform_pos.pkl"
#RANGE_RESOLUTION = SPEED_OF_LIGHT/(2* BANDWIDTH)
#CROSS_RANGE_RESOLUTION = CENTERED_WAVELENGTH * RANGE_TO_TARGET / (2*VELOCITY*CPI)
COORDINATES = [-10,10,-10,10] # x_start, x_end, y_start, y_end
RANGE_RESOLUTION = 0.1
CROSS_RANGE_RESOLUTION = 0.1

SCAN_COUNT = 1000
SCAN_START = 0 #+/-499,998 ps
SCAN_END = int(2*26e12/SPEED_OF_LIGHT) #+/-499,998 ps
SCAN_RES = 32 #1-511
BII = 8 #6-15