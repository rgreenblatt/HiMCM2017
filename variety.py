import numpy as np
from math import acos,pi

def mag(vector):
    return np.linalg.norm(vector)

def FindAngle(vector1, vector2):
    costhet=np.dot(vector1,vector2)/(mag(vector1)*mag(vector2))
    angle=acos(costhet)
    return angle
    
def variety(testruns,testdist, areas):
    nruns=np.sum(testruns)
    nregions=testdist.shape[0]
    trueruns=np.array([0.2*nruns,0.4*nruns,0.4*nruns])
    truedist=np.sum(testdist)*areas/np.sum(areas)
    print([trueruns,testruns])
    anglerun=FindAngle(trueruns,testruns)
    angledist=FindAngle(truedist,testdist)
    error=lambda true,test:abs(test-true)/true
    tupler=(error(pi,angledist),error(pi,anglerun))
    return tupler

def main():
    nruns=20 
    nregions=4
    test1=np.array([0.23*nruns,0.35*nruns,0.42*nruns])
    test2=np.array([4,6,4,6])
    area=np.array([4.001, 6, 4, 6])
    hi=variety(test1,test2, area) 
    print(hi) 

if __name__=="__main__":
    main()
