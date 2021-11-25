import numpy as np
from stl import mesh
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

import vtkplotlib as vpl


def surf_mesh(heightmap_file_name, size):
    heightmap = np.load(heightmap_file_name+'.npy')
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

    tri = Delaunay(points_xy)

    polys = tri.points[tri.vertices].tolist()
    for i in range(len(polys)):
        for j in range(len(polys[0])):
            polys[i][j].append(vertices[tri.vertices[i][j]][2])

    return vertices, polys


def save_mesh_2_stl(polys, filename):
    data = np.zeros(len(polys), dtype=mesh.Mesh.dtype)
    for i in range(len(polys)):
        tri1 = [polys[i][0][0], polys[i][0][1], polys[i][0][2]]
        tri2 = [polys[i][1][0], polys[i][1][1], polys[i][1][2]]
        tri3 = [polys[i][2][0], polys[i][2][1], polys[i][2][2]]
        data["vectors"][i] = np.array([tri1, tri2, tri3])
    m = mesh.Mesh(data)
    m.save(filename+'.stl')


def plot_stl(mesh):
    # figure = plt.figure()
    # axes = mplot3d.Axes3D(figure)
    # axes.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh.vectors))
    #
    # # Auto scale to the mesh size
    # scale = mesh.points.flatten()
    # axes.auto_scale_xyz(scale, scale, scale)

    # Plot the mesh
    vpl.mesh_plot(mesh)

    # Show the figure
    vpl.show()


if __name__ == '__main__':
    # heightmap = np.load('heightmap.npy')
    heightmap_file_name = 'heightmap'
    vertices, polys = surf_mesh(heightmap_file_name, 2)
    save_mesh_2_stl(polys, 'original')

    mesh_original = mesh.Mesh.from_file('original.stl')
    plot_stl(mesh_original)

    heightmap_file_name = 'heightmap1'
    vertices, polys = surf_mesh(heightmap_file_name, 1)
    save_mesh_2_stl(polys, 'small')

    mesh_small = mesh.Mesh.from_file('small.stl')
    plot_stl(mesh_small)