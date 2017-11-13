import numpy as np
from terrain import terrain

def dist(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5

def deg_to_feet(deg_in):
    for i in range(len(deg_in)):
        deg_in[i] = deg_in[i] * 11030.
    return deg_in

def difficulty(paths,ground):
    out=[]
   
    for path in paths:
   
        gradients = np.sqrt(np.sum(np.square(ground.gradient_along_path(path)),axis=0))

        maximum = np.max(gradients)        

        print(maximum)

        if maximum<0.25:
            out.append(0)
        elif maximum>0.25 and maximum<0.4:
            out.append(1)
        else:
            out.append(2)
    
    return out


