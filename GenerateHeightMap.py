import random
import numpy as np
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

    x = np.arange(mapsize*mapsize)
    x = x.reshape((mapsize, mapsize))
    heightMap = np.zeros_like(x)
    randObj = random.SystemRandom()

    noise1 = PerlinNoise(octaves=3)
    noise2 = PerlinNoise(octaves=6)
    noise3 = PerlinNoise(octaves=12)
    noise4 = PerlinNoise(octaves=24)

    offset = np.arange(nrOfOctaves)
    for i in range(nrOfOctaves):
        offset[i] = randObj.randint(-1000, 1000)
    

    for y in range(mapsize):
        for x in range(mapsize):
            scale = 0.2
            weight = 1

            noise_val = noise1([x/(5*mapsize), y/(5*mapsize)])
            noise_val += 0.5 * noise2([x/(3*mapsize), y/(3*mapsize)])
            noise_val += 0.05 * noise3([x/(2*mapsize), y/(2*mapsize)])
            noise_val += 0.005 * noise4([x/mapsize, y/mapsize])
            heightMap[y, x] = noise_val*1000
    
    #Normalize heightmap
    minElement = np.amin(heightMap)
    heightMap -= minElement
    maxElement = np.amax(heightMap)
    heightMap = heightMap/maxElement
            
    return heightMap
