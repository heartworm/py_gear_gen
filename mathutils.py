import numpy as np
from math import *

def rotation_matrix(theta):
    return np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])

def flip_matrix(h, v):
    return [[-1 if h else 1, 0], [0, -1 if v else 1]]

def polar_to_cart(*coords):
    if len(coords) == 1:
        coords = coords[0]
    r, ang = coords
    return r * cos(ang), r * sin(ang)


def cart_to_polar(*coords):
    if len(coords) == 1:
        coords = coords[0]
    x, y = coords
    return sqrt(x * x + y * y), atan2(y, x)