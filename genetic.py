import numpy as np
import random
import deap
import path as path_lib
import sys

from deap import base, creator, tools, algorithms

from terrain import terrain
from fitness import fitness
from tMap import Resort_Map

NGEN = 10000
CXPB = .6
MUTPB = .3
P1 = .1
P2 = .4
P3 = .4
P4 = .4
BASE_LIFTS = 3
POP_SIZE = 100

# Organisms will probably be treated as graphs with points representing the entry and exit points
def mag(a1):
    return np.sqrt(a1.dot(a1))

class gen_algoth:
  
    GROUND = terrain()

    run_count = 0

    def call_fitness(individual):
        gen_algoth.run_count += 1
        print(gen_algoth.run_count)
        if len(np.array(individual.chair_set).shape) < 3:
                print(np.array(individual.chair_set).shape)
        return fitness(individual, gen_algoth.GROUND)

    def mutate(child):
        
        #TODO:Take the top point of some trails. Draw new paths to the bottom. 
        if random.random() < P1:
            gen_algoth.mutate1(child)
        if random.random() < P2:
            gen_algoth.mutate2(child)
        '''
        if random.random() < P3:
            gen_algoth.mutate3(child)
        if random.random() < P4:
            gen_algoth.mutate4(child)
        '''
        pass

    def mutate1(child): # Add/Remove Ski Lift
        choice = random.randint(0,1)
        if choice: # Add Ski Lift
            bounds = gen_algoth.GROUND.regions.box_region()
            xlen = abs(bounds[0][0] - bounds[1][0])
            ylen = abs(bounds[0][1] - bounds[1][1])
            
            higher,lower = gen_algoth.chair_location(1)[0]
            
            immutable_peaks = [chair[1] for chair in child.chair_set[:BASE_LIFTS]]
            immutable_bottom = [chair[0] for chair in child.chair_set[:BASE_LIFTS]]

            child.make_chair(lower, higher)

            nearest = immutable_peaks[0]
            dist = mag(lower - nearest)
            for peak in immutable_peaks[1:]:
                if mag(peak - lower) < dist:
                    nearest = peak
                    dist = mag(lower-nearest)
            for j in range(random.randint(1,2)):
                tmp = np.array([lower, nearest])
                child.make_path(tmp)

            # Repeat process for path to bottom
            nearest = immutable_bottom[0]
            dist = mag(lower - nearest)
            for base in immutable_bottom[1:]:
                if mag(base - lower) < dist:
                    nearest = base
                    dist = mag(lower-nearest)
            for j in range(random.randint(1,2)):
                tmp = np.array([nearest, lower])
                child.make_path(tmp)
        else:
            if(BASE_LIFTS<len(child.chair_set)-1):
                child.rem_chair()
            
        
    def mutate2(child): # Add/Remove Trails
        choice = random.randint(0,1)
        if choice: # Add Trail
            trails = random.randint(1,4)
            for i in range(trails):
                chair = child.chair_set[random.randint(0, len(child.chair_set)-1)]
                child.make_path(chair)
        else:
            trails = random.randint(1,3)
            for i in range(trails):
                if child.trail_set:
                    child.trail_set.pop(random.randint(0, len(child.trail_set)-1))
        
        if len(np.array(child.chair_set).shape) < 3:
                print(np.array(child.chair_set).shape)


    def mutate3(child): # Add/Remove Midpoints
        if len(child.trail_set) > 0:
            choice = random.randint(0,1)
            index = np.random.randint(len(child.trail_set))
            trail = child.trail_set[index]
            if choice: # Add Midpoint
                spline = path_lib.paths()
                spline.set_points(np.transpose(np.array(trail)))
                new_point = spline.find_point(random.random())
                trail.append(new_point)
            else:
                if len(trail) > 2:
                    ind = random.randint(1, len(trail) - 2)
                    trail.pop(ind)
        else: print("No Trails (Mut3)")
        
    def mutate4(child): # Shift Midpoints
        if len(child.trail_set) > 0:
            num_trails = random.randint(2,5)
            num_points = random.randint(2,5)
            for i in range(num_trails):
                trail = child.trail_set[random.randint(0, len(child.trail_set)-1)]
                for x in range(num_points):
                    if len(trail) > 2:
                        ind = random.randint(1, len(trail) - 2)
                        bottom = trail[-1]
                        curr = trail[ind]
                        delta = (bottom - curr) / 10
        
                        theta = np.pi*(random.random()*90-45)/180
                        delta = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), -np.cos(theta)]]).dot(delta)
                        trail[ind] = curr+delta

        else: print("No Trails!")

    def cross(parent1,parent2):
        child1 = gen_algoth.cross_helper(parent1,parent2)
        child2 = gen_algoth.cross_helper(parent2,parent1)
        parent1.trail_set = child1.trail_set
        parent1.chair_set = child1.chair_set
        parent2.trail_set = child2.trail_set
        parent2.chair_set = child2.chair_set

    def cross_helper(parent1,parent2):
        if(len(np.array(parent1.trail_set).shape)<3):
                print(np.array(parent1.trail_set).shape)
                print(parent1.trail_set)
        if(len(np.array(parent2.trail_set).shape)<3):
                print(np.array(parent2.trail_set).shape)
                print(parent2.trail_set)
        chrlens=(len(parent1.chair_set),len(parent2.chair_set))
        chrlen=chrlens[random.randint(0,1)]
        
        trlens=(len(parent1.trail_set),len(parent2.trail_set))
        trllen=trlens[random.randint(0,1)]
        
        chrpars=(parent1.chair_set,parent2.chair_set)
        trlpars=(parent1.trail_set,parent2.trail_set)

        child=Resort_Map([],[])
        watched=[]
        
        back = 0
        for i in range(chrlen):
            index=random.randint(0,1)
            currparent=chrpars[index]
            if i < len(currparent):
                child.chair_set.append(currparent[i])
                
                if(BASE_LIFTS <= i): 
                    #watched.append(child.chair_set[i][0])
                    watched.append((i-back,0))
                    #watched.append(child.chair_set[i][1])
                watched.append((i-back, 1))
            else:
                back += 1

        for i in range(trllen):
            for parent in trlpars:
                if i < len(parent):
                        currtrail=parent[i]
                        for inds in watched:
                                toWatch = child.chair_set[inds[0]][inds[1]]
                                if mag(toWatch - currtrail[0]) < .0001:
                                        child.trail_set.append(currtrail)

        print(np.array(child.trail_set).shape)
        if(len(np.array(child.trail_set).shape)<3):
                print(np.array(child.trail_set).shape)
                print(child.trail_set)
        return child

    def chair_location(num_chairs):
        point_array = gen_algoth.GROUND.regions.get_random_points(2*num_chairs)
        point_array = np.reshape(point_array,(2,-1,1))
        heights = gen_algoth.GROUND.height_at_coordinates(np.array(point_array))

        point_array = np.reshape(point_array,(num_chairs,2,-1))
        heights = np.reshape(heights,(num_chairs,2))
        
        chairs = []
        for i in range(num_chairs):

            if heights[i][0] < heights[i][1]:
                higher = point_array[i][1]
                lower = point_array[i][0]

            else:
                higher = point_array[i][0]
                lower = point_array[i][1]
        
            chairs.append([higher,lower])
        return chairs

    def rand_map(verbose=False):
        if verbose: print("Start loading map")
        # Return a map object
        out = Resort_Map([], [])
        
        # Allocate chair lifts
        # Use hardcoded chair locations, but change their tops

        bounds = gen_algoth.GROUND.regions.box_region()
        xlen = abs(bounds[0][0] - bounds[1][0])
        ylen = abs(bounds[0][1] - bounds[1][1])

        if verbose: print("Generating chairlifts")
        
        locs = gen_algoth.chair_location(random.randint(2,5))

        for high, low in locs:
            out.make_chair(low, high)
            
        if verbose: print("Allocating trails")
        # Allocate trails
        immutable_peaks = [chair[1] for chair in out.chair_set[:BASE_LIFTS]]
        immutable_bottom = [chair[0] for chair in out.chair_set[:BASE_LIFTS]]

        for i in range(len(out.chair_set)):
            chair = out.chair_set[i]
            if i < BASE_LIFTS:
                for j in range(random.randint(4,7)):
                    out.make_path(chair)
            else:
                nearest = immutable_peaks[0]
                dist = mag(chair[0] - nearest)
                for peak in immutable_peaks[1:]:
                    if mag(peak - chair[0]) < dist:
                        nearest = peak
                        dist = mag(peak - chair[0])
                for j in range(random.randint(1,3)):
                    tmp = np.array([chair[0], nearest])
                    out.make_path(tmp)

                # Repeat process for path to bottom
                nearest = immutable_bottom[0]
                dist = mag(chair[0] - nearest)
                for base in immutable_bottom[1:]:
                    if mag(base - chair[0]) < dist:
                        nearest = base
                        dist = mag(base - chair[0])
                for j in range(random.randint(1,3)):
                    tmp = np.array([nearest, chair[0]])
                    out.make_path(tmp)
                for j in range(random.randint(3,5)):
                    out.make_path(chair)

        return out

    def driver(NGEN=NGEN, CXPB=CXPB, MUTPB=MUTPB, POP_SIZE=POP_SIZE):
        # Initialize our fitness function
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))

        # Set our individual class to be composed of resort maps
        creator.create("Individual", Resort_Map, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()

        # Register a function to make random maps for population generation
        toolbox.register("individual", gen_algoth.rand_map)

        # Register the population
        toolbox.register("population", tools.initRepeat, list, toolbox.individual, n=POP_SIZE)

        toolbox.register("mate", gen_algoth.cross)
        toolbox.register("mutate", gen_algoth.mutate)
        toolbox.register("select", tools.selTournament, tournsize=5)
        toolbox.register("evaluate", gen_algoth.call_fitness)

        pop = toolbox.population()

     
        invalid = [ind for ind in pop if ind.fitness==None]
        fitnesses = list(toolbox.map(toolbox.evaluate, invalid))
        
        for ind, fit in zip(invalid, fitnesses):
            ind.fitness = fit
        
        total_fitness = 0
        progression_avg = []
        progression_max = []
        for g in range(NGEN):
            sys.stdout.write("\rRunning generation " + str(g) + " Average Fitness: {}".format(total_fitness/POP_SIZE) + "\033[K")
            selected = toolbox.select(pop, POP_SIZE)
    
            total_fitness = 0

            # Clone selected
            offspring = list(map(toolbox.clone, selected))
            
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
            fitnesses = list(toolbox.map(toolbox.evaluate, invalid))
            for ind, fit in zip(invalid, fitnesses):
                ind.fitness = fit

            # Replace the population with the offspring
            pop[:] = offspring
            fitness_list = [ind.fitness for ind in pop]
            total_fitness = sum(fitness_list)
            max_fitness = max(fitness_list)

            progression_avg.append(total_fitness/POP_SIZE)
            progression_max.append(max_fitness)
        print("")

        fittest = pop[0]
        fit = fittest.fitness
        for ind in pop[1:]:
            if ind.fitness > fit:
                fit = ind.fitness
                fittest = ind
        return (ind, fit, progression_avg, progression_max)


if __name__ == '__main__':
        
        hi =(gen_algoth.driver())
        #print(hi)
    
