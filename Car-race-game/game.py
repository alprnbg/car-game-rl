import pygame, random, sys ,os,time
from pygame.locals import *


"""
def run_sensor(sensors):
    sensor_values = [0,0,0,0,0]
    stop = [False,False,False,False,False]
    step = 0
    while(step <= 50):
        for sensor_id in range(5):
            if stop[sensor_id] == True:
                continue

            for b in baddies:
                if sensors[sensor_id].colliderect(b['rect']):
                    stop[sensor_id] = True

            if sensor_id == 0:
                sensors[sensor_id].move_ip(-1,0)
            elif sensor_id == 1:
                sensors[sensor_id].move_ip(-1,-1)
            elif sensor_id == 2:
                sensors[sensor_id].move_ip(0,-1)
            elif sensor_id == 3:
                sensors[sensor_id].move_ip(1,-1)
            elif sensor_id == 4:
                sensors[sensor_id].move_ip(1,0)

            sensor_values[sensor_id] += 1
        step += 1

    return sensor_values
"""

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if b['type']=='car' and playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y, color):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


mainClock = None
windowSurface = None
font = None
playerImage = None
car3 = None
car4 = None
playerRect = None
baddieImage = None
sample = None
wallLeft = None
wallRight = None


class CarGame:
    def __init__(self):
        self.action_space = ['A', 'D']
        self.WINDOWWIDTH = 800
        self.WINDOWHEIGHT = 600
        self.TEXTCOLOR = (255, 255, 255)
        self.BACKGROUNDCOLOR = (0, 0, 0)
        self.FPS = 40
        self.BADDIEMINSIZE = 10
        self.BADDIEMAXSIZE = 40
        self.BADDIEMINSPEED = 8
        self.BADDIEMAXSPEED = 8
        self.ADDNEWBADDIERATE = 6
        self.PLAYERMOVERATE = 5
        self.done = None
        self.baddies = None
        self.sensors = None
        self.sensor_outputs = None
        self.baddieAddCounter = None
        self.score = None
        self.topScore = 0


    def render(self):
        pass


    def close(self):
        pygame.quit()
        sys.exit()

    def init(self):
        global mainClock
        global windowSurface
        global font
        global playerImage
        global car3
        global car4
        global playerRect
        global baddieImage
        global sample
        global wallLeft
        global wallRight

        pygame.init()
        mainClock = pygame.time.Clock()
        windowSurface = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        pygame.display.set_caption('car race')
        pygame.mouse.set_visible(False)

        # fonts
        font = pygame.font.SysFont(None, 30)

        # images
        playerImage = pygame.image.load('image/car1.png')
        car3 = pygame.image.load('image/car3.png')
        car4 = pygame.image.load('image/car4.png')
        playerRect = playerImage.get_rect()
        baddieImage = pygame.image.load('image/car2.png')
        sample = [car3,car4,baddieImage]
        wallLeft = pygame.image.load('image/left.png')
        wallRight = pygame.image.load('image/right.png')

    def reset(self):
        # start of the game
        self.done = False
        self.baddies = []
        self.score = 0

        playerRect.topleft = (self.WINDOWWIDTH / 2, self.WINDOWHEIGHT - 50)
        self.baddieAddCounter = 0



    def step(self, action):
        self.score += 1 # increase score

        if action == 0:
            moveLeft = True
            moveRight = False
        elif action == 1:
            moveLeft = False
            moveRight = False
        elif action == 2:
            moveLeft = False
            moveRight = True

        self.baddieAddCounter += 1

        if self.baddieAddCounter == self.ADDNEWBADDIERATE:
            self.baddieAddCounter = 0
            baddieSize = 30
            newBaddie = {'rect': pygame.Rect(random.randint(140, 485), 0 - baddieSize, 23, 47),
                         'speed': random.randint(self.BADDIEMINSPEED, self.BADDIEMAXSPEED),
                         'surface':pygame.transform.scale(random.choice(sample), (23, 47)),
                         'type':'car'
                         }
            self.baddies.append(newBaddie)
            sideLeft= {'rect': pygame.Rect(0,0,126,600),
                       'speed': random.randint(self.BADDIEMINSPEED, self.BADDIEMAXSPEED),
                       'surface':pygame.transform.scale(wallLeft, (126, 599)),
                       'type':'wall'
                      }
            self.baddies.append(sideLeft)
            sideRight= {'rect': pygame.Rect(497,0,303,600),
                        'speed': random.randint(self.BADDIEMINSPEED, self.BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(wallRight, (303, 599)),
                        'type':'wall'
                       }
            self.baddies.append(sideRight)

        if moveLeft and playerRect.left > 126:
            playerRect.move_ip(-1 * self.PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < 497:
            playerRect.move_ip(self.PLAYERMOVERATE, 0)

        #x, y = playerRect.topleft
        #left_sensor = pygame.Rect(x, y+23, 1, 1)
        #left_top_sensor = pygame.Rect(x, y, 1, 1)
        #top_sensor = pygame.Rect(x+11, y, 1, 1)
        #right_top_sensor = pygame.Rect(x+23, y, 1, 1)
        #right_sensor = pygame.Rect(x+23, y+23, 1, 1)
        #self.sensors = [left_sensor,left_top_sensor,top_sensor,right_top_sensor,right_sensor]

        for b in self.baddies:
            b['rect'].move_ip(0, b['speed'])



        for b in self.baddies[:]:
            if b['rect'].top > self.WINDOWHEIGHT:
                self.baddies.remove(b)

        # Draw the game world on the window.
        windowSurface.fill(self.BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Score: %s' % (self.score), font, windowSurface, 128, 0, self.TEXTCOLOR)
        drawText('Top Score: %s' % (self.topScore), font, windowSurface,128, 20, self.TEXTCOLOR)

        windowSurface.blit(playerImage, playerRect)


        for b in self.baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        reward = 1

        # Check if any of the car have hit the player.
        if playerHasHitBaddie(playerRect, self.baddies):
            if self.score > self.topScore:
                self.topScore = self.score
            self.done = True
            reward = -1

        mainClock.tick(self.FPS)

        return (None, reward, self.done, None)
