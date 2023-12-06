import numpy as np
import pygame
from time import time

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Lunar Lander')

run = True
FPS = 30
font = pygame.font.Font(None,50)
smallfont = pygame.font.Font(None,35)

black = (0,0,0)
Mooncolor = (148,148,148)
red = (255,0,0) 
yellow = (255,120,0) 
orange = (255,80,0) 
bottomColor = (255,255,255) 
topcolor = (74,74,74)

thrustvalue = 3/4
G = 1.62/4
num = int(1)

class spaceship():
  def __init__(self,vertices,vectors,color, mass,maxthrust,fuel):
      self.vertices = vertices
      self.vectors = vectors
      self.mass = mass
      self.color = color
      self.maxthrust = maxthrust
      self.fuel = fuel
  def fuelcheck(self, keys):
      multipliers = {"thrust": 1, "left": 1/2, "right": 1/2}
      validKeys = []
      for key in keys:
        if key[1] and self.fuel>0:
            validKeys.append(key[0])
            self.fuel-=75 * float(multipliers[key[0]])
            self.mass-=10 * float(multipliers[key[0]])
      if self.fuel < 0:
        self.fuel = 0
      return validKeys
  def draw(self):
    pygame.draw.polygon(screen, self.color, (self.vertices))
  def draw_flames(self, valid):
    if "thrust" in valid:
      pygame.draw.polygon(screen, (255,0,0), ([(self.vertices[1][0], self.vertices[1][1]+55), (self.vertices[1][0]-30, self.vertices[1][1]+55), (self.vertices[1][0]-15, self.vertices[1][1]+100)]))

    #left right thrust
    for x in [("left" in valid, 2, 3, 1), ("right" in valid, 7, 6, -1)]:
        if x[0]: pygame.draw.polygon(screen, (255,0,0), ([(self.vertices[x[1]][0],self.vertices[x[1]][1]+10),(self.vertices[x[2]][0],self.vertices[x[2]][1]-10),(self.vertices[x[1]][0]+10*x[3],self.vertices[x[1]][1]+15)]))

emptyVectors = np.array([(0,0) for i in range(8)], dtype=float)
rocket = spaceship(np.array([(90,100),(110,100),(100,80)], dtype=float), np.array([(0,0),(0,0),(0,0)], dtype=float), (255,255,255), 6479, 1000, 10000)
top = spaceship(np.array([(485,50),(515,50),(535,65),(535,95),(515,110),(485,110),(465,95),(465,65)], dtype=float), emptyVectors.copy(), topcolor, 2445,15000,8376)
bottom = spaceship(np.array([(485,110),(515,110),(550,135),(540,135),(505,115),(495,115),(460,135),(450,135)], dtype=float), emptyVectors.copy(), bottomColor,2034,45000,8248)
top.vectors+=3; bottom.vectors+=3

def drawaftercrash(num,downforce,sideforce):
    screen.fill(black)
    #draw land with a hole
    pygame.draw.rect(screen,Mooncolor, pygame.Rect(0,760,800,800))
    pygame.draw.circle(screen, black, (top.vertices[1][0]-15,500), 290)

    if num < 200:
        num+=10

        #bodies
        for (obj, value) in [(bottom,3), (top,5)]: 
           pygame.draw.polygon(screen, obj.color, (top.vertices-num*bottom.vectors[5][1]/value))

        #explosion
        for (num2, color) in [(0,red),(30, orange),(100,yellow)]:
            if num>num2: pygame.draw.circle(screen, color, (top.vertices[1][0]-15,670), num-num2)

    for (what, text) in [(downforce>15000 and abs(sideforce)> 5000, "sideforce and downforce"), (downforce > 15000, "downforce"), (abs(sideforce) > 5000, "sideforce")]:
        if what:
          Text=smallfont.render("Your " + text + " was too high so you crashed!",False,(255,255,255))
          break
    screen.blit(Text, (20,20))
    return num

def update_vectors(objects, keys, thrustvalue, valid, phaseAction, downforce, sideforce, lastChanged):
    totalmass = sum([a.mass for a in objects])
    finalthrust = thrustvalue*2000*len(objects)/totalmass

    if phaseAction in ["landing", "takeoff"]:
      if top.vertices[2][1]<670:
        for obj in objects: obj.vectors[:, 1] += G
      for key in [("thrust", 1,1), ("left", 0, 1/2), ("right", 0, -1/2)]:
         if key[0] in valid:
            for obj in objects: obj.vectors[:, key[1]] -= finalthrust * key[2]
      for obj in objects: obj.vertices+=obj.vectors

    if phaseAction == "landing" and top.vertices[2][1]>=670:
      downforce = objects[1].vectors[5][1]*totalmass
      sideforce = objects[1].vectors[5][0]*totalmass
      if downforce<20000 and abs(sideforce)<5000:
        phaseAction = "landed"
        lastChanged = time()
        objects[0].vectors = emptyVectors.copy()
      else:
        phaseAction = "crashed"
    return phaseAction, downforce, sideforce, lastChanged

downforce = 0
sideforce = 0
phaseAction = "landing"
lastChanged = time()

while run:
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): run = False
      if event.type == pygame.KEYDOWN and (time() - lastChanged > 1 and phaseAction == "landed"): phaseAction = "takeoff"

    pykeys = pygame.key.get_pressed()
    keys = [("thrust", pykeys[pygame.K_w]), ("left", pykeys[pygame.K_a]), ("right", pykeys[pygame.K_d])]
    valid = []
    
    if phaseAction != "crashed":
      screen.fill(black)

      affectedObjects = [bottom,top] if phaseAction == "landing" else [top]

      if phaseAction in ["landing", "takeoff"]:
        valid = (bottom if phaseAction != "takeoff" else top).fuelcheck(keys)
        phaseAction, downforce, sideforce, lastChanged = update_vectors(affectedObjects, keys, thrustvalue, valid, phaseAction, downforce, sideforce, lastChanged)

      pygame.draw.rect(screen, Mooncolor, pygame.Rect(0,760,800,800))
      top.draw_flames(valid)

      for obj in [bottom,top]: obj.draw()
      screen.blit(font.render("Fuel: " + str((bottom if phaseAction != "takeoff" else top).fuel),False,(255,255,255)), (20,20))

      # Draw Variables
      screen.blit(font.render("Phase: " + phaseAction,False,(255,255,255)), (20,50))
      screen.blit(font.render("Downforce: " + str(downforce),False,(255,255,255)), (20,80))
      screen.blit(font.render("Sideforce: " + str(sideforce),False,(255,255,255)), (20,110))
      screen.blit(font.render("Total Mass: " + str(sum([a.mass for a in affectedObjects])),False,(255,255,255)), (20,170))
      screen.blit(font.render("Total Thrust: " + str(sum([a.maxthrust for a in affectedObjects])),False,(255,255,255)), (20,200))
      screen.blit(font.render("Total Fuel: " + str(sum([a.fuel for a in affectedObjects])),False,(255,255,255)), (20,230))
    else:
        num = drawaftercrash(num,downforce,sideforce)
    pygame.display.update()