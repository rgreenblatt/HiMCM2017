import numpy as np
import random

def mag(a1):
    return np.sqrt(a1.dot(a1))

bottom = np.array([0,0])
curr = np.array([-5,0])
dir = (bottom - curr)/mag(bottom-curr)
theta = np.pi*(random.random()*15-30)/180
dir = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), -np.cos(theta)]]).dot(dir)

print(dir)
