from osgeo import gdal
import numpy as np
import scipy
import os
import sys
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


class terrain:
	def __init__(self):
		gdal.UseExceptions()
		
	def getFileNames(folder,file_ending):
		
		only_files = []

		for root, dirs, files in os.walk(folder):
			for name in files:
				(base, ext) = os.path.splitext(name)
				if ext in file_ending:
					only_files.append(os.path.join(root,name))
		return only_files

	def load_elevation(self,file_location):
		file_names = terrain.getFileNames(file_location,('.img'))
		
		geo = gdal.Open(file_names[0])
		self.data_array = geo.ReadAsArray()
		
		self.x_bounds = (-112.000555555294,-110.999444444905)
		self.y_bounds = (40.9994444447063,42.0005555550957)

		deg_to_feet=110030.

		self.data_resolution = abs(self.x_bounds[1]-self.x_bounds[0])/float(self.data_array.shape[0])*deg_to_feet

		x = np.linspace(self.x_bounds[0],self.x_bounds[1],num=self.data_array.shape[0])
		y = np.linspace(self.y_bounds[1],self.y_bounds[0],num=self.data_array.shape[0])
		self.x_points,self.y_points = np.meshgrid(x,y)

	def height_at_coordinates(self,coordinate):
		bad_coords = np.where(self.x_bounds[0] <= coordinate[0] <= self.x_bounds[1] or self.y_bounds[0] <= coordinate[1] <= self.y_bounds[1], False, True)
		if np.sum(bad_coords) > 1:
			print("Bad coordinates: " + str(numpy.where(bad_coords)))
			coordinate = np.delete(coordinate,numpy.where(bad_coords))

		interp = scipy.interpolate.interp2d(self.x_points,self.y_points,self.data_array,kind='cubic')

		return interp(coordinate)

	def length_of_path(self,path):
		heights = self.height_at_coordinates(path)

		path = np.concatenate((path,heights),axis=1)
		
		distances = np.sqrt(np.square(np.square(path[:-1]-path[1:]),axis=0))

		return np.sum(distances)

	def calc_slopes(self):
		gradients = np.gradient(self.data_array,self.data_resolution)
		return gradients

	def gradient_directions(self):
		pass

	def percent_slopes(self):
		pass

	def visualize_gradients(self):
		gradients = self.calc_slopes()

		fig = plt.figure()
		plt.imshow(np.sqrt(gradients[0]*gradients[0]+gradients[1]*gradients[1]), cmap=cm.BrBG_r)
		plt.axis('off')
		cbar = plt.colorbar(shrink=0.75)
		cbar.set_label('meters')
		plt.show()

	def visualize_elevation(self,flat=False):
		topo = self.data_array
		topo[topo==0] = np.nan
		
		if flat:
			print("test")
			fig = plt.figure(frameon=False)
			plt.imshow(topo, cmap=cm.BrBG_r)
			plt.axis('off')
			cbar = plt.colorbar(shrink=0.75)
			cbar.set_label('meters')
			#plt.savefig('kauai.png', dpi=300, bbox_inches='tight')
			plt.show()

		if not flat:
			fig = plt.figure()
			ax = fig.gca(projection = '3d')
			
			ax.set_zlim(0,10000)

			surf = ax.plot_surface(self.x_points,self.y_points,topo)
			plt.axis('off')
			plt.show()

def main():
	ground = terrain()
	ground.load_elevation("data_terrain/elevation")
	#ground.visualize_elevation(flat=False)
	#ground.calc_slopes()
	#ground.visualize_gradients()

if __name__ == "__main__":
	main()
