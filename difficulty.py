import numpy as np
from terrain import terrain

def dist(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5

def difficulty(paths,ground):
    out=[]
   
    for path in paths:
        maxer=0
    
        heights = ground.height_at_coordinates(np.reshape(path,(2,-1,1)))

        for i in range(1,len(path)-1):
            hm1=heights[i-1]
            h=heights[i]
            hp1=heights[i+1]
            
            hm1=1
            h=1
            hp1=1         
            d1=dist(path[i-1],path[i])
            d2=dist(path[i+1],path[i])
            
            s1=abs(h-hm1)/d1
            s2=abs(hp1-h)/d2

            grade=(s1+s2)/2
            
            if grade>maxer:
                maxer=grade
    
        if maxer<0.25:
            out.append(0)
        elif maxer>0.25 and maxer<0.4:
            out.append(1)
        else:
            out.append(2)
    
    return out


