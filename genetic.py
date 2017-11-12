import numpy as np
import random
import deap
import path as path_lib
import sys

from deap import base, creator, tools, algorithms

from terrain import terrain
from fitness import fitness

NGEN = 10000
CXPB = .6
MUTPB = .03
P1 = .1
P2 = .4
P3 = .4
P4 = .4
BASE_LIFTS = 3

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
        path.trail_set.append(path)
            

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


def mag(a1):
    return np.sqrt(a1.dot(a1))

class gen_algoth:
  
    GROUND = terrain()

    def mutate(child):
        #TODO:Take the top point of some trails. Draw new paths to the bottom. 
        if random.random() < P1:
            gen_algoth.mutate1(child)
        if random.random() < P2:
            gen_algoth.mutate2(child)
        if random.random() < P3:
            gen_algoth.mutate3(child)
        if random.random() < P4:
            gen_algoth.mutate4(child)

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
                child.make_trail(tmp)

            # Repeat process for path to bottom
            nearest = immutable_bottom[0]
            dist = mag(lower - nearest)
            for base in immutable_bottom[1:]:
                if mag(base - lower) < dist:
                    nearest = base
                    dist = mag(lower-nearest)
            for j in range(random.randint(1,2)):
                tmp = np.array([nearest, lower])
                child.make_trail(tmp)
        else:
            if(BASE_LIFTS<len(child.chair_set)-1):
                child.rem_chair()
            
        
    def mutate2(child): # Add/Remove Trails
        choice = random.randint(0,1)
        if choice: # Add Trail
            trails = random.randint(1,4)
            for i in range(trails):
                chair = child.chair_set[random.randint(0, len(child.chair_set)-1)]
                child.make_trail(chair)
        else:
            trails = random.randint(1,3)
            for i in range(trails):
                if child.trail_set:
                    child.trail_set.pop(random.randint(0, len(child.trail_set)-1))


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
        
    def mutate4(child): # Shift Midpoints
        if len(child.trail_set) > 0:
            num_trails = random.randint(2,5)
            num_points = random.randint(2,5)
            for i in range(num_trails):
                trail = child.trail_set[random.randint(len(child.trail_set))]
                for x in range(num_points):
                    if len(trail) > 2:
                        ind = random.randint(1, len(trail) - 2)
                        bottom = trail[-1]
                        curr = trail[ind]
                        delta = (bottom - curr) / 10
        
                        theta = np.pi*(random.random()*90-45)/180
                        delta = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), -np.cos(theta)]]).dot(disp)
                        trail[ind] = curr+delta            

    def cross(parent1,parent2):
        child1 = gen_algoth.cross_helper(parent1,parent2)
        child2 = gen_algoth.cross_helper(parent1,parent2)
        parent1 = child1
        parent2 = child2

    def cross_helper(parent1,parent2):
        chrlens=(len(parent1.chair_set),len(parent2.chair_set))
        chrlen=chrlens[random.randint(0,1)]
        
        trlens=(len(parent1.trail_set),len(parent2.trail_set))
        trllen=trlens[random.randint(0,1)]
        
        chrpars=(parent1.chair_set,parent2.chair_set)
        trlpars=(parent1.trail_set,parent2.trail_set)

        child=Resort_Map([],[])
        watched=[]
        
        for i in range(chrlen):
            index=random.randint(0,1)
            currparent=chrpars[index]
            
            child.chair_set.append(currparent.chair_set[i])
            
            if(BASE_LIFTS <= i): 
                watched.append(child.chair_set[i][0])
            watched.append(child.chair_set[i][1])

        for i in range(trllen):
            for parent in trlpars:
                currtrail=parent[i]
                if currtrail[0] in watched:
                    child.trail_set.append(currtrail)
        return child

    def chair_location(num_chairs):
        point_array = np.transpose(gen_algoth.GROUND.regions.get_random_points(2*num_chairs))
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
                    out.make_trail(chair)
            else:
                nearest = immutable_peaks[0]
                dist = mag(chair[0] - nearest)
                for peak in immutable_peaks[1:]:
                    if mag(peak - chair[0]) < dist:
                        nearest = peak
                        dist = mag(peak - chair[0])
                for j in range(random.randint(1,3)):
                    tmp = np.array([chair[0], nearest])
                    out.make_trail(tmp)

                # Repeat process for path to bottom
                nearest = immutable_bottom[0]
                dist = mag(chair[0] - nearest)
                for base in immutable_bottom[1:]:
                    if mag(base - chair[0]) < dist:
                        nearest = base
                        dist = mag(base - chair[0])
                for j in range(random.randint(1,3)):
                    tmp = np.array([nearest, chair[0]])
                    out.make_trail(tmp)
                for j in range(random.randint(3,5)):
                    out.make_trail(chair)

        return out

    def driver(NGEN=NGEN, CXPB=CXPB, MUTPB=MUTPB):
        # Initialize our fitness function
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))

        # Set our individual class to be composed of resort maps
        creator.create("Individual", Resort_Map, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()

        # Register a function to make random maps for population generation
        toolbox.register("individual", gen_algoth.rand_map)

        # Register the population
        toolbox.register("population", tools.initRepeat, list, toolbox.individual, n=100)

        toolbox.register("mate", gen_algoth.cross)
        toolbox.register("mutate", gen_algoth.mutate)
        toolbox.register("select", tools.selTournament, tournsize=5)
        toolbox.register("evaluate", fitness)

        pop = toolbox.population()

     
        invalid = [ind for ind in pop if ind.fitness==None]
        fitnesses = list(toolbox.map(toolbox.evaluate, invalid))
        
        for ind, fit in zip(invalid, fitnesses):
            ind.fitness = fit
        
        for g in range(NGEN):
            sys.stdout.write("\rRunning generation " + str(g) + "\033[K")
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
            fitnesses = list(toolbox.map(toolbox.evaluate, invalid))
            for ind, fit in zip(invalid, fitnesses):
                ind.fitness = fit

            # Replace the population with the offspring
            pop[:] = offspring
        print("")

        fittest = pop[0]
        fit = fittest.fitness
        for ind in pop[1:]:
            if ind.fitness > fit:
                fit = ind.fitness
                fittest = ind
        return (ind, fit)


if __name__ == '__main__':
    print(gen_algoth.driver())
    
