import numpy as np
from scipy.interpolate import splprep, splev

import matplotlib.pyplot as plt

class paths:
	def __init__(self,points = None):
		self.spline = None
		self.resolution = 100
		if points != None:
			self.set_points(points)

	def set_points(self,points):
		self.point_array = points
		self.spline, u = splprep(points,s=0)

	def set_resolution(resolution):
		self.resolution = resolution

	def draw_spline(self):
		locations = self.calc_locations(self.resolution)
		fig, ax = plt.subplots()
		ax.plot(self.point_array[0],self.point_array[1],'bo')
		ax.plot(locations[0],locations[1], 'r-')
		plt.show()

	def calc_locations(self,num_points=None):
		if num_points == None:
			num_points = self.resolution
		u = np.linspace(0,1,num=num_points)
		new_points = splev(u,self.spline)
		return new_points

	def find_point(self,point):
		return splev(point,self.spline)

def main():
	path = paths()

	path.set_points(np.transpose(np.array([[1,1],[1,2],[1,4],[2,3],[2,2]])))
	path.draw_spline()

if __name__ == "__main__":
	main()
