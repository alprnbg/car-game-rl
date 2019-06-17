import pygame, random, sys ,os,time
from pygame.locals import *


# reset
# step(action)
# render
# close
# get_screen

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
        self.count=3

    def terminate(self):
        pygame.quit()
        sys.exit()

    def waitForPlayerToPressKey(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: #escape quits
                        terminate()
                    return

    def playerHasHitBaddie(self, playerRect, baddies):
        for b in baddies:
            if playerRect.colliderect(b['rect']):
                return True # ÇARPMA
        return False

    def drawText(self, text, font, surface, x, y):
        textobj = font.render(text, 1, TEXTCOLOR)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('car race')
pygame.mouse.set_visible(False)

# fonts
font = pygame.font.SysFont(None, 30)

# sounds
gameOverSound = pygame.mixer.Sound('music/crash.wav')
pygame.mixer.music.load('music/car.wav')
laugh = pygame.mixer.Sound('music/laugh.wav')


# images
playerImage = pygame.image.load('image/car1.png')
car3 = pygame.image.load('image/car3.png')
car4 = pygame.image.load('image/car4.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('image/car2.png')
sample = [car3,car4,baddieImage]
wallLeft = pygame.image.load('image/left.png')
wallRight = pygame.image.load('image/right.png')



# "Start" screen
drawText('Press any key to start the game.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
drawText('And Enjoy', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3)+30)
pygame.display.update()
waitForPlayerToPressKey()
zero=0
if not os.path.exists("data/save.dat"):
    f=open("data/save.dat",'w')
    f.write(str(zero))
    f.close()
v=open("data/save.dat",'r')
topScore = int(v.readline())
v.close()
while (True):
    # start of the game
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    x, y = playerRect.topleft

    left_sensor = pygame.Rect(x, y+23, 1, 1)
    left_top_sensor = pygame.Rect(x, y, 1, 1)
    top_sensor = pygame.Rect(x+11, y, 1, 1)
    right_top_sensor = pygame.Rect(x+23, y, 1, 1)
    right_sensor = pygame.Rect(x+23, y+23, 1, 1)

    sensors = [left_sensor,left_top_sensor,top_sensor,right_top_sensor,right_sensor]

    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)



    while True: # the game loop
        score += 1 # increase score

        for event in pygame.event.get():

            if event.type == QUIT:
                terminate()

            OUTPUT MODELRUN(SENSORS)

            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True


        # Add new baddies at the top of the screen
        baddieAddCounter += 1

        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize =30
            newBaddie = {'rect': pygame.Rect(random.randint(140, 485), 0 - baddieSize, 23, 47),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(random.choice(sample), (23, 47)),
                        }
            baddies.append(newBaddie)
            sideLeft= {'rect': pygame.Rect(0,0,126,600),
                       'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                       'surface':pygame.transform.scale(wallLeft, (126, 599)),
                       }
            baddies.append(sideLeft)
            sideRight= {'rect': pygame.Rect(497,0,303,600),
                       'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                       'surface':pygame.transform.scale(wallRight, (303, 599)),
                       }
            baddies.append(sideRight)



        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)

        x, y = playerRect.topleft

        left_sensor = pygame.Rect(x, y+23, 1, 1)
        left_top_sensor = pygame.Rect(x, y, 1, 1)
        top_sensor = pygame.Rect(x+11, y, 1, 1)
        right_top_sensor = pygame.Rect(x+23, y, 1, 1)
        right_sensor = pygame.Rect(x+23, y+23, 1, 1)

        sensors = [left_sensor,left_top_sensor,top_sensor,right_top_sensor,right_sensor]


        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)




        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 128, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface,128, 20)
        drawText('Rest Life: %s' % (count), font, windowSurface,128, 40)

        windowSurface.blit(playerImage, playerRect)


        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the car have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                g=open("data/save.dat",'w')
                g.write(str(score))
                g.close()
                topScore = score
            break

        mainClock.tick(FPS)

    # "Game Over" screen.
    pygame.mixer.music.stop()
    count=count-1
    gameOverSound.play()
    time.sleep(1)
    if (count==0):
     laugh.play()
     drawText('Game over', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
     drawText('Press any key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 30)
     pygame.display.update()
     time.sleep(2)
     waitForPlayerToPressKey()
     count=3
     gameOverSound.stop()
