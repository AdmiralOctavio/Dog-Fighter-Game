import pygame as pg
import numpy
import time

pg.init()
width, height = 1920, 1080
resolution = (width,height)
screen = pg.display.set_mode(resolution)
scrrect = screen.get_rect()
black =(0, 0, 0)
refreshRate = 144 #Hz

ship = pg.image.load('Player.png')
ship = pg.transform.scale(ship, (128, 96))
enemy = pg.image.load('Enemy.png')
enemy = pg.transform.scale(enemy, (128, 96))
missileText = pg.image.load('missile.png')
missileText = pg.transform.scale(missileText, (128, 96))

shiprect = ship.get_rect()
shiprect.centerx = 250
enemyrect = enemy.get_rect()
enemyrect.centerx = 500
missilerect = missileText.get_rect()
shipDir = []
enemyDir = []
missileDir = []
F_missilesArray = []
E_missilesArray = []
explosions = []
Emwait = 0
Fmwait = 0
speed, missileSpeed = 3, 10
running = True
F_heading, E_heading = 0, 180
isExploding = False
timeafterexplosion = 1
missiletemp = 0

class Missile:
    def __init__(self, posx, posy, heading, timer, origin):
        self.posx = posx
        self.posy = posy
        self.heading = heading
        self.timer = timer
        self.origin = origin
    
    def update(self):
        self.posx += missileSpeed*numpy.cos(numpy.radians(self.heading))
        self.posy -= missileSpeed*numpy.sin(numpy.radians(self.heading))
        self.timer += 1

    def render(self, screen):
        missileText = missileDir[self.heading]
        missilerect = missileText.get_rect()
        missilerect.centerx = self.posx
        missilerect.centery = self.posy
        screen.blit(missileText, missilerect)

def turnLeft(heading):
    heading -= round(90/refreshRate)
    if heading < 0: heading += 360
    return heading

def turnRight(heading):
    heading += round(90/refreshRate)
    if heading > 359: heading -= 360
    return heading

def setup():
    for i in range(360):
        shipDir.append(pg.transform.rotate(ship, i))
        enemyDir.append(pg.transform.rotate(enemy, i))
        missileDir.append(pg.transform.rotate(missileText, i))
    for i in range(5):
        explosion = pg.image.load('ex' + str(i+1) + '.png')
        explosions.append(pg.transform.scale2x(explosion))

setup()
missilerect = missileText.get_rect()
#Friendly Position
F_positionx, F_positiony = width-500, 540
#Enemy Position
E_positionx, E_positiony = 500, 540
enemy = enemyDir[180]
#Main Game Loop
while running:
    pg.event.pump()
    keys = pg.key.get_pressed()
    event = pg.event.get()
#Blue Player Rotation
    if keys[pg.K_a]:
         F_heading = turnRight(F_heading)
         shiprect = ship.get_rect()
         ship = shipDir[F_heading]

    elif keys[pg.K_d]:
         F_heading = turnLeft(F_heading)
         shiprect = ship.get_rect()
         ship = shipDir[F_heading]
#Red Player Rotation
    if keys[pg.K_RIGHT]:
         E_heading = turnRight(E_heading)
         enemyrect = enemy.get_rect()
         enemy = enemyDir[E_heading]

    elif keys[pg.K_LEFT]:
         E_heading = turnLeft(E_heading)
         enemyrect = enemy.get_rect()
         enemy = enemyDir[E_heading]
#Movement
    F_positionx += speed*numpy.cos(numpy.radians(F_heading))
    F_positiony -= speed*numpy.sin(numpy.radians(F_heading))

    E_positionx += speed*numpy.cos(numpy.radians(E_heading))
    E_positiony -= speed*numpy.sin(numpy.radians(E_heading))

    shiprect.centerx = F_positionx
    shiprect.centery = F_positiony

    enemyrect.centerx = E_positionx
    enemyrect.centery = E_positiony

#Resets position when out of bounds
    F_positionx %= width
    F_positiony %= height
    E_positionx %= width
    E_positiony %= height

#Missiles
    if pg.key.get_pressed()[pg.K_s] and Fmwait > 100: #Friendly Missile Launch
        Fmwait = 0
        Ftimer = 0
        m = Missile(F_positionx, F_positiony, F_heading, Ftimer, "Blue")
        F_missilesArray.append(m)

    if pg.key.get_pressed()[pg.K_DOWN] and Emwait > 100: #Enemy Missile Launch
        Emwait = 0
        Etimer = 0
        m = Missile(E_positionx, E_positiony, E_heading, Etimer, "Red")
        E_missilesArray.append(m)

    pg.draw.rect(screen, black, scrrect)
    screen.blit(ship, shiprect)
    screen.blit(enemy, enemyrect)

    for missile in F_missilesArray:
        missile.render(screen)
        missile.update()

        if missile.timer > 100:
            F_missilesArray.pop(0)
            isExploding = True
            missiletemp = 1
            xpos = missile.posx
            ypos = missile.posy

    for missile in E_missilesArray:
        missile.render(screen)
        missile.update()

        if missile.timer > 100:
            E_missilesArray.pop(0)
            isExploding = True
            missiletemp = 1
            xpos = missile.posx
            ypos = missile.posy
#Missile Destruction Animation
    if isExploding and missiletemp <5:
        timeafterexplosion += 1
        exp = explosions[missiletemp]
        explosionrect = exp.get_rect()
        explosionrect.centerx = xpos
        explosionrect.centery = ypos
        screen.blit(exp, explosionrect)

    if timeafterexplosion % 16 == 0:
        missiletemp += 1
        
    elif missiletemp == len(explosions):
        timeafterexplosion = 1
        isExploding = False
        missiletemp = 0

    print(missiletemp)
    Emwait += 1
    Fmwait += 1
    pg.display.flip() 
    if keys[pg.K_TAB]:
            running = False    
    pg.time.Clock().tick(refreshRate)       