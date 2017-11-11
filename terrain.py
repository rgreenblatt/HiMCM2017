from osgeo import gdal
import numpy as np
from scipy.interpolate import RectBivariateSpline
import os
import sys
import matplotlib.pyplot as plt
from region import region
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from descartes import PolygonPatch

class terrain:
	def __init__(self):
		gdal.UseExceptions()
		self.load_region("data_terrain/regions")
		
	def getFileNames(folder,file_ending):
		
		only_files = []

		for root, dirs, files in os.walk(folder):
			for name in files:
				(base, ext) = os.path.splitext(name)
				if ext in file_ending:
					only_files.append(os.path.join(root,name))
		return only_files

	def load_region(self,file_location):
		reg = region()
		reg.load_region(file_location)
		self.regions = reg
	
	def in_region(self,points):
		contained = self.regions.in_region(points)
		return contained

	def box_region(self):
		points = np.array(self.regions.points_in)
		
		return np.array([np.min(points,axis=0),np.max(points,axis=0)])

	def visualize_region(self,on_elevation=False):

		fig = plt.figure()

		ax = fig.add_subplot(111, aspect='equal')

		box = self.box_region()
		print(box)	
		ax.set_xlim(box[0,0],box[1,0])
		ax.set_ylim(box[0,1],box[1,1])
	
		if on_elevation:
			topo = self.data_array
			topo[topo==0] = np.nan
			
			plt.imshow(topo, cmap=cm.BrBG_r)
			cbar = plt.colorbar(shrink=0.75)
			cbar.set_label('meters')

		patch = PolygonPatch(self.regions.polygon, facecolor=[0,0,0.5], edgecolor=[1,1,1], alpha=1.0) 
		ax.add_patch(patch) 
		plt.show()			

	def load_elevation(self,file_location):
		file_names = terrain.getFileNames(file_location,('.img'))
		
		geo = gdal.Open(file_names[0])
		self.data_array = np.flip(geo.ReadAsArray(),axis=1)
		
		self.x_bounds = (-112.000555555294,-110.999444444905)
		self.y_bounds = (40.9994444447063,42.0005555550957)

		deg_to_feet=110030.

		self.data_resolution = abs(self.x_bounds[1]-self.x_bounds[0])/float(self.data_array.shape[0])*deg_to_feet

		self.x_vals = np.linspace(self.x_bounds[0],self.x_bounds[1],num=self.data_array.shape[0])
		self.y_vals  = np.linspace(self.y_bounds[0],self.y_bounds[1],num=self.data_array.shape[0])
		self.x_points,self.y_points = np.meshgrid(self.x_vals,self.y_vals)

		self.interp = RectBivariateSpline(self.x_vals,self.y_vals,self.data_array)

		gradients = self.calc_slopes()
		self.gradX = RectBivariateSpline(self.x_vals,self.y_vals,gradients[0])
		self.gradY = RectBivariateSpline(self.x_vals,self.y_vals,gradients[1])

	def height_at_coordinates(self,coordinate):
		return self.interp(coordinate[0],coordinate[1],grid=False)

	def length_of_path(self,path):
		heights = self.height_at_coordinates(path)

		path = np.concatenate((path,heights),axis=1)
		
		distances = np.sqrt(np.square(np.square(path[:-1]-path[1:]),axis=0))

		return np.sum(distances)
	def gradient_at_coordinates(self,coordinate):
		gradX=self.gradX(coordinate[0],coordinate[1],grid=False)
		gradY=self.gradY(coordinate[0],coordinate[1],grid=False)
		
		return np.array([gradX,gradY])

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
			fig = plt.figure(frameon=False)
			plt.imshow(topo, cmap=cm.BrBG_r)
			plt.axis('off')
			cbar = plt.colorbar(shrink=0.75)
			cbar.set_label('meters')
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
	#ground.visualize_elevation(flat=True)
	#ground.calc_slopes()
	#ground.visualize_gradients()

	#print(ground.gradient_at_coordinates(np.transpose(np.array([[-111.2,41],[-111.3,41.01]]))))
	#print(ground.in_region(np.array([[-111,41],[-111.1,41],[-111,41.1],[-111.8,41.1],[-111.83,41.12],[-111.793,41.06],[-111.789,41.08]])))
	ground.visualize_region()

if __name__ == "__main__":
	main()

