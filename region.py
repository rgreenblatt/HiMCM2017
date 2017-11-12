import numpy
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import os
import numpy as np
import sys

class region:
	def __init__(self):
		pass

	def getFileNames(folder,file_ending):

                only_files = []

                for root, dirs, files in os.walk(folder):
                        for name in files:
                                (base, ext) = os.path.splitext(name)
                                if ext in file_ending:
                                        only_files.append(os.path.join(root,name))
                return only_files

	def load_single_region(self,name_in, names_out = None):
		try:
			self.points_in = np.genfromtxt(name_in,delimiter=',')
		except Exception as e:
			print("Failed to load file " + name_in + ". Error " + str(e)) #This was added because Ryan is bad at filenames
		self.points_out = []
		if names_out != None:
			for name in names_out:
				self.points_out.append(np.genfromtxt(name,delimiter=',')[::-1])
		self.polygon = Polygon(self.points_in,self.points_out)

	def get_random_points(self,number_of_points):
		valid_points = []
		bounds = self.box_region()
		while len(valid_points) < number_of_points:
			points=np.array([np.random.uniform(bounds[0][0],bounds[1][0],number_of_points-len(valid_points)),np.random.uniform(bounds[0][1],bounds[1][1],number_of_points-len(valid_points))])
			points = np.transpose(points)
			valid_points.extend(points[np.where(self.in_region(points))])
		return valid_points
		

	def box_region(self):
		points = np.array(self.points_in)
		return np.array([np.min(points,axis=0),np.max(points,axis=0)])

	def load_region(self,file_location):
		files = region.getFileNames(file_location,".csv")
		
		points_in = []
		points_out = []
		for single_file in files:
			sys.stdout.write('\rLoading region: ' + single_file + '\033[K')
			if 'in' in single_file and 'out' not in single_file:
				point_set=np.genfromtxt(single_file,delimiter=',')
				if np.isnan(point_set).any():
					print("Issue with csv: " + single_file)
				points_in.extend(point_set)
			elif 'out' in single_file:
				point_set=np.genfromtxt(single_file,delimiter=',')[::-1]
				if np.isnan(point_set).any():
					print("Issue with csv: " + single_file)
				points_out.extend(point_set)
		self.points_in = points_in
		self.points_out = points_out
		self.polygon = Polygon(points_in,[points_out])

	def in_region(self,check_points):
		contained = []
		for point in check_points:
			loc = Point(point)
			contained.append(self.polygon.contains(loc))
		contained = numpy.array(contained)
		return contained

	def intersection(self,otherA,otherB):
		poly = otherA.polygon.intersection(otherB.polygon)
		return poly.intersection(self.polygon)
		
def main():
	reg = region()
	#print(reg.in_region(numpy.array([[1,1.5],[0.5,0.5],[1.3,1.4],[2,1.5]])))

if __name__ == "__main__":
	main()
