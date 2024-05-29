import pygame as pg
import numpy
import random

pg.init()
width, height = 1920, 1080
resolution = (width,height)
screen = pg.display.set_mode(resolution)
scrrect = screen.get_rect()
black = (0, 0, 0)
white = (255, 255, 255)
refreshRate = 60 #Hz

ship = pg.image.load('Player.png')
ship = pg.transform.scale(ship, (128, 96))
enemy = pg.image.load('Enemy.png')
enemy = pg.transform.scale(enemy, (128, 96))
missileText = pg.image.load('missile.png')
missileText = pg.transform.scale(missileText, (128, 96))

explodeSound = pg.mixer.Sound('explosion.wav')
music =[]
for i in range(2): music.append(pg.mixer.Sound('music' + str(i+1) + '.mp3'))
song = music[random.randint(0,1)]
song.play()

shiprect, enemyrect, missilerect = ship.get_rect(), enemy.get_rect(), missileText.get_rect()
shiprect.centerx, enemyrect.centerx = 250, 500
shipDir = []
enemyDir = []
missileDir = []
F_missilesArray = []
E_missilesArray = []
explosions = []
Emwait, Fmwait = 0, 0
speed, missileSpeed = 8, 24
Fscore, Escore = 0, 0
running = True
F_heading, E_heading = 0, 180
isExploding = False
timeafterexplosion, missiletemp = 1, 0
FisDead, EisDead = False, False
wait = -0
font = pg.font.Font('freesansbold.ttf', 32)

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
        missilerect.centerx, missilerect.centery = self.posx, self.posy
        screen.blit(missileText, missilerect)

def turnLeft(heading):
    heading -= round(180/refreshRate)
    if heading < 0: heading += 360
    return heading

def turnRight(heading):
    heading += round(180/refreshRate)
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
         E_heading = turnLeft(E_heading)
         enemyrect = enemy.get_rect()
         enemy = enemyDir[E_heading]

    elif keys[pg.K_LEFT]:
         E_heading = turnRight(E_heading)
         enemyrect = enemy.get_rect()
         enemy = enemyDir[E_heading]
#Movement
    F_positionx += speed*numpy.cos(numpy.radians(F_heading))
    F_positiony -= speed*numpy.sin(numpy.radians(F_heading))

    E_positionx += speed*numpy.cos(numpy.radians(E_heading))
    E_positiony -= speed*numpy.sin(numpy.radians(E_heading))

    shiprect.centerx, shiprect.centery = F_positionx, F_positiony
    enemyrect.centerx, enemyrect.centery = E_positionx, E_positiony

#Resets position when out of bounds
    F_positionx %= width
    F_positiony %= height
    E_positionx %= width
    E_positiony %= height

#Missiles
    if pg.key.get_pressed()[pg.K_s] and Fmwait > 60: #Friendly Missile Launch
        Fmwait, Ftimer = 0, 0
        m = Missile(F_positionx, F_positiony, F_heading, Ftimer, "Blue")
        F_missilesArray.append(m)

    if pg.key.get_pressed()[pg.K_DOWN] and Emwait > 60: #Enemy Missile Launch
        Emwait, Etimer = 0, 0
        m = Missile(E_positionx, E_positiony, E_heading, Etimer, "Red")
        E_missilesArray.append(m)

    text = font.render(str(Fscore) + ' | ' + str(Escore), True, white, black)

    textRect = text.get_rect()
    textRect.center = (1920/2 , 900)

    pg.draw.rect(screen, black, scrrect)
    screen.blit(ship, shiprect)
    screen.blit(enemy, enemyrect)
    screen.blit(text, textRect)

#Looping through Friendly missile array 
    for missile in F_missilesArray:
        missile.render(screen)
        missile.update()

        if missile.timer > 60:
            F_missilesArray.pop(0)
            isExploding, missiletemp = True, 1
            xpos, ypos = missile.posx, missile.posy
        
        if abs(E_positionx - missile.posx) < 40 and abs(E_positiony - missile.posy) < 40:
            missile.timer = 61
            EisDead = True

    if EisDead == True:
        Fscore += 1
        EisDead = False
        explodeSound.play()
        speed = 0
        wait = 1
        
#Looping through Enemy missile array
    for missile in E_missilesArray:
        missile.render(screen)
        missile.update()

        if missile.timer > 60:
            E_missilesArray.pop(0)
            isExploding, missiletemp = True, 1
            xpos, ypos = missile.posx, missile.posy

        if abs(F_positionx - missile.posx) < 40 and abs(F_positiony - missile.posy) < 40:
            missile.timer = 61
            FisDead = True

    if FisDead == True:
        Escore += 1
        FisDead = False
        explodeSound.play()
        F_heading, E_heading, 0, 180
        wait = 1

    if 0 < wait < 200:
        wait += 1
        speed = 0
        E_heading, F_heading = 180, 0
        enemy, ship = enemyDir[180], shipDir[0]

    elif wait > 199:
        wait = 0
        E_positionx, E_positiony = 400, 540
        F_positionx, F_positiony = width-400, 540

    elif wait == 0:
        speed = 8

#Missile Destruction Animation
    if isExploding and missiletemp <5:
        timeafterexplosion += 1
        exp = explosions[missiletemp]
        explosionrect = exp.get_rect()
        explosionrect.centerx, explosionrect.centery = xpos, ypos
        screen.blit(exp, explosionrect)

    if timeafterexplosion % 10 == 0:
        missiletemp += 1
        
    elif missiletemp == len(explosions):
        timeafterexplosion, missiletemp, isExploding = 1, 0, False

    Emwait += 1
    Fmwait += 1


    pg.display.flip() 
    if keys[pg.K_TAB]:
            running = False    
    pg.time.Clock().tick(refreshRate)       