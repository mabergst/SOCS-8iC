import math
import random
import numpy as np
import itertools
import GenerateHeightMap as genMap
import Droplet

erosionRadius = 4
inertia = 0.03
sedimentCapacityFactor = 4
minSedimentCapacity = 0.01
erodeSpeed = 0.2
depositSpeed = 0.5
evaporateSpeed = 0.1
gravity = 4
dropletLifetime = 30
initialWaterVolume = 1
initialSpeed = 1

def Erode(numDroplets,heightMap,iterations):
    #Assuming heightMap is a numpyArray
    mapSize = heightMap.shape[0]
    nodesIndex = getNodeOffsets(erosionRadius)

    droplets = []
    for i in range (numDroplets):
        droplets.append(Droplet.Droplet(mapSize*random.random(),mapSize*random.random(),0,0,initialWaterVolume,initialSpeed,0,0,0))


    for iIter in range(iterations):
        for drop in droplets:
        
            
            mapIndexX = int(drop.posX)
            mapIndexY = int(drop.posY)

            #Calculate droplet's offset inside the cell (0,0) = at NW node, (1,1) = at SE node
            offsetX = drop.posX-mapIndexX
            offsetY = drop.posY-mapIndexY
            

            #Set gradient and height
            drop.setGradientAndHeight(heightMap)
            prevHeight = drop.height

            #Move drop
            drop.move()

            if drop.posX < 0 or drop.posX >= mapSize - 1 or drop.posY < 0 or drop.posY >= mapSize - 1 or drop.height==-1:
                del drop
                continue

            #Set gradient and height
            drop.setGradientAndHeight(heightMap)
            
            #Calculate change in height
            deltaHeight = drop.height-prevHeight

            # Calculates the droplet capacity
            drop.capacity = max(-deltaHeight * drop.speed * drop.water * sedimentCapacityFactor, minSedimentCapacity)
            
            if drop.sediment > drop.capacity or deltaHeight > 0:

                #If uphill, try to fill hole
                if deltaHeight > 0:
                    depositAmount = min(deltaHeight,drop.sediment)
                else:
                    depositAmount = (drop.sediment - drop.capacity) * depositSpeed
            
                #Bilinear interpolation between the four nodes
                heightMap[mapIndexX,mapIndexY] += depositAmount * (1 - offsetX) * (1 - offsetY)
                heightMap[mapIndexX+1,mapIndexY] += depositAmount * offsetX * (1 - offsetY)
                heightMap[mapIndexX,mapIndexY+1] += depositAmount * (1 - offsetX) * offsetY
                heightMap[mapIndexX+1,mapIndexY+1] += depositAmount * offsetX * offsetY

                drop.sediment -= depositAmount
            else:

                #Dont remove more than deltaHeight
                erosionAmount = min((drop.capacity - drop.sediment) * erodeSpeed, -deltaHeight)

                weights,nodes = getErodeNodesAndWeights(erosionRadius,drop.posX,drop.posY,nodesIndex,mapSize)

                for i in range(len(weights)):
                    heightMap[nodes[i][0],nodes[i][1]] -= erosionAmount*weights[i]
                    heightMap[nodes[i][0],nodes[i][1]] = max(heightMap[nodes[i][0],nodes[i][1]],-1)

                drop.sediment += erosionAmount

            drop.speed = math.sqrt( max(drop.speed * drop.speed + deltaHeight * gravity,0))
            drop.water *= (1 - evaporateSpeed)

    return(heightMap)



def getHeight(map,posX,posY):
    coordx=math.floor(posX)
    coordy=math.floor(posY)
    internalx=posX-coordx
    internaly=posY-coordy
    if posX<map.shape[0]-1 and posY<map.shape[1]-1: 
        corner1 = map[coordx, coordy]
        corner2 = map[coordx + 1, coordy]
        corner3 = map[coordx, coordy + 1]
        corner4 = map[coordx + 1, coordy + 1]
        height = corner1 * (1 - internalx) * (1 - internaly) + corner2 * internalx * (1 - internaly) + corner3 * (1 - internalx) * internaly + corner4 * internalx * internaly
    else:
        height = -1
    
    return height


def getErodeNodesAndWeights(erosionRadius,posX,posY,nodesIndex,mapSize):
    mapIndexX = int(posX)
    mapIndexY = int(posY)

    weights = []
    nodes = []

    for i in range(len(nodesIndex)):

        if mapIndexX+nodesIndex[i][0]<mapSize and mapIndexY+nodesIndex[i][1]<mapSize:

            d = getDistance([posX,posY],[mapIndexX+nodesIndex[i][0],mapIndexY+nodesIndex[i][1]])
            if d<=erosionRadius:
                weights.append(1-math.sqrt(d))
                nodes.append([mapIndexX+nodesIndex[i][0],mapIndexY+nodesIndex[i][1]])
    weights = softmax(weights)

    return weights,nodes


def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)



def getDistance(position,target):
    d = math.sqrt((position[0]-target[0])*(position[0]-target[0])+(position[1]-target[1])*(position[1]-target[1]))
    return d


def unique(list1):
    # insert the list to the set
    list_set = set(list1)
    # convert the set to the list
    unique_list = (list(list_set))
    return unique_list


#Get all nodes withon brushradius+1 square
def getNodeOffsets(radius):
    offset =[0]
    offset.append(0)
    for i in range(radius+2):
        if i ==0:
            continue
        offset.append(i)
        offset.append(i)
        offset.append(-i)
        offset.append(-i)

    nodeOffsets = list(itertools.permutations(offset, 2))
    uniqueNodeOffsets = unique(nodeOffsets)
    return uniqueNodeOffsets
    




#Show the paths of the waterdroplets in both cases and compare aswell

        



