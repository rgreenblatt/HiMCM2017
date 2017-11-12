import numpy as np
import variety as var
import congest
from path import paths as path_lib
from terrain import terrain
from region import region
import difficulty as diff
from tMap import Resort_Map

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
fileNameArray2 = ["Regions/dividers1.csv", "Regions/dividers2.csv", "Regions/dividers3.csv"]

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

reg = region()
reg.load_region('data_terrain/regions')

area = np.zeros((len(regions1),len(regions2)))

for i in range(len(regions1)):
	for k in range(len(regions2)):
		area[i][k] = reg.intersection(regions1[i],regions2[k]).area
areas = area.flatten()

weights = {"regionalVariation" : .33333, "difficulty" : .33333, "congenstion" : .33333}
totalPeople = 4000
liftSpeeds = 100
descentSpeed = 100

def feet_to_deg(feet):
	return feet / 11030.

def fitness(individual, ground):
	paths = individual.trail_set
	lifts = individual.chair_set
	pathLengths = []
	path_points = []
	for path in paths:
		temp_path = path_lib()
		temp_path.set_points(np.transpose(path))
		single_point = temp_path.calc_locations()
		path_points.append(single_point)
		temp_array = np.reshape(np.transpose(single_point),(2,-1,1))
		pathLengths.append(ground.length_of_path(temp_array))
	totalPathLength = np.sum(pathLengths)
	
	penalty = 0
	
	if(totalPathLength > feet_to_deg(656168)):
		penalty +=(totalPathLength - feet_to_deg(656168))*-.01
	if(totalPathLength < feet_to_deg(524934)):
		penalty += (feet_to_deg(524934) - totalPathLength)*-.01
	if(len(lifts) > 19):
		penalty += (len(lifts) - 19)*-.2
	if(len(lifts) < 3):#feet	
		penalty += (3-len(lifts))*-.4
	
	#finds lengths of trails in each partition
	lengthsByRegion = np.zeros((regionX.shape[0]+1,regionY.shape[0]+1))
	for path,points in zip(paths,path_points):
			
		tmp_pnt = np.array(points)
		x_regions = []
		x_regions.append(points[0]<regionX[0])
		for i in range(regionX.shape[0]-1):
			x_regions.append(np.logical_and(regionX[i] <= points[0], points[0] < regionX[i+1]))
		#print((regionX[:-1] <= np.repeat([points],6,axis=0) < regionX[1:]))
		x_regions.append(points[0] >= regionX[-1])
		
		y_regions = []
		y_regions.append(points[1]<regionY[0])
		for i in range(regionY.shape[0]-1):
			y_regions.append(np.logical_and(regionY[i] <= points[1], points[1] < regionY[i+1]))
	
		y_regions.append(points[1] >= regionY[-1])
		
		for xReg,i in zip(x_regions,range(len(x_regions))):
			for yReg, k in zip(y_regions,range(len(y_regions))):
				#where both xReg and yReg, get points and find total length
				pointIndex = np.where(np.logical_and(xReg, yReg))

				contiguous = np.split(pointIndex,np.where(np.diff(pointIndex)!=1)[0]+1)

				for indices in contiguous:
					temp_path = np.reshape(tmp_pnt[:,indices],(2,-1,1))
					lengthsByRegion[i,k]+=ground.length_of_path(temp_path)
				
		penalty+=np.sum(ground.in_region(np.transpose(points)))*-.1

	print(paths)
	
	pathDiff = diff.difficulty(paths,ground)
	green = np.where(pathDiff == 0, 1, 0)
	blue = np.where(pathDiff == 1, 1, 0)
	black = np.where(pathDiff == 2, 1, 0)

	#print(pathDiff)

	greenLength = np.sum(green*pathLengths)	
	blueLength = np.sum(blue*pathLengths)	
	blackLength = np.sum(black*pathLengths)
	lengthByDiff = np.array([greenLength, blueLength, blackLength])
	
	#print(lengthByDiff)
	#print(lengthsByRegion)
	#print(areas)
	
	varietyScores = var.variety(lengthByDiff, lengthsByRegion, areas)

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
	

		
	trailLengthsPerLift = 10 #TODO: some function probably from terrain here

		
	congestScore = congest.congFitness(totalPeople, trailLengthsPerLift,  liftCapacity, liftTimeToTop, skiTimeDown) 
	return weights["regionalVariation"]*varietyScores[0]+weights["difficulty"]*varietyScores[1]+weights["congestion"]*congestScore+penalty
	
	

