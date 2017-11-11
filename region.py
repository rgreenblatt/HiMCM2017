import numpy
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class region:
	def __init__(self,points):
		self.points = points
		self.polygon = Polygon(points)

	def in_region(self,check_points):
		contained = []
		for point in check_points:
			loc = Point(point)
			contained.append(self.polygon.contains(loc))
		contained = numpy.array(contained)
		return contained
def main():
	reg = region(numpy.array([[1,1],[2,2],[3,1]]))
	print(reg.in_region(numpy.array([[1,1.5],[0.5,0.5],[1.3,1.4],[2,1.5]])))

if __name__ == "__main__":
	main()
