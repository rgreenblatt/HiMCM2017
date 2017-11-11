import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def main():

    X = np.arange(-5, 5, 0.25)
    xlen = len(X)
    Y = np.arange(-5, 5, 0.25)
    ylen = len(Y)
    X, Y = np.meshgrid(X, Y)
    R = X**2 + Y**2
    Z = -R


    xs=X[20][10:]
    ys=Y[20][10:]
    zs=Z[20][10:]

    mountain=(X,Y,Z)
    runs=runs=[(xs,ys,zs,'g')]
    mtnplot(mountain,runs)

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

if __name__=="__main__":
    main()
