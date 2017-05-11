import math


class Vector2D:
    def __init__(self, x=0,y=0):
        self.x = x
        self.y = y

    def set_coords_2d(self,x,y):
        self.x = x
        self.y = y

    def output(self):
        print "x is",self.x,"y is",self.y

    def unit(self):
        self.x = self.x/self.mod()
        self.y = self.y/self.mod()
        return self

    def mod(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

    def invert(self):
        self.x = -self.x
        self.y = -self.y
        return self

def vectorAdd(v1,v2):
    return Vector2D(v1.x+v2.x, v1.y+v2.y)


def vector_from_to(v1, v2):
    return Vector2D(v2.x - v1.x, v2.y - v1.y)

def scalar_multiply(v,c):
    v.x=v.x*c
    v.y=v.y*c
    return v

if __name__ == "__main__":
    v1 = Vector2D(1,2)
    v2 = Vector2D(3,4)

