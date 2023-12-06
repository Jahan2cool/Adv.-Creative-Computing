import numpy as np
import pygame
import math

pygame.init()
clock = pygame.time.Clock()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Lunar Lander")
run = True
FPS = 30
font = pygame.font.Font(None, 50)
smallfont = pygame.font.Font(None, 35)

black = (0, 0, 0)
Mooncolor = (148, 148, 148)
red = (255, 0, 0)
yellow = (255, 120, 0)
orange = (255, 80, 0)
bottomColor = (255, 255, 255)
topcolor = (74, 74, 74)
split, crash, wreset = False, False, False

emptyVectors = np.array([(0.0, 0.0),(0.0, 0.0),(0.0, 0.0),(0.0, 0.0),(0.0, 0.0),(0.0, 0.0),(0.0, 0.0),(0.0, 0.0)])
movementScale = 0.6
thrustvalue = 3 / 4
G = 1.62 / 4
num = int(1)

phase = "p1"

class rocketclass:
    def __init__(this,vertices: list,vectors: list,color: tuple,mass: int,maxthrust: float,fuel: int,radius=20,angle=-math.pi / 2,angleVect=0,):
        this.vertices = vertices
        this.vectors = vectors
        this.mass = mass
        this.color = color
        this.maxthrust = maxthrust
        this.fuel = fuel
        this.radius = radius
        this.angle = angle
        this.angleVect = angleVect
        this.mass = mass

    def fuelcheck(this, keys: dict) -> dict:
        booleans = {"thrust": False, "left": False, "right": False}
        if this.fuel < 0: this.fuel = 0
        for fuelthing in [(keys[pygame.K_w], "thrust", 1),(keys[pygame.K_a], "left", 1 / 2),(keys[pygame.K_d], "right", 1 / 2)]:
            if fuelthing[0] and this.fuel > 0:
                booleans[fuelthing[1]] = True
                this.fuel -= 75 * float(fuelthing[2])
                this.mass -= 10 * float(fuelthing[2])
        return {"thrust": booleans["thrust"],"left": booleans["left"],"right": booleans["right"]}

    def getPoints(this, triangle: list) -> list:
        return np.array([(rad * math.cos(t + this.angle), rad * math.sin(t + this.angle)) for [t, rad] in triangle])

    def update(this, pressed: dict):
        for key in [(pressed["left"], -0.01), (pressed["right"], 0.01)]:
            if key[0]: this.angleVect += key[1] * movementScale
        if pressed["thrust"]:
            this.vectors[0] += movementScale * math.cos(this.angle)
            this.vectors[1] += movementScale * math.sin(this.angle)
        this.angle += this.angleVect
        this.vertices += this.vectors

    def draw(this, pressed: dict):
        if pressed["thrust"]: pygame.draw.polygon(screen,red,this.getPoints([[(5 * math.pi / 6), 0.8 * this.radius],[(7 * math.pi / 6), 0.8 * this.radius],[math.pi, 1.5 * this.radius],])+ this.vertices,)
        pygame.draw.polygon(screen,this.color,this.getPoints([[0, this.radius],[(3 * math.pi / 4), this.radius],[(5 * math.pi / 4), this.radius],]) + this.vertices,)
class planet:
    def __init__(self):
        pass

class landerclass:
    def __init__(this):
        this.top = halfLanderClass(np.array([(485.0, 50.0),(515.0, 50.0),(535.0, 65.0),(535.0, 95.0),(515.0, 110.0),(485.0, 110.0),(465.0, 95.0),(465.0, 65.0),]),emptyVectors.copy(),topcolor,2445,15000,8376)
        this.bottom = halfLanderClass(np.array([(485.0, 110.0),(515.0, 110.0),(550.0, 135.0),(540.0, 135.0),(505.0, 115.0),(495.0, 115.0),(460.0, 135.0),(450.0, 135.0)]),emptyVectors.copy(),bottomColor,2034,45000,8248,)

    def update(this, split: bool, thrustvalue: float, crash: bool, pressed: dict) -> tuple:
        totalmass = this.top.mass + this.bottom.mass if not split else this.top.mass
        finalthrust = thrustvalue * 4000 / totalmass if not split else thrustvalue * 2500 / totalmass
        objlist = [this.top] if split else [this.bottom, this.top]
        downforce = this.bottom.vectors[5][1] * totalmass
        sideforce = this.bottom.vectors[5][0] * totalmass

        for i in range(8):
            for key in [(pressed["thrust"], 1, 1),(pressed["left"], 0, 1 / 2),(pressed["right"], 0, -1 / 2),(True if this.top.vertices[7][1] < 685 else False, 1, -G / finalthrust),]:
                if key[0]:
                    for obj in objlist: obj.vectors[i][key[1]] -= finalthrust * key[2]

        if not split:
            if this.top.vertices[7][1] < 685:
                for obj in objlist: obj.vertices += obj.vectors
            else:
                if downforce < 15000 and abs(sideforce) < 5000:
                    split = True
                    this.top.vectors = emptyVectors.copy()
                else: crash = True

        elif split: this.top.vertices += this.top.vectors

        return (split, crash, downforce, sideforce)
    
    def draw(this, split: bool, pressed: dict):
        pygame.draw.rect(screen, Mooncolor, pygame.Rect(0, 760, 800, 800))
        if pressed["thrust"]: pygame.draw.polygon(screen,(255, 0, 0),([(this.top.vertices[1][0], this.top.vertices[1][1] + 55),(this.top.vertices[1][0] - 30, this.top.vertices[1][1] + 55),(this.top.vertices[1][0] - 15, this.top.vertices[1][1] + 100)]))
        for x in [(pressed["left"], 2, 3, 1), (pressed["right"], 7, 6, -1)]:
            if x[0]: pygame.draw.polygon(screen,(255, 0, 0),([(this.top.vertices[x[1]][0], this.top.vertices[x[1]][1] + 10),(this.top.vertices[x[2]][0], this.top.vertices[x[2]][1] - 10),(this.top.vertices[x[1]][0] + 10 * x[3], this.top.vertices[x[1]][1] + 15),]))

        for obj in [this.bottom, this.top]: pygame.draw.polygon(screen, obj.color, (obj.vertices))

        show = this.bottom if split == False else this.top
        Text = font.render("Fuel: " + str(show.fuel), False, (255, 255, 255))
        screen.blit(Text, (20, 20))
        
    def drawaftercrash(this, num: int, downforce: float, sideforce: float) -> int:
        screen.fill(black)
        pygame.draw.rect(screen, Mooncolor, pygame.Rect(0, 760, 800, 800))
        pygame.draw.circle(screen, black, (this.top.vertices[1][0] - 15, 500), 290)
        if num < 200:
            num += 10
            for obj, value in [(this.bottom, 3), (this.top, 5)]: pygame.draw.polygon(screen, obj.color, (obj.vertices - num * obj.vectors[5][1] / value))
            for num2, color in [(0, red),(30, orange),(100, yellow)]:
                if num > num2: pygame.draw.circle(screen, color, (this.top.vertices[1][0] - 15, 670), num - num2)

        if downforce > 15000 and abs(sideforce) > 5000: Text = smallfont.render("Both your sideforce and downforce were too high so you crashed!",False,(255, 255, 255))
        else:
            for force, limit, text in [(downforce, 15000, "downforce"),(sideforce, 5000, "sideforce")]:
                if abs(force) > limit: Text = smallfont.render("Your " + text + " was too high so you crashed!",False,(255, 255, 255))
        
        screen.blit(Text, (20, 20))

        return num

class halfLanderClass:
    def __init__(this,vertices: list,vectors: list,color: tuple,mass: int,maxthrust: float,fuel: int,radius=20,angle=-math.pi / 2,angleVect=0,):
        this.vertices = vertices
        this.vectors = vectors
        this.mass = mass
        this.color = color
        this.maxthrust = maxthrust
        this.fuel = fuel
        this.radius = radius
        this.angle = angle
        this.angleVect = angleVect
        this.mass = mass

    def fuelcheck(this, keys: dict) -> dict:
        booleans = {"thrust": False, "left": False, "right": False}
        if this.fuel < 0:
            this.fuel = 0

        for fuelthing in [(keys[pygame.K_w], "thrust", 1),(keys[pygame.K_a], "left", 1 / 2),(keys[pygame.K_d], "right", 1 / 2)]:
            if fuelthing[0] and this.fuel > 0:
                booleans[fuelthing[1]] = True
                this.fuel -= 75 * float(fuelthing[2])
                this.mass -= 10 * float(fuelthing[2])
        return {"thrust": booleans["thrust"],"left": booleans["left"], "right": booleans["right"],}

rocket: rocketclass = rocketclass(np.array([400.0, 400.0]), np.array([0.0, 0.0]), (255, 255, 255), 6479, 1000, 10000)

lander: landerclass = landerclass()
lander.top.vectors += 3
lander.bottom.vectors += 3

while run:
    clock.tick(FPS)
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): run = False

    keys = pygame.key.get_pressed()

    if phase == "p1":
        pressed = rocket.fuelcheck(keys)
        rocket.update(pressed)
        rocket.draw(pressed)

    elif phase == "p2":
        if crash == False:
            pressed = (lander.bottom if split == False else lander.top).fuelcheck(keys)
            split, crash, downforce, sideforce = lander.update(split, thrustvalue, crash, pressed)
            lander.draw(split, pressed)
        else: num = lander.drawaftercrash(num, downforce, sideforce)
    pygame.display.update()