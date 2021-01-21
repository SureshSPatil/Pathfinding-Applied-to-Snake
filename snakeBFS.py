import pygame, random, sys

pygame.init()

cellWidth = 15
gameSize = 20
if(len(sys.argv) > 1): 
	gameSize = int(sys.argv[1]);
buff = 1
growth = 5

winWidth = (cellWidth + buff) * gameSize # 22 * 40
winHeight = (cellWidth + buff) * gameSize

win = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("SNAKE")

board = [[0 for i in range(0, gameSize)] for j in range(0, gameSize)]

snake = [[random.randint(gameSize//4, gameSize - gameSize//4), random.randint(gameSize//4, gameSize - gameSize//4)]]
print(snake)

score = 0

boardTup = set(tuple([xB, yB]) for yB in range(0, gameSize) for xB in range(0, gameSize))

def generateFood():
	snakeTup = set(tuple(snakePix) for snakePix in snake)
	possibleLoc = list(boardTup - snakeTup)
	chosenLoc = list(possibleLoc[random.randint(0, len(possibleLoc) - 1)])
	
	board[chosenLoc[1]][chosenLoc[0]] = 2

	#board[4][4] = 2
	#print(chosenLoc)
	return chosenLoc

foodLoc = [-2, -2]
foodLoc = generateFood()


def redrawGameWindow():
	# win.fill((135, 206, 235))
	# win.blit(bg, (0, 0))
	# win.blit(bird, (x, y))
	pygame.draw.rect(win, (0, 0, 0), (0, 0, winWidth, winHeight))

	# for pipe in pipes:
	# 	pygame.draw.rect(win, (0, 255, 0), pipe[0])
	# 	pygame.draw.rect(win, (0, 255, 0), pipe[1])

	for j in range(0, gameSize):
		for i in range(0, gameSize):
			if (j + i)%2 >= 0:
				pygame.draw.rect(win, (1, 50, 32), (i*(buff + cellWidth), j*(buff + cellWidth) + buff, cellWidth, cellWidth))
			else:
				pygame.draw.rect(win, (	0, 250, 154), (i*(buff + cellWidth), j*(buff + cellWidth) + buff, cellWidth, cellWidth))
			# if board[j][i] == 1:
			# 	pygame.draw.rect(win, (255, 255, 255), (i*(buff + cellWidth), j*(buff + cellWidth) + buff, cellWidth, cellWidth), 1)
			if board[j][i] == 2:
				pygame.draw.rect(win, (255, 0, 0), (i*(buff + cellWidth), j*(buff + cellWidth) + buff, cellWidth, cellWidth))

	for snakePixel in snake:
		# print((snakePixel[1]*(buff + cellWidth), snakePixel[0]*(buff + cellWidth) + buff, cellWidth, cellWidth))
		pygame.draw.rect(win, (0, 0, 255), (snakePixel[0]*(buff + cellWidth), snakePixel[1]*(buff + cellWidth) + buff, cellWidth, cellWidth))

	# if foodLoc[0] != -1:
	# 	pygame.draw.rect(win, (255, 0, 0), (foodLoc[0]*(buff + cellWidth), foodLoc[1]*(buff + cellWidth) + buff, cellWidth, cellWidth), 1)

	font = pygame.font.Font('freesansbold.ttf', 12) 
	text = font.render('Score: ' + str(score), True, (255, 0, 255)) 
	textRect = text.get_rect()   
	textRect.center = (winWidth // 2, winHeight // 8) 

	win.blit(text, textRect)

	pygame.display.update()

# bird = pygame.image.load('bird.png')
# bg = pygame.image.load('background.png')

deltaTime = 100
run = True


direction = 0
incJ = 0
incI = 1

snakeLenProg = 0

def inBounds(snakeCoords):
	return (0 <= snakeCoords[0] < gameSize) and (0 <= snakeCoords[1] < gameSize)

def snakeBFS(foodLoc, snakeQueue, directionQueue, alreadyTraveled, snakeLenProg):
	if(len(snakeQueue) == 0):
		return []
	curSnake = snakeQueue.pop(0)
	curDirection = directionQueue.pop(0)
	while not ((0 <= curSnake[0][0] < gameSize) and (0 <= curSnake[0][1] < gameSize) and (curSnake[0] not in curSnake[1:]) and (curSnake[0] not in alreadyTraveled)):
		if(len(snakeQueue) == 0):
			return []
		curSnake = snakeQueue.pop(0)
		curDirection = directionQueue.pop(0)

	if(foodLoc[0] == curSnake[0][0] and foodLoc[1] == curSnake[0][1]):
		return curDirection
	else:
		newSnake = [snakePix[:] for snakePix in curSnake]
		newSnake.insert(0, [newSnake[0][0] + 1, newSnake[0][1]])
		if not (snakeLenProg > 0):
			newSnake.pop(-1)
		snakeQueue.append(newSnake)

		newSnake = [snakePix[:] for snakePix in curSnake]
		newSnake.insert(0, [newSnake[0][0], newSnake[0][1] - 1])
		if not (snakeLenProg > 0):
			newSnake.pop(-1)
		snakeQueue.append(newSnake)

		newSnake = [snakePix[:] for snakePix in curSnake]
		newSnake.insert(0, [newSnake[0][0] - 1, newSnake[0][1]])
		if not (snakeLenProg > 0):
			newSnake.pop(-1)
		snakeQueue.append(newSnake)

		newSnake = [snakePix[:] for snakePix in curSnake]
		newSnake.insert(0, [newSnake[0][0], newSnake[0][1] + 1])
		if not (snakeLenProg > 0):
			newSnake.pop(-1)
		snakeQueue.append(newSnake)
		for d in range(0, 4):
			newDirection = curDirection[:]
			newDirection.append(d)
			directionQueue.append(newDirection)


		alreadyTraveled.append(curSnake[0])
		return snakeBFS(foodLoc, snakeQueue, directionQueue, alreadyTraveled, snakeLenProg - 1)


def nextMove(foodLoc, snake, direction, snakeLenProg):
	directionList = snakeBFS(foodLoc, [[snakePix[:] for snakePix in snake]], [[]], [], snakeLenProg)
	if(directionList == None or len(directionList) == 0):
		if(inBounds([snake[0][0] + 1, snake[0][1]]) and ([snake[0][0] + 1, snake[0][1]] not in snake) and direction != 2):
			return 0
		elif(inBounds([snake[0][0], snake[0][1] - 1]) and ([snake[0][0], snake[0][1] - 1] not in snake) and direction != 3):
			return 1
		elif(inBounds([snake[0][0] - 1, snake[0][1]]) and ([snake[0][0] - 1, snake[0][1]] not in snake) and direction != 0):
			return 2
		elif(inBounds([snake[0][0], snake[0][1] + 1]) and ([snake[0][0] , snake[0][1] + 1] not in snake) and direction != 1):
			return 3
		else:
			return 0
	
	return directionList[0]

while run:
	pygame.time.delay(deltaTime)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	keys = pygame.key.get_pressed()
	if direction != -1:

		if board[snake[0][1]][snake[0][0]] == 2:
			snakeLenProg += growth
			# snakeEatLoc = [snake[0][1], snake[0][0]]
			board[snake[0][1]][snake[0][0]] = 0
			foodLoc = generateFood()
			#print(foodLoc)

		if snakeLenProg > 0:
			snake.append([snake[-1][0], snake[-1][1]])
			snakeLenProg -= 1

		nextDirection = nextMove(foodLoc, snake[:], direction, snakeLenProg + 1)

		if(len(snake) > 1):
			if nextDirection == 0 and direction != 2:
				direction = 0
				incJ = 0
				incI = 1
			elif nextDirection == 1 and direction != 3:
				direction = 1
				incJ = -1
				incI = 0
			elif nextDirection == 2 and direction != 0:
				direction = 2
				incJ = 0
				incI = -1
			elif nextDirection == 3 and direction != 1:
				direction = 3
				incJ = 1
				incI = 0
		else:
			if nextDirection == 0:
				direction = 0
				incJ = 0
				incI = 1
			elif nextDirection == 1:
				direction = 1
				incJ = -1
				incI = 0
			elif nextDirection == 2:
				direction = 2
				incJ = 0
				incI = -1
			elif nextDirection == 3:
				direction = 3
				incJ = 1
				incI = 0

		#print(direction)




		snake = ([[snake[0][0] + incI, snake[0][1] + incJ]] + snake)[0:-1]

		score = len(snake) - 1

	if not (0 <= snake[0][0] < gameSize):
		# run = False	
		direction = -1
		incJ = 0
		incI = 0
	elif not (0 <= snake[0][1] < gameSize):
		# run = False	
		direction = -1
		incJ = 0
		incI = 0
	elif (snake[0] in snake[1:]):#len(snake) > len(set([tuple(snakePix) for snakePix in snake])):
		direction = -1
		incJ = 0
		incI = 0

	redrawGameWindow()
	

pygame.quit()
print("Score:", score)
