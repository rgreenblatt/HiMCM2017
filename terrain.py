from osgeo import gdal, ogr, osr
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
		self.load_elevation("data_terrain/elevation")
	
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

	def GetExtent(gt,cols,rows):
		''' Return list of corner coordinates from a geotransform
	
			@type gt:   C{tuple/list}
			@param gt: geotransform
			@type cols:   C{int}
			@param cols: number of columns in the dataset
			@type rows:   C{int}
			@param rows: number of rows in the dataset
			@rtype:    C{[float,...,float]}
			@return:   coordinates of each corner
		'''
		ext=[]
		xarr=[0,cols]
		yarr=[0,rows]
		
		for px in xarr:
			for py in yarr:
				x=gt[0]+(px*gt[1])+(py*gt[2])
				y=gt[3]+(px*gt[4])+(py*gt[5])
				ext.append([x,y])
			yarr.reverse()
		return ext

	def ReprojectCoords(coords,src_srs,tgt_srs):
		''' Reproject a list of x,y coordinates.
			
			@type geom:     C{tuple/list}
			@param geom:    List of [[x,y],...[x,y]] coordinates
			@type src_srs:  C{osr.SpatialReference}
			@param src_srs: OSR SpatialReference object
			@type tgt_srs:  C{osr.SpatialReference}
			@param tgt_srs: OSR SpatialReference object
			@rtype:         C{tuple/list}
			@return:        List of transformed [[x,y],...[x,y]] coordinates
		'''
		trans_coords=[]
		transform = osr.CoordinateTransformation( src_srs, tgt_srs)
		for x,y in coords:
			x,y,z = transform.TransformPoint(x,y)
			trans_coords.append([x,y])
		return trans_coords
	def get_bounds(ds):	
		gt=ds.GetGeoTransform()
		cols = ds.RasterXSize
		rows = ds.RasterYSize
		ext=terrain.GetExtent(gt,cols,rows)
		
		src_srs=osr.SpatialReference()
		src_srs.ImportFromWkt(ds.GetProjection())
		#tgt_srs=osr.SpatialReference()
		#tgt_srs.ImportFromEPSG(4326)
		tgt_srs = src_srs.CloneGeogCS()
		
		geo_ext=terrain.ReprojectCoords(ext,src_srs,tgt_srs)
		return [geo_ext[0],geo_ext[2]]

	def load_elevation(self,file_location):
		print("Loading Elevation Data")
		file_names = terrain.getFileNames(file_location,('.img'))
		
		deg_to_feet=110030.
		
		self.overall_box = self.regions.box_region()
		
		data_array = []
		x_bounds = []
		y_bounds = []
		data_resolution = []
		x_vals = []
		y_vals = []
		x_points = []
		y_points = []
		interp = []
		gradients = []
		gradX = []
		gradY = []

		for single_name in file_names:
			sys.stdout.write('\rStarted Loading file: ' + single_name + '\033[K')
			geo = gdal.Open(single_name)
			data_array_single = geo.ReadAsArray()
			data_array_single = np.transpose(data_array_single)
			sys.stdout.write('\rCalculating bounds of ' + single_name + '\033[K')			
			bounds = terrain.get_bounds(geo)		

			if bounds[0][0] < bounds[1][0]:
				x_bounds_single = (bounds[0][0],bounds[1][0])
			else:
				x_bounds_single = (bounds[1][0],bounds[0][0])
				data_array_single = np.flip(data_array_single,axis=1)			

			if bounds[0][1] < bounds[1][1]:
				y_bounds_single = (bounds[0][1],bounds[1][1])
			else:
				y_bounds_single = (bounds[1][1],bounds[0][1])
				data_array_single = np.flip(data_array_single,axis=1)
	

			sys.stdout.write('\rGenerating point coordinates for ' + single_name + '\033[K')

			data_resolution_single = abs(x_bounds_single[1]-x_bounds_single[0])/float(data_array_single.shape[0])*deg_to_feet
			data_resolution.append(data_resolution_single)
	
			x_vals_single = np.linspace(x_bounds_single[0],x_bounds_single[1],num=data_array_single.shape[0])
			y_vals_single = np.linspace(y_bounds_single[0],y_bounds_single[1],num=data_array_single.shape[0])

			x,y = np.meshgrid(x_vals_single,y_vals_single)

			included_points = np.where(np.logical_and(np.logical_and(self.overall_box[0,0] <= x,self.overall_box[1,0] > x),np.logical_and(self.overall_box[0,1] <= y,self.overall_box[1,1] > y)))

			x = x[included_points]
			y = y[included_points]
			x_points.append(x)
			y_points.append(y)
			
			x_indices = np.where(np.logical_and(self.overall_box[0,0] <=x_vals_single,self.overall_box[1,0] > x_vals_single))
			y_indices = np.where(np.logical_and(self.overall_box[0,1] <=y_vals_single,self.overall_box[1,1] > y_vals_single))
			x_vals_single = x_vals_single[x_indices]
			y_vals_single = y_vals_single[y_indices]
			x_vals.append(x_vals_single)
			y_vals.append(y_vals_single)		

			data_array_single = data_array_single[x_indices]
			data_array_single = data_array_single[:,y_indices[0]]
			data_array.append(data_array_single)		

			x_bounds_single = [max(x_bounds_single[0],self.overall_box[0,0]),min(x_bounds_single[1],self.overall_box[1,0])]
			y_bounds_single = [max(y_bounds_single[0],self.overall_box[0,1]),min(y_bounds_single[1],self.overall_box[1,1])]
			x_bounds.append(x_bounds_single)
			y_bounds.append(y_bounds_single)
			
			sys.stdout.write('\rBuilding interpolation function for ' + single_name + ' heights\033[K')

			interp.append(RectBivariateSpline(x_vals_single,y_vals_single,data_array_single))
	
			sys.stdout.write('\rDifferentiating and interpolating gradients for ' + single_name + '\033[K')

			gradients_single = terrain.calc_slopes(data_array_single,data_resolution_single)
			gradients.append(gradients_single)
			gradX.append(RectBivariateSpline(x_vals_single,y_vals_single,gradients_single[0]))
			gradY.append(RectBivariateSpline(x_vals_single,y_vals_single,gradients_single[1]))
			
			sys.stdout.write('\rDone loading ' + single_name + '\n')

		self.data_array = data_array
		self.x_bounds = x_bounds
		self.y_bounds = y_bounds
		self.data_resolution = data_resolution
		self.x_vals = x_vals
		self.y_vals = y_vals
		self.x_points = x_points
		self.y_points = y_points
		self.interp = interp
		self.gradients = gradients
		self.gradX = gradX
		self.gradY = gradY

		print("Done loading regions. Loaded " + str(len(file_names)) + " regions")

	def sort_by_data_set(self,coordinates):
		out_array = []
		for x,y in zip(self.x_bounds, self.y_bounds):
			indices = np.where(np.logical_and(np.logical_and(x[0] <= coordinates[0], coordinates[0] < x[1]), np.logical_and(y[0] <= coordinates[1], coordinates[1] < y[1])))
			out_array.append([coordinates[:,indices[0],indices[1]],indices])
		return out_array

	def height_at_coordinates(self,coordinate):
		interpolated = np.zeros((coordinate.shape[1],coordinate.shape[2]))

		coordinate = self.sort_by_data_set(coordinate)
		for area,interpolater in zip(coordinate,self.interp):
			inter_value = interpolater(area[0][0],area[0][1],grid=False)
			interpolated[area[1][0],area[1][1]] = inter_value
		return interpolated

	def length_of_path(self,path):
		heights = self.height_at_coordinates(path)

		path = np.concatenate((path,[heights]),axis=0)
		
		distances = np.sqrt(np.sum(np.square(path[:-1]-path[1:]),axis=0))

		return np.sum(distances)


	def gradient_at_coordinates(self,coordinate):
		gradX = np.zeros((coordinate.shape[1],coordinate.shape[2]))
		gradY = np.zeros((coordinate.shape[1],coordinate.shape[2]))
		
		coordinate = self.sort_by_data_set(coordinate)
		for area,gradFuncX,gradFuncY in zip(coordinate,self.gradX,self.gradY):
			gradX[area[1][0],area[1][1]]=gradFuncX(area[0][0],area[0][1],grid=False)
			gradY[area[1][0],area[1][1]]=gradFuncY(area[0][0],area[0][1],grid=False)
		
		return np.array([gradX,gradY])

	def calc_slopes(data_array,data_resolution):
		gradients = np.gradient(data_array,data_resolution)
		return gradients

def main():
	ground = terrain()
	#ground.load_elevation("data_terrain/elevation")
	#ground.visualize_elevation(flat=True)
	#ground.calc_slopes()
	#ground.visualize_gradients()

	#print(ground.gradient_at_coordinates(np.transpose(np.array([[-111.2,41],[-111.3,41.01]]))))
	#print(ground.in_region(np.array([[-111,41],[-111.1,41],[-111,41.1],[-111.8,41.1],[-111.83,41.12],[-111.793,41.06],[-111.789,41.08]])))
	#ground.visualize_region(on_elevation=True)
	#ground.visualize_resort()

if __name__ == "__main__":
	main()

