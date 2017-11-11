import numpy as np
def liftUses(totalPeople, lengthsPerLift):
	peoplePerLift = totalPeople*lengthsPerLift/np.sum(lengthsPerLift)
	return peoplePerLift

def congFitness(totalPeople, lengthsPerLift, liftCapacity, liftTimeToTop, skiTimeDown):
	peoplePerLift = liftUses(totalPeople, lengthsPerLift)
	pMountain = liftCapacity + liftCapacity*skiTimeDown/liftTimeToTop
	pLine = peoplePerLift - pMountain
	propSkiing = np.where(pLine>0, skiTimeDown/(skiTimeDown + liftTimeToTop + pLine*liftTimeToTop/liftCapacity), skiTimeDown/(skiTimeDown + liftTimeToTop))
	return np.sum(propSkiing*peoplePerLift)/np.sum(peoplePerLift)
def main():
	print(congFitness(600, np.array([10, 15, 20]), np.array([90, 100, 110]), np.array([9, 10, 11]), np.array([3, 3, 3])))


if __name__=="__main__":
    main()
