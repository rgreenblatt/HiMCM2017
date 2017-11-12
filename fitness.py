import numpy as np
import variety as var
import congest
import path
from terrain import terrain
from region import region

regionBottom = -111.8285
regionTop = -111.806

region1 = 41.0175
region2 = 41.031
region3 = 41.06
region4 = 41.074
region5 = 41.08927
region6 = 41.112
region7 = 41.14

regionX = np.array([region1, region2,region3,region4,region5,region6,region7])
regionY = np.array([regionBottom, regionTop])

fileNameArray1 = ["Regions/region1.csv","Regions/region2.csv","Regions/region3.csv","Regions/region4.csv","Regions/region5.csv","Regions/region6.csv","Regions/region6.csv"]
fileNameArray2 = ["dividers1", "dividers2", "dividers3"]

regions1 = []
for fileName in fileNameArray1:
	regionT = region()
	regionT.load_single_region(fileName)
	regions1.append(regionT) 

regions2 = []
for fileName in fileNameArray2:
	regionT = region()
	regionT.load_single_region(fileName)
	regions2.append(regionT) 

areas = np.zeros((len(regions1), len(regions2)))

for i in range(len(regions1)):
	for k in range(len(regions2)):
		area[i][k] = ground.regions.intersection(regions1[i]).intersection(regions2[k]).area
area = np.flatten(area)


def fitness(weights,partitionAreas, paths, lifts, totalPeople, liftSpeeds, descentSpeed, liftCapacities, areas):
	totalPathLength = #some function here on paths
	if(totalPathLength > 656168 or totalPathLength < 524934 or lift.shape[0] > 19 or lift.shape[0] < 3):#feet
		return -3000
	else:
		
		ground = terrain()
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
		
		penalty = 0
		for path in paths:
			points = path.calc_locations(100)
			x_regions = []
			for i in range(regionX.shape[0]-1):
				x_regions.append(np.where(regionX[i] <= points[0] < regionX[i+1]))
			y_regions = []
			for i in range(regionY.shape[0]-1):
				y_regions.append(np.where(regionY[i] <=	points[1] < regionY[i+1]))
					

			penalty+=np.sum(ground.in_region(path))*-.1
			
		trailLengthsPerLift = #some function probably from terrain here

			
		congestScore = congest.congFitness(totalPeople, trailLengthsPerLift,  liftCapacity, liftTimeToTop, skiTimeDown) 
		return weights["regionalVariation"]*varietyScores[0]+weights["difficulty"]*varietyScores[1]+weights["congestion"]*congestScore
		
		
	
