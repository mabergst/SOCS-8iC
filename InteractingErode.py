import math
import random
import numpy as np
import itertools
import GenerateHeightMap as genMap
import Droplet

erosionRadius = 4
mergeRadius = 0.01
inertia = 0.03
sedimentCapacityFactor = 4
minSedimentCapacity = 0.03
erodeSpeed = 0.2
depositSpeed = 0.1
evaporateSpeed = 0.1
gravity = 4
dropletLifetime = 30
initialWaterVolume = 1
initialSpeed = 1

def Erode(numDroplets,heightMap):
    #Assuming heightMap is a numpyArray
    mapSize = heightMap.shape[0]
    nodesIndex = getNodeOffsets(erosionRadius)

    droplets = []
    for i in range (numDroplets):
        droplets.append(Droplet.Droplet(mapSize*random.random(),mapSize*random.random(),0,0,initialWaterVolume,initialSpeed,0,0,0,erosionRadius))


    for j in range(dropletLifetime):
        print(len(droplets))
        for drop in droplets:
        
            mapIndexX = int(drop.posX)
            mapIndexY = int(drop.posY)

            #Calculate droplet's offset inside the cell (0,0) = at NW node, (1,1) = at SE node
            offsetX = drop.posX-mapIndexX
            offsetY = drop.posY-mapIndexY

            nearDrops = getNearDrops(droplets,drop)

            for nearDrop in nearDrops:
                if getDistance([drop.posX, drop.posY],[nearDrop.posX, nearDrop.posY]) < mergeRadius:
                    droplets.remove(nearDrop)
                    droplets.remove(drop)
                    droplets.append(mergeDrops(drop,nearDrop))
                    break



            #Contnue if drop has merged
            if droplets.count(drop)==0:
                continue
            
            #Set gradient and height
            drop.setGradientAndHeight(heightMap,nearDrops)
            prevHeight = drop.height

            

            #Move drop
            drop.move()

            if  math.sqrt(drop.dirX*drop.dirX+drop.dirY*drop.dirY)==0 or drop.posX < 0 or drop.posX >= mapSize - 1 or drop.posY < 0 or drop.posY >= mapSize - 1 or drop.height==-1:
                droplets.remove(drop)
                continue

            #Set gradient and height
            currentHeight = getHeight(drop.posX,drop.posY,heightMap)
            
            #Calculate change in height
            deltaHeight = currentHeight-prevHeight

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

def getDropDistance(position,target):
    d = math.sqrt((position.posX-target.posX)*(position.posX-target.posX)+(position.posY-target.posY)*(position.posY-target.posY)+(position.height-target.height)*(position.height-target.height))
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
    

def getNearDrops(droplets, currentDrop):
    nearDrops = []
    for drop in droplets:
        if getDropDistance(drop,currentDrop) < erosionRadius and drop is not currentDrop:
            nearDrops.append(drop)
    return(nearDrops)

def mergeDrops(drop1,drop2):
    posX = (drop1.posX+drop2.posX)/2
    posY = (drop1.posY+drop2.posY)/2

    dirX = (drop1.dirX+drop2.dirX)
    dirY = (drop1.dirY+drop2.dirY)

    dirLength = math.sqrt(dirX*dirX+dirY*dirY)
    if dirLength != 0:
        dirX = dirX/dirLength
        dirY = dirY/dirLength

    speed = (drop1.speed+drop2.speed)/2
    water = drop1.water + drop2.water
    sediment = drop1.sediment + drop2.sediment
    
    return Droplet.Droplet(posX,posY,dirX,dirY,water,speed,sediment,0,0,erosionRadius)



    

def getHeight(posX,posY,map):
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

    return(height)
    

            




