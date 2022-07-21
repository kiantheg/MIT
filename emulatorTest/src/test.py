import pickle
from Point import Point
# load : get the data from file
data = pickle.load(open("/Users/zxiao23/Desktop/BWSISummer/team5/emulatorTest/output/20220719T103736_5_point_scatter_platform_pos.pkl", "rb"))
print(data)

#print((20 - 1.14627368)/2000/200000E-12)
#print((17.16877474 + 20)/2000/400000E-12)

p1 = Point(1, 2, 3)
print(p1.distance(Point(2,3,3)))