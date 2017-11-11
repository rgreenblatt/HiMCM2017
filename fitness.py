import numpy as np
import variety as var
import congest
import path
import terrain

def fitness(weights,partitionAreas, paths, lifts, totalPeople, liftSpeeds, descentSpeed, liftCapacities):
	totalPathLength = #some function here on paths
	if(totalPathLength > 656168 or totalPathLength < 524934 or lift.shape[0] > 19 or lift.shape[0] < 3):#feet
		return -3000
	else:
		
		ground = terrain.terrain()
		lengthsPerPartition = #some function here on paths (probably in terrain.py as it needs partition data)
		
		numberOfEachDifficulty = #some function here on paths which judges difficulty
		varietyScores = var.variety(numberOfEachDifficulty, lengthsPerPartition, partitionAreas)
		
		liftDistance = []
		skiTimeDown = []
		for lift in lifts:
			Xcoords = np.linspace(lift[0][0], lift[1][0], 300)	
			Ycoords = np.linspace(lift[0][1], lift[1][1], 300)
			#liftPath = np.swapaxes(np.array([Xcoords, Ycoords]), 0, 1)

			liftDistance.append(ground.length_of_path(np.array([Xcoords, Ycoords])))
			elevations = ground.height_at_coordinates(np.array([[lift[0][0], lift[1][0]], [lift[0][1], lift[1][1]]]))
			skiTimeDown.append(abs((elevations[1] - elevations[0])/descentSpeed))
		liftTimeToTop = np.array(liftDistance)/liftSpeeds
		
		
		trailLengthsPerLift = #some function probably from terrain here

			
		congestScore = congest.congFitness(totalPeople, trailLengthsPerLift,  liftCapacity, liftTimeToTop, skiTimeDown) 
		return weights["regionalVariation"]*varietyScores[0]+weights["difficulty"]*varietyScores[1]+weights["congestion"]*congestScore
		
		
	
