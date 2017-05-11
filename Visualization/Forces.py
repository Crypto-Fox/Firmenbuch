import Vector
import math

def force_square_attractive(v1,v2):
    vector = Vector.vector_from_to(v1, v2)
    distance = vector.mod()
    mag = 10000/math.pow(distance,2)
    #print "square",mag

    return Vector.scalar_multiply(vector.unit(),mag)


def force_cube_repulsion(v1,v2):
    vector = Vector.vector_from_to(v1, v2)
    distance = vector.mod()
    mag = -1000000/math.pow(distance, 3)
    #print "cube",mag


    return Vector.scalar_multiply(vector.unit(), mag)


def springForce(v1,v2,baseLength):
    vector = Vector.vector_from_to(v1, v2)
    distance = vector.mod()-baseLength
    mag = distance*2
    #print "spring",mag

    return Vector.scalar_multiply(vector.unit(),mag)