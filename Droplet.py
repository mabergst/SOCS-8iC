import math

ForceFactor = 0.03

class Droplet:
    def __init__(self,posX,posY,dirX,dirY,water,speed,sediment,capacity,height):
        self.posX = posX
        self.posY = posY
        self.height = height

        self.dirX = dirX
        self.dirY = dirY
        
        self.water = water
        self.speed = speed
        self.sediment = sediment
        self.capacity = capacity
        self.inertia = min(1,0.05*water)
        

    def move(self):
        self.posX = self.posX + self.dirX
        self.posY = self.posY + self.dirY

    def setGradientAndHeight(self,map,nearDrops):
        coordx=math.floor(self.posX)
        coordy=math.floor(self.posY)
        internalx=self.posX-coordx
        internaly=self.posY-coordy
        if self.posX<map.shape[0]-1 and self.posY<map.shape[1]-1: 
            corner1 = map[coordx, coordy]
            corner2 = map[coordx + 1, coordy]
            corner3 = map[coordx, coordy + 1]
            corner4 = map[coordx + 1, coordy + 1]
            gradx = (corner2-corner1)*(1-internaly)+(corner4-corner3)*internaly 
            grady = (corner3 - corner1) * (1 - internalx) + (corner4 - corner2) * internalx
            height = corner1 * (1 - internalx) * (1 - internaly) + corner2 * internalx * (1 - internaly) + corner3 * (1 - internalx) * internaly + corner4 * internalx * internaly
        else:
            gradx=0
            grady=0
            height=-1

        attractionVectors = []

        for drop in nearDrops:
            dropDir = [drop.posX-self.posX,drop.posY-self.posY]
            length = math.sqrt(dropDir[0]*dropDir[0]+dropDir[1]*dropDir[1])
            attractionVectors.append([dropDir[0]/(0.2+length),dropDir[1]/(0.2+length)])


        attractionVector = [0,0]
        for vect in attractionVectors:
            attractionVector[0] = attractionVector[0]+vect[0]
            attractionVector[1] = attractionVector[1]+vect[1]
        
        if len(attractionVectors) > 0:
            veclength = math.sqrt(attractionVector[0]*attractionVector[0]+attractionVector[1]*attractionVector[1])
            attractionVector[0] = attractionVector[0]/veclength
            attractionVector[1] = attractionVector[1]/veclength


        dirX = (self.dirX * self.inertia - (gradx+ForceFactor*attractionVector[0])*(1 - self.inertia))
        dirY = (self.dirY * self.inertia - (grady+ForceFactor*attractionVector[1])*(1 - self.inertia))

        dirLength = math.sqrt(dirX*dirX+dirY*dirY)
        if dirLength != 0:
            dirX = dirX/dirLength
            dirY = dirY/dirLength
        
        self.dirX = dirX
        self.dirY = dirY
        self.height = height
        