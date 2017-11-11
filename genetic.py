import numpy
import random
import deap

from deap import base
from deap import creator
from deap import tools

# Organisms will probably be treated as graphs with points representing the entry and exit points

def fitness(trail_map):
    #TODO: trail_map gives chair endpoints as list, followed by list of trail points. 
    

    pass

def mutate(child):
    #TODO:Take the top point of some trails. Draw new paths to the bottom. 
    pass

def cross(parent1, parent2):
    #TODO: Take the bottom points of chairlifts. 
    pass

# Initialize our fitness function
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

# 
creator.create("Individual", list, )
