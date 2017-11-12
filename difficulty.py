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
   
        heights = ground.height_at_coordinates(np.reshape(np.transpose(path),(2,-1,1)))

        grades = []

        path = deg_to_feet(path)

        for i in range(1,len(path)-1):
            hm1=heights[i-1]
            h=heights[i]
            hp1=heights[i+1]
            
            d1=dist(path[i-1],path[i])
            d2=dist(path[i+1],path[i])
            
            print(d1)

            s1=abs(h-hm1)/d1
            s2=abs(hp1-h)/d2

            grades.append((s1+s2)/2)
        maximum = np.max(grades)        

        print(maximum)

        if maximum<0.25:
            out.append(0)
        elif maximum>0.25 and maximum<0.4:
            out.append(1)
        else:
            out.append(2)
    
    return out


