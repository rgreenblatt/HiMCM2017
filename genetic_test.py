import numpy
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
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
        self.fitness = None
    def __str__(self):
        return "("+str(self.num1)+", "+str(self.num2)+")   " + str(self.fitness)

def fitness(trail_map):
    return 50 - abs(50-trail_map.num1-trail_map.num2)

def mutate(child):
    child.num1 = child.num1 + random.random() * 5
    child.num2 = child.num2 + random.random() * 5

def cross(parent1, parent2):
    stuff = parent1.num2
    parent1.num2 = parent2.num2
    parent2.num2 = stuff

def rand_map():
    # Return a map object
    out = Resort_Map(random.random()*50, random.random()*50)
    
    # Allocate chair lifts

    # Allocate trails

    return out

def driver(NGEN=10, CXPB=.5, MUTPB=.2):
    # Initialize our fitness function
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))

    # Set our individual class to be composed of resort maps
    creator.create("Individual", Resort_Map, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    # Register a function to make random maps for population generation
    toolbox.register("individual", rand_map)

    # Register the population
    toolbox.register("population", tools.initRepeat, list, toolbox.individual, n=10)

    toolbox.register("mate", cross)
    toolbox.register("mutate", mutate)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", fitness)

    pop = toolbox.population()
    fitnesses = list(toolbox.map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
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

        invalid = [ind for ind in offspring if ind.fitness==None]
        fitnesses = toolbox.map(toolbox.evaluate, invalid)
        for ind, fit in zip(invalid, fitnesses):
            ind.fitness = fit

        # Replace the population with the offspring
        pop[:] = offspring
        print('\n'.join([str(k) for k in pop]))

    fittest = pop[0]
    fit = fittest.fitness
    for ind in pop[1:]:
        if ind.fitness > fit:
            fit = ind.fitness
            fittest = ind
    return (ind, fit)

sol = driver()[0]
print(sol.num1, sol.num2)
