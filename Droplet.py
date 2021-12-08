import math


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
        self.inertia = self.water*0.05
        

    def move(self):
        self.posX = self.posX + self.dirX
        self.posY = self.posY + self.dirY

    def setGradientAndHeight(self,map):
        coordx=math.floor(self.posX)
        coordy=math.floor(self.posY)
        internalx=self.posX-coordx
        internaly=self.posY-coordy
        if self.posX<map.shape[0]-1 and self.posY<map.shape[1]-1: 
            corner1 = map[coordx, coordy]
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


        dirX = (self.dirX * self.inertia - gradx* (1 - self.inertia))
        dirY = (self.dirY * self.inertia - grady* (1 - self.inertia))

        dirLength = math.sqrt(dirX*dirX+dirY*dirY)
        if dirLength != 0:
            dirX = dirX/dirLength
            dirY = dirY/dirLength
        
        self.dirX = dirX
        self.dirY = dirY
        self.height = height
        