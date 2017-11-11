import numpy as np
def liftUses(totalPeople, lengthsPerLift):
	peoplePerLift = totalPeople*lengthsPerLift/np.sum(lengthsPerLift)
	return liftUses

def congFitness(peoplePerLift, liftCapacity, liftTimeToTop, skiTimeDown):
	pMountain = liftCapacity + liftCapacity*skiTimeDown/LiftTimeToTop
	pLine = peoplePerLift - pMountain
	if(pLine>0):
		propSkiing = skiTimeDown/(skiTimeDown + liftTimeToTop + pLine*liftTimeToTop/liftCapacity)
	else:
		propSkiing = skiTimeDown/(skiTimeDown + liftTimeToTop)
	return np.sum(propSkiing*peoplePerLift)/np.sum(peoplePerLift)
