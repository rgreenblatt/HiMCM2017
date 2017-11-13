import numpy as np
import random
import path as path_lib
import sys

def mag(a):
	return np.sqrt(a.dot(a))

def convert(feet):
    return feet/345876.

BASE_LIFTS = 3
# Organisms will probably be treated as graphs with points representing the entry and exit points
class Resort_Map():
    def __init__(self, chair_set=None, trail_set=None):
        self.chair_set = chair_set # chair set is a list of arrays specifying chair end points
        self.trail_set = trail_set # trail_set is a list of arrays specifying the trails
        self.fitness = None
    
    def make_path(self, chair):

        x = np.linspace(chair[1,0],chair[0,0],5)
        y = np.linspace(chair[1,1],chair[0,1],5)

        self.trail_set.append(np.array([x,y]))
        
    def owned_by(self, trail):
        for chair in self.chair_set:
            if np.sqrt(np.sum(np.square(chair[1] - trail[0]))) < convert(40) and np.sqrt(np.sum(np.square(chair[0] - trail[-1]))):
                return chair
            elif np.all(trail[0] == chair[0]):
                return chair
        return None 

    def trails_owned(self, chair):
        out = []
        for trail,i in zip(self.trail_set,range(len(self.trail_set))):
            if np.sum(trail[:,0]-chair[1]) < convert(80) and np.sum(trail[:,-1] - chair[0]) < convert(80):
                out.append(i)
            elif np.all(np.array(trail[0] == chair[0])):
                out.append(i)
        return out


    def make_chair(self, bottom, top):
        self.chair_set.append(np.array([bottom, top]))

    def rem_chair(self):
        if len(self.chair_set) > BASE_LIFTS:
            ind = np.random.randint(len(self.chair_set))
            del self.chair_set[ind]

