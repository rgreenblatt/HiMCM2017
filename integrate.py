import numpy as np
from variety import mag
import matplotlib.pyplot as plt
f=lambda point:-(point[0]**2)-(point[1]**2)+50
grad= lambda point:np.array((-2*point[0],-2*point[1]))

end=np.array((5,5))

current=np.array((-0.1,0.1))
dt=0.001
out=[]
for i in range(7000):
    deriv=0.5*(grad(current)/mag(grad(current)**1))+10*((1/f(current))*(end-current)/(mag(end-current)**1))
    normc=mag(deriv)
    unit=(deriv/normc)
    current=current+unit*dt
    out.append(current)

hello=np.array(out)  
graph=np.transpose(hello)
plt.plot(graph[0],graph[1])

plt.show()
