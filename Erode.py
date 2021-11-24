import random
import numpy as np

erosionRadius = 3
inertia = 0.1
sedimentCapacityFactor = 4
minSedimentCapacity = 0.1
erodeSpeed = 0.3
depositSpeed = 0.4
evaporateSpeed = 0.1
gravity = 4
dropletLifetime = 30
initialWaterVolume = 1
initialSpeed = 1

def Erode(numDroplets,heightMap):
    #Assuming heightMap is a numpyArray
    mapSize = heightMap.shape[0]

    for i in range(numIterations):
        posX = mapSize*random.random()
        posY = mapSize*random.random()
        speed = initialSpeed
        water = initialWaterVolume

        dirX = 0
        dirY = 0

        for j in range(dropletLifetime):
            mapIndexX = int(posX)
            mapIndexY = int(posY)

            #Calculate droplet's offset inside the cell (0,0) = at NW node, (1,1) = at SE node
            offsetX = posX-mapIndexX
            offsetY = posY-mapIndexY

            





