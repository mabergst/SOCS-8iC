# Did some testing with gradients but not quite sure how to translate SebLagues C# code for the gradient
import math

#import matplotlib.pyplot as plt
import numpy as np

z = np.array([[x**2 + y**2 for x in range(20)] for y in range(20)])
x, y = np.meshgrid(range(z.shape[0]), range(z.shape[1]))
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.plot_surface(x, y, z)
#plt.title('z as 3d height map')
#plt.show()
inertia=0.01
dropletxpos=17.1
dropletypos=15.9
def returngradient(map,xpos,ypos):
    coordx=math.floor(xpos)
    coordy=math.floor(ypos)
    internalx=xpos-coordx
    internaly=ypos-coordy
    if xpos<map.shape[0]-1 and ypos<map.shape[1]-1: # how do we erode the two excluded edges?
        corner1 = map[coordx, coordy] #ideally make corner array
        corner2 = map[coordx + 1, coordy]
        corner3 = map[coordx, coordy + 1]
        corner4 = map[coordx + 1, coordy + 1]
        gradx = (corner2-corner1)*(1-internaly)+(corner4-corner3)*internaly #not exactly sure why we do it this way but its correct?
        grady = (corner3 - corner1) * (1 - internalx) + (corner4 - corner2) * internalx
        height = corner1 * (1 - internalx) * (1 - internaly) + corner2 * internalx * (1 - internaly) + corner3 * (1 - internalx) * internaly + corner4 * internalx * internaly
    return (gradx,grady,height)
result=returngradient(z,dropletxpos,dropletypos) #seems to work but changeing xpos ypox to different decimal (same integer) does not change the result so might be unnecessary
print(result)
#ignore rest

# Different decimals give diffrent height, so it is necessary

