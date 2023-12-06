import pygame
import numpy as np
import math
pygame.init()
width = 800
height = 800

black = (0,0,0)

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
FPS = 60
run = True

class Mars:
  def __init__(self):
    #self.mass = 8.5771812e+14
    self.mass = 50
    self.name = 'mars'
    self.vectors = np.array([0.0000000001, 0.0])
    self.vertices = np.array([-318, 0])
    self.color = (255,120,0)
    self.radius = 30


class Sun:
  def __init__(self):
    #self.mass = 2.6711409e+21
    self.mass = 200
    self.distance = 0
    self.name = 'sun'
    self.vectors = np.array([0.0 , 0.0])
    self.vertices = np.array([0,0])
    self.color = (255,255,204)
    self.radius = 80

mars = Mars()
sun = Sun()

planets = [sun,mars]

def updatevectors(planets):
    for i in planets:
        for j in planets:
            if i != j:
                r = math.sqrt((i.vertices[0] - j.vertices[0]) ** 2 + (i.vertices[1] - j.vertices[1]) ** 2)
                force = (6.67e-11 * i.mass * j.mass) / r ** 2
                angle = math.atan2((i.vertices[1] - j.vertices[1]),(i.vertices[0] - j.vertices[0]))
                j.vectors[0] += ((math.cos(angle)*force)/j.mass) * 58800
                j.vectors[1] += ((math.sin(angle)*force)/j.mass) * 58800

        i.vertices[0] = i.vertices[0] + i.vectors[0] * 58800
        i.vertices[1] = i.vertices[1] + i.vectors[1] * 58800
    return planets

def drawplanets(screen, planets):
    for i in planets:
        pygame.draw.circle(screen, i.color , ((i.vertices[0]) + width/2 , (i.vertices[1]) + height/2), i.radius)

while run:
    clock.tick(FPS)
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    planets = updatevectors(planets)
    drawplanets(screen, planets)
    pygame.display.flip()