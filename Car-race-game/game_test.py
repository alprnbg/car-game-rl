from game import CarGame

myGame = CarGame()

myGame.init()
myGame.reset()

action = 2

while(True):
	myGame.step(action)
	if myGame.done:
		myGame.reset()
