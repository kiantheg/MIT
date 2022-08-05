<<<<<<< Updated upstream

import pickle              # import module first

f = open('/Users/rishita/bwsi22/team5/marathon_0_image.pkl', 'r')   # 'r' for reading; can be omitted
mydict = pickle.load(f)         # load file content as mydict
f.close()                       

print(mydict)
=======
import pickle as pkl
import glob
import os
from Configuration import COORDINATES
import numpy as np
import matplotlib.pyplot as plt
img = pkl.load(open("hide_and_seek_8_img.pkl", "rb"))
plt.imshow(img['img'], cmap='gray', origin='lower', extent=COORDINATES)
plt.show()
>>>>>>> Stashed changes
