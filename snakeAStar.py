import pygame, random, sys

pygame.init()

cellWidth = 15
gameSize = 40
if(len(sys.argv) > 1):
	gameSize = int(sys.argv[1])
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

	for index,snakePixel in enumerate(snake):
		# print((snakePixel[1]*(buff + cellWidth), snakePixel[0]*(buff + cellWidth) + buff, cellWidth, cellWidth))
		pygame.draw.rect(win, (0, 0, 255), (snakePixel[0]*(buff + cellWidth), snakePixel[1]*(buff + cellWidth) + buff, cellWidth, cellWidth))
		if index == 0:
			pygame.draw.rect(win, (0, 255, 0), (snakePixel[0]*(buff + cellWidth), snakePixel[1]*(buff + cellWidth) + buff, cellWidth, cellWidth))

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

def manhattanDistance(coord1, coord2):
	return (abs(coord2[0] - coord1[0]) + abs(coord2[1] - coord1[1]))

def find2D(findList, value):
	for index, x in enumerate(findList):
		if x[0] == value:
			return index
	return -1

def nextTo(snakeVals):
	if [snakeVals[0][0] + 1, snakeVals[0][1]] in snakeVals or [snakeVals[0][0], snakeVals[0][1] + 1] in snakeVals or [snakeVals[0][0] - 1, snakeVals[0][1]] or snakeVals [snakeVals[0][0], snakeVals[0][1] - 1] in snakeVals:
		return True
	return False

def snakeBFS(foodLoc, snakeData, alreadyTraveled, depth):

	if(len(snakeData) == 0 or depth == 993):
		return []
	curData = snakeData.pop(0)
	curSnake = curData[1]
	curDirection = curData[2]
	curSnakeLenProg = curData[3]
	curDistance = curData[4]
	

	while not ((0 <= curSnake[0][0] < gameSize) and (0 <= curSnake[0][1] < gameSize) and (curSnake[0] not in curSnake[1:]) and (curSnake[0] not in alreadyTraveled)):
		if(len(snakeData) == 0):
			return []
		curData = snakeData.pop(0)
		curSnake = curData[1]
		curDirection = curData[2]
		curSnakeLenProg = curData[3]
		curDistance = curData[4]
	

	if(foodLoc[0] == curSnake[0][0] and foodLoc[1] == curSnake[0][1]):
		return curDirection
	else:
		bias = 0
		if(nextTo(curSnake)):
			bias -= 0.1

		newSnake = [snakePix[:] for snakePix in curSnake]
		newSnake.insert(0, [newSnake[0][0] + 1, newSnake[0][1]])
		newSnakeLenProg = curSnakeLenProg
		if (curSnakeLenProg == 0):
			newSnake.pop()
		else:
			newSnakeLenProg -= 1

		newDistance = curDistance + 1
		newDirection = curDirection[:]
		newDirection.append(0)
		newSnakeData = [bias + newDistance + manhattanDistance(newSnake[0], foodLoc), newSnake, newDirection, newSnakeLenProg, newDistance]
		snakeData.append(newSnakeData)
		#snakeData = sorted(snakeData, key=lambda l:l[0])

		newSnake = [snakePix[:] for snakePix in curSnake]
		newSnake.insert(0, [newSnake[0][0], newSnake[0][1] - 1])
		newSnakeLenProg = curSnakeLenProg
		if (curSnakeLenProg == 0):
			newSnake.pop()
		else:
			newSnakeLenProg -= 1
		newDistance = curDistance + 1
		newDirection = curDirection[:]
		newDirection.append(1)
		newSnakeData = [bias + newDistance + manhattanDistance(newSnake[0], foodLoc), newSnake, newDirection, newSnakeLenProg, newDistance]
		snakeData.append(newSnakeData)
		#snakeData = sorted(snakeData, key=lambda l:l[0])

		newSnake = [snakePix[:] for snakePix in curSnake]
		newSnake.insert(0, [newSnake[0][0] - 1, newSnake[0][1]])
		newSnakeLenProg = curSnakeLenProg
		if (curSnakeLenProg == 0):
			newSnake.pop()
		else:
			newSnakeLenProg -= 1
		newDistance = curDistance + 1
		newDirection = curDirection[:]
		newDirection.append(2)
		newSnakeData = [bias + newDistance + manhattanDistance(newSnake[0], foodLoc), newSnake, newDirection, newSnakeLenProg, newDistance]
		snakeData.append(newSnakeData)
		#snakeData = sorted(snakeData, key=lambda l:l[0])

		newSnake = [snakePix[:] for snakePix in curSnake]
		newSnake.insert(0, [newSnake[0][0], newSnake[0][1] + 1])
		newSnakeLenProg = curSnakeLenProg
		if (curSnakeLenProg == 0):
			newSnake.pop()
		else:
			newSnakeLenProg -= 1
		newDistance = curDistance + 1
		newDirection = curDirection[:]
		newDirection.append(3)
		newSnakeData = [bias + newDistance + manhattanDistance(newSnake[0], foodLoc), newSnake, newDirection, newSnakeLenProg, newDistance]
		snakeData.append(newSnakeData)
		
		snakeData = sorted(snakeData, key=lambda l:l[0])
		
#		for d in range(0, 4):
#			newDirection = curDirection[:]
#			newDirection.append(d)
#			directionQueue.append(newDirection)
#

		alreadyTraveled.append(curSnake[0])	

		return snakeBFS(foodLoc, snakeData, alreadyTraveled, depth + 1)


def nextMove(foodLoc, snake, direction, snakeLenProg):
	directionList = snakeBFS(foodLoc, [[manhattanDistance(snake[0], foodLoc), [snakePix[:] for snakePix in snake], [], snakeLenProg, 0]], [], 0)
	if(directionList == None or len(directionList) == 0):
		directionList = snakeBFS(snake[-1][:], [[manhattanDistance(snake[0], snake[-1][:]), [snakePix[:] for snakePix in snake], [], snakeLenProg, 0]], [], 0)
		print('here')
		if(directionList == None or len(directionList) == 0):
			if(inBounds([snake[0][0] + 1, snake[0][1]]) and ([snake[0][0] + 1, snake[0][1]] not in snake) and direction != 2):
				return [0]
			elif(inBounds([snake[0][0], snake[0][1] - 1]) and ([snake[0][0], snake[0][1] - 1] not in snake) and direction != 3):
				return [1]
			elif(inBounds([snake[0][0] - 1, snake[0][1]]) and ([snake[0][0] - 1, snake[0][1]] not in snake) and direction != 0):
				return [2]
			elif(inBounds([snake[0][0], snake[0][1] + 1]) and ([snake[0][0] , snake[0][1] + 1] not in snake) and direction != 1):
				return [3]
			else:
				return [0]
	
	return directionList

nextDirections = []
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

		if len(nextDirections) == 0: 
			nextDirections = nextMove(foodLoc, snake[:], direction, snakeLenProg)
		nextDirection = nextDirections.pop(0)


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

		if snakeLenProg > 0:
			snake.append([snake[-1][0], snake[-1][1]])
			snakeLenProg -= 1


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
