from random import Random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as pltpip
from numpy.lib.npyio import mafromtxt
from perlin_noise import PerlinNoise


class HeightMapGenerator:
    numOctaves=7
    persistance=0.5
    lacunarity=2
    initialScale=2
    randomizeSeed = True

def randomHeightMap(mapSize):
    return np.random.rand(mapSize, mapSize)

def generateMapTest(nrOfOctaves, mapsize):
    persistence =0.5
    lacunarity = 2
    map=np.array()
    for y in range(mapsize):
        for x in range(mapsize):
            noiseValue=0
            scale = 2
            weight = 1

            for i in range(nrOfOctaves):
                
                xy = Random.randint(-1000, 1000) + [x/mapsize, y/mapsize*scale] 
                noiseValue += PerlinNoise(xy(1),xy(2))*weight
                weight *= persistence
                scale *= lacunarity
            map[y*mapsize+ x] = noiseValue
    return map





