import numpy as np
import random
import path as path_lib
import sys

BASE_LIFTS = 3
# Organisms will probably be treated as graphs with points representing the entry and exit points
class Resort_Map():
    def __init__(self, chair_set=None, trail_set=None):
        self.chair_set = chair_set # chair set is a list of arrays specifying chair end points

        self.trail_set = trail_set # trail_set is a list of arrays specifying the trails
        self.fitness = None

    def make_trail(self, chair):
        # Karna and Ryan will write this
        # Given the endpoints of a chair, find a path for a 
        curr = chair[1]
        bottom = chair[0]
        path = []
        while mag(curr - bottom) < 200:
            dir = (bottom - curr)/mag(bottom-curr)
            theta = np.pi*(random.random()*15-30)/180
            dir = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), -np.cos(theta)]]).dot(dir)
            curr += dir * 50

        self.trail_set.append(path)

    def make_path(self, chair):
        curr = chair[1]
        bottom = chair[0]
        path = []
        path.append(curr)
        disp = (bottom-curr)/5
        for i in range(3):
            curr += disp
            theta = np.pi*(random.random()*90-45)/180
            dir = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), -np.cos(theta)]]).dot(disp)
            path.append(curr+dir)
        path.append(bottom)
        self.trail_set.append(path)

    def owned_by(self, trail):
        for chair in self.chair_set:
            if chair[1] == trail[0] and chair[0] == trail[-1]:
                return chair
            elif trail[0] == chair[0]:
                return chair
        return None 

    def trails_owned(self, chair):
        out = []
        for trail in self.trail_set:
            if trail[0] == chair[1] and trail[-1] == chair[0]:
                out.append(trail)
            elif trail[0] == chair[0]:
                out.append(trail)
        return out


    def make_chair(self, bottom, top):
        self.chair_set.append(np.array([bottom, top]))

    def rem_chair(self):
        ind = random.randint(BASE_LIFTS, len(self.chair_set)-1)
        dead = self.chair_set[ind]

        #TODO: Remove this if it's not working out

        for trail in self.trail_set:
            if trail[0] == dead[1]:
                self.trail_set.remove(trail)

            elif trail[0] == dead[0]:
                toKill = True

                index = 0
                for trail2 in self.trail_set:
                    if trail2[-1] == dead[0]:
                        toKill = False
                        toExtend = index     
                    index += 1
        
                if not toKill:
                    self.trail_set[toExtend] += trail[1:]
    
                self.trail_set.remove(trail)

            index+=1
                    
        del self.chair_set[ind]
