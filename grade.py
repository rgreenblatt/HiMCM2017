def grader(paths):
    out=[]
    penalty=0
     
    for path in paths:
        for i in range(1,len(path)-1):
            hm1=terrain.height_from_coordinates(path[i-1])
            h=terrain.height_from_coordinates(path[i])
            hp1=terrain.height_from_coordinates(path[i+1])
            
            hm1=1
            h=1
            hp1=1         
            d1=dist(path[i-1],path[i])
            d2=dist(path[i+1],path[i])
            
            s1=(h-hm1)/d1
            s2=(hp1-h)/d2

            grade=(s1+s2)/2
            if grade<-2:
                penalty+= (-grade-2)*0.1
            if grade>0:
                penalty+=(grade)*0.1
            
    return -penalty
