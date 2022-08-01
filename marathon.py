import pickle as pkl
from Point import Point
from alive_progress import alive_bar
import numpy as np
import time

'''
data format:
dictionary with 3 keys:
1st key: scan_data, 1st val: multidimensional array with scan data
2nd key: platform_pos: 1nd val: md array of range pos
3rd key: range_bins: 1d array of range bins
'''

# load : get the data from file
marathon_datalist = pkl.load(open("/Users/rishita/bwsi22/team5/marathon_0.pkl", "rb"))
print(marathon_datalist['scan_data'])
print(np.shape(marathon_datalist['scan_data']))
