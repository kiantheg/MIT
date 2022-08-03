from Point import Point

USER = input("Who is running the code in team 5? (r/g/am/aw/k/other): ")

#Constants
SPEED_OF_LIGHT = 299792458 # (m/s)
K = 1.380649 * 10e-23 # Boltzmann constant (J/K)
T0 = 290 # Standard system temperature (K)
BANDWIDTH = 1.1 * 10e9
CENTERED_FREQUENCY = 4.3 * 10e9
CENTERED_WAVELENGTH = SPEED_OF_LIGHT/CENTERED_FREQUENCY
VELOCITY = 66.730296

if USER == 'k':
    PLAT_PATH = "/Users/kianchen/Desktop/BeaverWorks/emulator/output/*"
elif USER == 'am':
    PLAT_PATH = "/Users/zxiao23/Desktop/BWSISummer/emulator/output/*"
elif USER == 'r':
    PLAT_PATH = "/Users/rishita/bwsi22/emulator/output/*"
elif USER == 'g':
    PLAT_PATH = r"C:\Users\gheat\Documents\GitHub\emulator\output\*"
elif USER == 'aw':
    PLAT_PATH = r"\Users\xiaoz\Documents\BWSISummer\emulator\output\*"
else:
    USER_SYSTEM = input("Which system are you running on? (w/m): ")
    PLAT_PATH = input("Please enter your path to the output folder in emulator: ")
    if USER_SYSTEM == 'w':
        PLAT_PATH = repr(PLAT_PATH + '\*')
    else:
        PLAT_PATH = PLAT_PATH + '/*'

CPI = 0.74
#RANGE_RESOLUTION = SPEED_OF_LIGHT/(2* BANDWIDTH)
#CROSS_RANGE_RESOLUTION = CENTERED_WAVELENGTH * RANGE_TO_TARGET / (2*VELOCITY*CPI)
COORDINATES = [-50,50,-50,50] # x_start, x_end, y_start, y_end #img1 is -2,2 
RANGE_RESOLUTION = 0.1 #img1 is 0.05
CROSS_RANGE_RESOLUTION = RANGE_RESOLUTION

SCAN_COUNT = 65535
SCAN_START = 0 #in meters
SCAN_END = 50 #in meters
SCAN_RES = 32 #1-511
BII = 8 #6-15