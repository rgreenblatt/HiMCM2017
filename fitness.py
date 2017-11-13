import numpy as np
import variety as var

from terrain import terrain
from region import region
import difficulty as diff
from tMap import Resort_Map

from path import paths as path_lib

import congest

weights = {"regionalVariation" : .33333, "difficulty" : .33333, "congestion" : .33333}
totalPeople = 4000
liftSpeeds = 16.4
descentSpeed = 32808.4
liftChairSize = 4


def feet_to_deg(feet):
	return feet / 364287.

def fitness(individual, ground):

	paths = np.flip(individual.trail_set, axis = 2)
	
	lifts = individual.chair_set
	pathLengths = []
	path_points = []
	for path in paths:
		temp_path = path_lib()
		temp_path.set_points(path)
		single_point = temp_path.calc_locations(20)
		path_points.append(single_point)
		pathLengths.append(ground.length_of_path(np.array(single_point)))
	totalPathLength = np.sum(pathLengths)
	#print(pathLengths)	
	penalty = 0
	
	if(totalPathLength > feet_to_deg(656168)):
		penalty +=(totalPathLength - feet_to_deg(656168))*-.01
	if(totalPathLength < feet_to_deg(524934)):
		penalty += (feet_to_deg(524934) - totalPathLength)*-.01
	if(len(lifts) > 19):
		penalty += (len(lifts) - 19)*-.2
	if(len(lifts) < 3):#feet	
		penalty += (3-len(lifts))*-.4
	
	pathDiff = diff.difficulty(paths,ground)
	green = np.where(pathDiff == 0, 1, 0)
	blue = np.where(pathDiff == 1, 1, 0)
	black = np.where(pathDiff == 2, 1, 0)
	
	#print("Printing pathDiffs")
	#print(pathDiff)

	greenLength = np.sum(green*pathLengths)	
	blueLength = np.sum(blue*pathLengths)	
	blackLength = np.sum(black*pathLengths)
	lengthByDiff = np.array([greenLength, blueLength, blackLength])
	
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

	trailLengthsPerLift = np.zeros((len(lifts))) 
	i=0
	for lift in lifts:
		lengthByLift = 0
		for index in individual.trails_owned(lift):
			lengthByLift+=ground.length_of_path(paths[index])		 
		trailLengthsPerLift[i] = lengthByLift
		i+=1

	liftCapacity = np.array([200]*len(lifts)) #FIXXXXX TODO TODO
	congestScore = congest.congFitness(totalPeople, trailLengthsPerLift,  liftCapacity, liftTimeToTop, skiTimeDown) 
	#print([varietyScores[0],varietyScores[1],congestScore])
	fit = weights["difficulty"]+weights["congestion"]*congestScore+penalty
	return fit
	

