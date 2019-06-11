from game import CarGame

myGame = CarGame()

myGame.init()
myGame.reset()

action = 1

while(True):
    myGame.step(action) 
