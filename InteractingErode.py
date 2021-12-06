import math
import random
import numpy as np
import itertools
import GenerateHeightMap as genMap

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

def Erode(numDroplets,heightMap):
    #Assuming heightMap is a numpyArray
    mapSize = heightMap.shape[0]
    nodesIndex = getNodeOffsets(erosionRadius)

    for i in range(numDroplets):
        posX = mapSize*random.random()
        posY = mapSize*random.random()
        speed = initialSpeed
        water = initialWaterVolume
        sediment = 0

        dirX = 0
        dirY = 0

        for j in range(dropletLifetime):
            mapIndexX = int(posX)
            mapIndexY = int(posY)

            #Calculate droplet's offset inside the cell (0,0) = at NW node, (1,1) = at SE node
            offsetX = posX-mapIndexX
            offsetY = posY-mapIndexY
            
            #Get gradient and height then normalize and move droplet
            gradientAndHeight = returngradient(heightMap,posX,posY)

            dirX = (dirX * inertia - gradientAndHeight[0] * (1 - inertia))
            dirY = (dirY * inertia - gradientAndHeight[1]* (1 - inertia))

            dirLength = math.sqrt(dirX*dirX+dirY*dirY)
            if dirLength != 0:
                dirX = dirX/dirLength
                dirY = dirY/dirLength

            posX = posX + dirX
            posY = posY + dirY

            if dirLength == 0 or posX < 0 or posX >= mapSize - 1 or posY < 0 or posY >= mapSize - 1 or gradientAndHeight[2]==-1:
                    break
            
            #Calculate change in height
            deltaHeight = returngradient(heightMap,posX,posY)[2]-gradientAndHeight[2]

            # Calculates the droplet capacity, just took this from lague, idk the derivation
            sedimentCapacity = max(-deltaHeight * speed * water * sedimentCapacityFactor, minSedimentCapacity)
            
            if sediment > sedimentCapacity or deltaHeight > 0:

                #If uphill, try to fill hole
                if deltaHeight > 0:
                    depositAmount = min(deltaHeight,sediment)
                else:
                    depositAmount = (sediment - sedimentCapacity) * depositSpeed
            
                #Bilinear interpolation between the four nodes
                heightMap[mapIndexX,mapIndexY] += depositAmount * (1 - offsetX) * (1 - offsetY)
                heightMap[mapIndexX+1,mapIndexY] += depositAmount * offsetX * (1 - offsetY)
                heightMap[mapIndexX,mapIndexY+1] += depositAmount * (1 - offsetX) * offsetY
                heightMap[mapIndexX+1,mapIndexY+1] += depositAmount * offsetX * offsetY

                sediment -= depositAmount
            else:

                #Dont remove more than deltaHeight
                erosionAmount = min((sedimentCapacity - sediment) * erodeSpeed, -deltaHeight)

                weights,nodes = getErodeNodesAndWeights(erosionRadius,posX,posY,nodesIndex,mapSize)

                for i in range(len(weights)):
                    heightMap[nodes[i][0],nodes[i][1]] -= erosionAmount*weights[i]
                    heightMap[nodes[i][0],nodes[i][1]] = max(heightMap[nodes[i][0],nodes[i][1]],-1)

                sediment += erosionAmount

    return(heightMap)


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
    else:
        gradx=0
        grady=0
        height=-1
    return (gradx,grady,height)

    

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
    
        

    

heightMap = genMap.generateMapTest(4,100)

erodedMap = heightMap.copy()


erodedMap = Erode(100,erodedMap)




#Show the paths of the waterdroplets in both cases and compare aswell

            




