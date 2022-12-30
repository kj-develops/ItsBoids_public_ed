import pygame
from pygame import Vector2
import random

class Boid (pygame.sprite.Sprite):
    def __init__(self, screen, pos):
        super().__init__()
        self.image = pygame.image.load("boid.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = self.pos
        self.screen = screen
        self.acceleration = Vector2 (0, 0)
        #sets the speed for movement in different directions
        self.speed = Vector2 (random.uniform(-5, -2) if (random.randrange (1,100) < 50) else random.uniform(2, 5), \
                            random.uniform(-5, -2) if (random.randrange (1,100) < 50) else random.uniform(2, 5))

    def update(self, screenWidth, screenHeight, boidSpeed): 
        #checks if the boids fly out of the screen and spawns them on the oposite side
        if (self.rect.left > screenWidth):
            self.pos.x = 0
        if (self.rect.right < 0):
            self.pos.x = screenWidth - self.image.get_width()
        if (self.rect.top > screenHeight):
            self.pos.y = 0
        if (self.rect.bottom < 0):
            self.pos.y = screenHeight -self.image.get_height()
        #moves the boids
        self.pos += boidSpeed
        self.rect.x = self.pos.x - self.image.get_width() / 2
        self.rect.y = self.pos.y - self.image.get_height() / 2   

    
class Hoik (pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.image = pygame.image.load("hoik.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()
        self.pos = self.rect.center 
        self.speed = Vector2 (random.uniform(-5, -2) if (random.randrange (1,100) < 50) else random.uniform(2, 5), \
                            random.uniform(-5, -2) if (random.randrange (1,100) < 50) else random.uniform(2, 5))
        self.screen = screen
        self.screech = pygame.mixer.Sound("screech.wav")
        
    def spawn(self):
        #draws the hoik and makes sound
        self.screech.play() 
        self.rect.center = pygame.mouse.get_pos()
        self.pos = self.rect.center 
        self.speed = Vector2 (random.uniform(-5, -2) if (random.randrange (1,100) < 50) else random.uniform(2, 5), \
                            random.uniform(-5, -2) if (random.randrange (1,100) < 50) else random.uniform(2, 5))

    def update(self):
        #moves the Hoik
        self.pos += self.speed
        self.rect.x = self.pos.x - self.image.get_width() / 2
        self.rect.y = self.pos.y - self.image.get_height() / 2

    def isOffScreen(self, screenWidth, screenHeight):
        #checks if hoik is not on screen. Updates "hoikStatus"
        if (self.rect.left > screenWidth):
            return False        
        if (self.rect.right < 0):
            return False
        if (self.rect.top > screenHeight):
            return False
        if (self.rect.bottom < 0):
            return False
        
        return True

#birdcage
class Cage (pygame.sprite.Sprite):
    def __init__(self, screen, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = self.pos
        self.radius = self.rect.width/2
        self.screen = screen