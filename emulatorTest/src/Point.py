import math
class Point:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z
    def distance(self, o):
        return math.sqrt((self.x - o.x)**2 + (self.y - o.y)**2 + (self.z - o.z)**2)
