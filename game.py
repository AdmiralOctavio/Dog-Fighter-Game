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
speed = 3
missileSpeed = 15
running = True
F_heading = 0
E_heading = 180

class Missile:
    def __init__(self, posx, posy, heading):
        self.posx = posx
        self.posy = posy
        self.heading = heading
    
    def update(self):
        self.posx += missileSpeed*numpy.cos(numpy.radians(self.heading))
        self.posy -= missileSpeed*numpy.sin(numpy.radians(self.heading))

    def render(self, screen):
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

setup()
missilerect = missileText.get_rect()
#Friendly Position
F_positionx = width-500
F_positiony = 540
#Enemy Position
E_positionx = 500
E_positiony = 540
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
    if pg.key.get_pressed()[pg.K_SPACE]:
        m = Missile(F_positionx, F_positiony, F_heading)
        F_missilesArray.append(m)
        print("balls")
        time.sleep(0.5)
    
    for missile in F_missilesArray:
        missile.render(screen)
        missile.update()


            

    pg.draw.rect(screen, black, scrrect)
    screen.blit(ship, shiprect)
    screen.blit(enemy, enemyrect)

    pg.display.flip() 
    if keys[pg.K_TAB]:
            running = False    
    pg.time.Clock().tick(refreshRate)       