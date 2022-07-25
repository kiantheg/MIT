import pickle
from Point import Point
from alive_progress import alive_bar
import numpy as np
import time

'''for x in 50, 60, 30, 0:
    with alive_bar(x) as bar:
        for i in range(x):
            time.sleep(.001)
            bar()'''
# load : get the data from file
data = pickle.load(open("/Users/zxiao23/Desktop/BWSISummer/team5/mypickle.pickle", "rb"))
print(data)

#print((20 - 1.14627368)/2000/200000E-12)
#print((17.16877474 + 20)/2000/400000E-12)

xPos = np.arange(-10,10,0.1)
yPos = np.arange(-10,10,0.1)
#with open('mypickle.pickle', 'wb') as f:
    #pickle.dump(xPos, f)