import numpy as np
from terrain import terrain
from genetic import BASEH
import random 
from genetic import Resort_Map  


def cross(parent1,parent2):
        
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
        
        if(ground.height_from_coordinates(chair_set[i][0])>BASEH): 
            watched.append(chair_set[i][0])
        watched.append(chair_set[i][1])

    for i in range(trllen):
        for parent in trlpars:
            currtrail=parent[i]
            if currtrail[1] in watched:
                child.trail_set.append(currparent.trail_set[i])
    return child
    

            

