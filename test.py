import glob
import os
import pickle as pkl
dir = os.path.dirname(__file__)
fileName = os.path.join(dir, '..\emulator\output\*')
list_of_files = glob.glob(fileName) # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
data = pkl.load(open(latest_file, "rb"))
platformPos = data['platform_pos']
print(platformPos)