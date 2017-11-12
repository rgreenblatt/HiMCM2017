import numpy as np
import random
import deap

from deap import base
from deap import creator
from deap import tools

NGEN = 10
CXPB = .3
MUTPB = .03

# Organisms will probably be treated as graphs with points representing the entry and exit points
class Resort_Map():
    def __init__(self, chair_set, trail_set):
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

    def make_path():
        pass

    def make_chair(self, point1, point2):
        

def mag(a1):
    return np.sqrt(a1.dot(a1))

def fitness(trail_map):
    #TODO: trail_map gives chair endpoints as list, followed by list of trail points. 
    # Ryan will write a fitness function    

    pass

def mutate(child):
    #TODO:Take the top point of some trails. Draw new paths to the bottom. 
    pass

def cross(parent1, parent2):
    #TODO: Take the bottom points of chairlifts. 
    # This function must modify parent1 and parent2
    pass

def rand_map():
    # Return a map object
    out = Resort_Map([], [])
    
    # Allocate chair lifts

    # Allocate trails

    return out

def driver(NGEN=10, CXPB=.5, MUTPB=.1):
    # Initialize our fitness function
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))

    # Set our individual class to be composed of resort maps
    creator.create("Individual", Resort_Map, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    # Register a function to make random maps for population generation
    toolbox.register("individual", rand_map)

    # Register the population
    toolbox.register("population", tools.initRepeat, list, toolbox.individual, n=100)

    toolbox.register("mate", cross)
    toolbox.register("mutate", mutate)
    toolbox.register("select", tools.selTournament, tournsize=5)
    toolbox.register("evaluate", fitness)

    pop = toolbox.population()

    invalid = [ind for ind in pop if ind.fitness=None]
    fitnesses = list(toolbox.map(toolbox.evaluate, invalid))
    for ind, fit in zip(invalid, fitnesses):
        ind.fitness = fit

    for g in range(NGEN):
        offspring = toolbox.select(pop, len(pop))

        # Clone selected
        offspring = list(map(toolbox.clone, offspring))
        
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                child1.fitness = None
                child2.fitness = None

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                mutant.fitness = None

        invalid = [ind for ind in offspring if ind.fitness=None]
        fitnesses = list(toolbox.map(toolbox.evaluate, invalid))
        for ind, fit in zip(invalid, fitnesses):
            ind.fitness = fit

        # Replace the population with the offspring
        pop[:] = offspring

    fittest = pop[0]
    fit = fittest.fitness
    for ind in pop[1:]:
        if ind.fitness > fit:
            fit = ind.fitness
            fittest = ind
    return (ind, fit)

if __name__ == 'main':
    test = rand_map()
    
