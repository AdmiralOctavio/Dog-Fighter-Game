import pygame as pg
import numpy
import time

pg.init()
resolution = (1920,1080)
screen = pg.display.set_mode(resolution)
scrrect = screen.get_rect()
black =(0, 0, 0)
refreshRate = 144 #Hz

ship = pg.image.load('Player.png')
ship = pg.transform.scale(ship, (128, 96))
enemy = pg.image.load('Enemy.png')
enemy = pg.transform.scale(enemy, (128, 96))
missile = pg.image.load('missile.png')
missile = pg.transform.scale(missile, (128, 96))

shiprect = ship.get_rect()
shiprect.centerx = 250
enemyrect = enemy.get_rect()
enemyrect.centerx = 500
missilerect = missile.get_rect()

shipDir = []
enemyDir = []
missileDir = []

speed = 3

running = True
heading = 0

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
        missileDir.append(pg.transform.rotate(missile, i))

setup()

positionx = 540
positiony = 540
while running:
    pg.event.pump()
    keys = pg.key.get_pressed()

    if keys[pg.K_a]:
         heading = turnRight(heading)
         shiprect = ship.get_rect()
         ship = shipDir[heading]

    elif keys[pg.K_d]:
         heading = turnLeft(heading)
         shiprect = ship.get_rect()
         ship = shipDir[heading]
    
    positionx += speed*numpy.cos(numpy.radians(heading))
    positiony -= speed*numpy.sin(numpy.radians(heading))

    shiprect.centerx = positionx
    shiprect.centery = positiony

    pg.draw.rect(screen, black, scrrect)
    screen.blit(ship, shiprect)
    pg.display.flip() 
    if keys[pg.K_TAB]:
            running = False    
    pg.time.Clock().tick(refreshRate)       