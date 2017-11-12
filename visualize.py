import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from descartes import PolygonPatch
from region import region
from paths import path as path_lib

def visualize_elevation(ground,flat=False,x_vals=None,y_vals=None,image_resolution=(512,512)):
        if x_vals == None:
            x_vals = np.linspace(ground.overall_box[0,0],ground.overall_box[1,0],image_resolution[0])
            y_vals = np.linspace(ground.overall_box[0,1],ground.overall_box[1,1],image_resolution[1])
        x,y=np.meshgrid(x_vals,y_vals)
        topo = ground.height_at_coordinates(np.array([x,y]))
        topo[topo==0] = np.nan
        if flat:
            fig = plt.figure(frameon=False)
            ax = fig.add_subplot(111, aspect='equal')

            ax.set_xlim(ground.overall_box[0,0],ground.overall_box[1,0])
            ax.set_ylim(ground.overall_box[0,1],ground.overall_box[1,1])
            plt.imshow(topo, extent=[ground.overall_box[0,0],ground.overall_box[1,0],ground.overall_box[1,1],ground.overall_box[0,1]], cmap=cm.BrBG_r)
            cbar = plt.colorbar(shrink=0.75)
            cbar.set_label('feet')
            plt.show()

        if not flat:
            fig = plt.figure()
            ax = fig.gca(projection = '3d')

            ax.set_zlim(0,10000)

            surf = ax.plot_surface(x,y,topo)
            plt.axis('off')
            plt.show()

def visualize_region(ground,on_elevation=True,image_resolution=(512,512))
    
    print("Visualizing Region")

    fig = plt.figure()

    ax = fig.add_subplot(111, aspect='equal')

    ax.set_xlim(ground.overall_box[0,0],ground.overall_box[1,0])
    ax.set_ylim(ground.overall_box[0,1],ground.overall_box[1,1])

    if on_elevation:
        print("Getting elevation data")
        x_vals = np.linspace(ground.overall_box[0,0],ground.overall_box[1,0],image_resolution[0])
        y_vals = np.linspace(ground.overall_box[0,1],ground.overall_box[1,1],image_resolution[1])
        x,y=np.meshgrid(x_vals,y_vals)
        topo = ground.height_at_coordinates(np.array([x,y]))
        topo[topo==0] = np.nan

        print("Adding elevation data to plot")
        plt.imshow(topo, extent=[ground.overall_box[0,0],ground.overall_box[1,0],ground.overall_box[1,1],ground.overall_box[0,1]], cmap=cm.BrBG_r)
        cbar = plt.colorbar(shrink=0.75)
        cbar.set_label('feet')

    print("Adding regions")
    patch = PolygonPatch(self.regions.polygon, facecolor=[0,0,0.5], edgecolor=[1,1,1], alpha=0.5)
    ax.add_patch(patch)
    print("Showing plot")
    plt.ylabel('Latitude Degrees North')
    plt.xlabel('Longitude Degrees West')
    plt.show()

def visualize_resort(ground,resort,image_resolution=(512,512)):
    print("Visualizing Full Resort")

    fig = plt.figure()

    ax = fig.add_subplot(111, aspect='equal')

    ax.set_xlim(ground.overall_box[0,0],ground.overall_box[1,0])
    ax.set_ylim(ground.overall_box[0,1],ground.overall_box[1,1])

    print("Getting elevation data")
    x_vals = np.linspace(ground.overall_box[0,0],ground.overall_box[1,0],image_resolution[0])
    y_vals = np.linspace(ground.overall_box[0,1],ground.overall_box[1,1],image_resolution[1])
    x,y=np.meshgrid(x_vals,y_vals)
    topo = ground.height_at_coordinates(np.array([x,y]))
    topo[topo==0] = np.nan

    print("Adding elevation data to plot")
    plt.imshow(topo, extent=[ground.overall_box[0,0],ground.overall_box[1,0],ground.overall_box[1,1],ground.overall_box[0,1]], cmap=cm.BrBG_r)
    cbar = plt.colorbar(shrink=0.75)
    cbar.set_label('feet')

    print("Adding regions")
    patch = PolygonPatch(self.regions.polygon, facecolor=[0,0,0.5], edgecolor=[1,1,1], alpha=0.25)
    ax.add_patch(patch)

    print("Adding Ski Lifts")

    print("Adding slopes")

    print("Showing plot")
    plt.ylabel('Latitude Degrees North')
    plt.xlabel('Longitude Degrees West')
    plt.show()

 def visualize_gradients(self,x_vals=None,y_vals=None,image_resolution=(512,512)):
        #gradients = self.calc_slopes()
        if x_vals == None:
            x_vals = np.linspace(self.overall_box[0,0],self.overall_box[1,0],image_resolution[0])
            y_vals = np.linspace(self.overall_box[0,1],self.overall_box[1,1],image_resolution[1])
        x,y=np.meshgrid(x_vals,y_vals)
        gradients = self.gradient_at_coordinates(np.array([x,y]))
        gradients[gradients == 0] = None
        fig = plt.figure()
        plt.imshow(np.sqrt(gradients[0]*gradients[0]+gradients[1]*gradients[1]), cmap=cm.BrBG_r)
        plt.axis('off')
        cbar = plt.colorbar(shrink=0.75)
        cbar.set_label('meters')
        plt.show()

def mtnplot(mountain,runs):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    
    surf = ax.plot_surface(mountain[0],mountain[1],mountain[2], facecolors=np.full(mountain[0].shape,'w'), linewidth=0)

    ax.w_zaxis.set_major_locator(LinearLocator(6))

    for element in runs:
        ax.plot(element[0],element[1],element[2],element[3])
    ax.set_facecolor('black')
    
    ax.set_zlim(-20,0)
    plt.axis('off')
    plt.show()

def main():
    pass

if __name__=="__main__":
    main()
