import math
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


                # Havent figured out how to do the "Correct" erosion based on erosion radius
                # This just erodes the four nodes of the cell
                heightMap[mapIndexX,mapIndexY] -= erosionAmount* (1 - offsetX) * (1 - offsetY)
                heightMap[mapIndexX+1,mapIndexY] -= erosionAmount * offsetX * (1 - offsetY)
                heightMap[mapIndexX,mapIndexY+1] -= erosionAmount * (1 - offsetX) * offsetY
                heightMap[mapIndexX+1,mapIndexY+1] -= erosionAmount * offsetX * offsetY

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







            




