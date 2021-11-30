import numpy as np
from numpy.lib.twodim_base import tri
from scipy.spatial import Delaunay
import mesh
import GenerateHeightMap as genMap
import Erode

import matplotlib.pyplot as plt

def surf_mesh(heightmap, size):

    map_size = list(heightmap.shape)
    base = (0, 0, 0)
    x_size = size
    y_size = x_size
    dx = x_size / map_size[0]
    dy = y_size / map_size[1]

    vertices = []
    for i in range(map_size[0]):
        for j in range(map_size[1]):
            x_coord = base[0] + dx * i
            y_coord = base[1] + dy * j
            z_coord = base[2] + heightmap[i][j]
            vertices.append([x_coord, y_coord, z_coord])

    vertices = np.array(vertices)

    points_xy = []
    for i in range(len(vertices)):
        points_xy.append([vertices[i, 0], vertices[i, 1]])
    points_xy = np.array(points_xy)

    tri = Delaunay(points_xy).simplices

    
    return vertices, tri

heightMap = genMap.generateMapTest(4,1000)
x, y = np.meshgrid(range(heightMap.shape[0]), range(heightMap.shape[1]))

#Copy
erodedMap = heightMap

erodedMap = Erode.Erode(100,erodedMap)

fig = plt.figure(figsize=plt.figaspect(0.5))

ax = fig.add_subplot(1, 2, 1, projection='3d')
ax.plot_surface(x, y, heightMap)

ax = fig.add_subplot(1, 2, 2, projection='3d')
ax.plot_surface(x, y, erodedMap)

plt.show()