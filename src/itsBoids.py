#!/usr/local/bin/python3

import pygame
from pygame import Vector2
import random
from classes import Boid, Hoik, Cage

#Cohesion
def togetherRule(theBoid, boidsGroup):
    

    boidPosSum = Vector2(0,0)
    boidCount = 0

    for boid in boidsGroup:
        tempDistance = (theBoid.pos - boid.pos).length()
        if tempDistance < 100   :
            boidPosSum += boid.pos
            boidCount += 1

    #avoid division by 0 if there are no boids around
    if boidCount != 0:
        boidPosSum /= boidCount
        return (boidPosSum - theBoid.pos) / 30

    return theBoid.pos
    

#Separation
def privacyRule(theBoid, boidsGroup, hoikStatus, hoik):
    distanceVec = Vector2 (0,0)

    for boid in boidsGroup:
        if (hoikStatus == True):
            if (boid.pos - hoik.pos).length() < 50:
                distanceVec -= (boid.pos - theBoid.pos)
                return distanceVec
        if boid != theBoid:
                if ((theBoid.pos-boid.pos).length() < 25):
                    distanceVec -= (boid.pos - theBoid.pos)
    
    return distanceVec/4
             
#Alignment
def thisWayRule(theBoid, boidsGroup):
    boidAccelSum = Vector2(0,0)
    boidCount = 0

    for boid in boidsGroup:
        tempDistance = (theBoid.pos - boid.pos).length()
        if tempDistance < 100:
            boidAccelSum += boid.acceleration
            boidCount += 1

    #avoid devicion by 0 if there are no boids around
    if boidCount != 0:
        boidAccelSum /= boidCount
        return (boidAccelSum - theBoid.acceleration) / 2   

    return theBoid.acceleration

#limit the speed 
def speedlimit (speed):
    if (speed.length() > 5):
        speed.scale_to_length(5)

    return speed

def collisionRule(theBird, cageGroup):

    distanceVec = Vector2 (0,0)

    for cage in cageGroup:
        if (theBird.pos - cage.rect.center).length() < cage.radius:
            distanceVec -= (cage.rect.center - theBird.pos)
    
    return distanceVec/4

print ("Lets play itsBoids!")
pygame.display.set_caption("itsBoids!")
pygame.init()

#sets screen and background image
screenWidth = 1200
screenHeight = 750
BGFileName = "sky.png"
mainScreen = pygame.display.set_mode((screenWidth, screenHeight))

backGround = pygame.transform.scale(pygame.image.load(BGFileName), (screenWidth, screenHeight))

#BOIDS
boidsGroup = pygame.sprite.Group()
for i in range(100):
    #Sets a random vector to be each boids position 
    boidPos = Vector2(random.randrange(0, screenWidth),random.randrange(0, screenHeight))
    #make a boid object
    boid = Boid(mainScreen, Vector2 (boidPos))
    #Add the boid object to the group
    boidsGroup.add(boid)

#HOIKS
hoik = Hoik(mainScreen)
hoiksGroup = pygame.sprite.Group()
hoiksGroup.add(hoik)

#CAGE
cageGroup = pygame.sprite.Group()
cageImage = pygame.image.load("cage.png").convert_alpha()
pos = Vector2 ((screenWidth/2)-300, (cageImage.get_height()/2) + 100)
for i in range(3):
    cage = Cage(mainScreen, cageImage, pos)
    cageGroup.add(cage)
    pos.x += 300
    pos.y += 200

#variable to spawn/remove hoik
hoikStatus = False

#main program loop
while True:
    pygame.time.delay(60)
    
    mainScreen.blit(backGround, (0,0))
    
    cageGroup.draw(mainScreen)
    
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Thank you for playing!")
            exit()
            #spawn hoik and play sound at mouseclick
        if (event.type == pygame.MOUSEBUTTONDOWN):
            hoikStatus = True
            hoik.spawn()
    if (hoikStatus == True):
        hoiksGroup.update()
        #remove Hoik when exiting screen
        hoikStatus = hoik.isOffScreen(screenWidth, screenHeight)
        hoiksGroup.draw(mainScreen)

    boidsGroup.draw(mainScreen)

    for boid in boidsGroup:
        #call each rule for boid movement
        v1 = togetherRule(boid, boidsGroup)
        v2 = privacyRule(boid, boidsGroup, hoikStatus, hoik)
        v3 = thisWayRule(boid, boidsGroup)
        
        boid.acceleration = (v1 + v2 + v3)
        
        boid.acceleration += collisionRule(boid, cageGroup)
        
        boid.speed += boid.acceleration
        
        boid.speed = speedlimit(boid.speed)

        boid.update(screenWidth, screenHeight, boid.speed)        
   
    

    pygame.display.update()