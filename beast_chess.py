import random, pygame, sys
from pygame.locals import *
import os

FPS = 30

WINDOWWIDTH = 450
WINDOWHEIGHT = 560
XMARGIN = 10
YMARGIN = 10
BOXSIZE = 100
GAPSIZE = 10
ROWNUM = 5
COLUMNSNUM = 4

WHITE = (255, 255, 255)
BLAK  = (0, 0, 0)
GRAY = (200, 200, 200)
GRAY2 = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

GRAYH = (150, 150, 150)
REDH = (255, 100, 100)
BLUEH = (100, 100, 255)

BKCOLOR = GRAY2
BOARDCOLOR = GRAY
SELECTCOLOR = ORANGE
MIDAREACOLOR = CYAN
GAPLINECOLOR = BLAK
FONTCOLOR = WHITE
PIECECOLORS = (GRAY, RED, BLUE, GRAYH, REDH, BLUEH, ORANGE, BKCOLOR)
PIECESHAPES = ("", "Mouse", "Cat", "Dog", "Wolf", "Leopard", "Lion", "Tiger", "Elephant", "", "HOLE", "RIVER", "MOUNT", "HOLE")
elemNum = 8

selectLineSize = 4
clearLineSize = 10

selectFlag = True

def getOriginalDispContent():
	print("getOriginalDispContent")
	pieceShapeList = [i for i in range(1, elemNum * 2 + 1)]
	print(pieceShapeList)
	random.shuffle(pieceShapeList)
	print(pieceShapeList)
	pieceColorList = []
	for i in range(len(pieceShapeList)):
		if pieceShapeList[i] > elemNum:
			pieceShapeList[i] = pieceShapeList[i] - elemNum
			randColorFlag = 1
		else:
			randColorFlag = 2
		pieceColorList.append(randColorFlag)
	
	pieceEle = []
	for i in range(len(pieceShapeList) + 4):
		if i > 7 and i < 12:
			if i == 8:
				pieceEle.append((10, 6))
			elif i == 9:
				pieceEle.append((11, 6))
			elif i == 10:
				pieceEle.append((12, 6))
			else:
				pieceEle.append((13, 6))
		elif i > 11:
			pieceEle.append((pieceShapeList[i - 4], pieceColorList[i - 4]))
		else:
			pieceEle.append((pieceShapeList[i], pieceColorList[i]))
	print(pieceEle)
	return pieceEle

def getInitDispContent():
	pieceEle = []
	for i in range(elemNum * 2 + 4):
		if i > 7 and i < 12:
			if i == 8:
				pieceEle.append((10, 6))
			elif i == 9:
				pieceEle.append((11, 6))
			elif i == 10:
				pieceEle.append((12, 6))
			else:
				pieceEle.append((13, 6))
		else:	
			pieceEle.append((9, 0))
	print(pieceEle)
	return pieceEle
	
def policyDecision(currentData, lastClickPos, curClickPos):
	gapX = abs(curClickPos[0] - lastClickPos[0])
	gapY = abs(curClickPos[1] - lastClickPos[1])
	kLast = COLUMNSNUM * lastClickPos[0] + lastClickPos[1]
	kCur = COLUMNSNUM * curClickPos[0] + curClickPos[1]

	# if two points are at the same position
	if currentData[kLast][1] == currentData[kCur][1]:
		clearBoxSelect()
	# if this point has not been turned over
	elif currentData[kLast][1] == GRAY:
		#clearBoxSelect()
		print('ope error')
	# if normal moving
	elif (0 == gapX and 1 == gapY) or (0 == gapY and 1 == gapX):
		# click location is quarantine area, and not chess piece
		if currentData[kCur][0] > 9:
			gotoFlag = False
			if (kCur == 8 or kCur == 11) and currentData[kLast][0] == 1:
				gotoFlag = True
			elif (kCur == 9) and currentData[kLast][0] == 8:
				gotoFlag = True
			elif (kCur == 10) and (currentData[kLast][0] == 2 or currentData[kLast][0] == 3 or currentData[kLast][0] == 4 or currentData[kLast][0] == 5 or currentData[kLast][0] == 6 or currentData[kLast][0] == 7):
				gotoFlag = True
			else:
				gotoFlag = False
			if gotoFlag:
				currentData[kCur] = currentData[kLast]
				currentData[kLast] = (0, 7)
				if lastClickPos[0] == 2:
					currentData[kLast] = (0, 6)
				else:
					currentData[kLast] = (0, 7)
			else:
				print("do nothing")
		# click chess piece
		else:
			n = currentData[kLast][0] - currentData[kCur][0]
			print(n)
			if currentData[kLast][0] > 9:
				print("do nothing")
			# eat
			elif n > 0 or -7 == n:
				currentData[kCur] = currentData[kLast]
				if lastClickPos[0] == 2:
					if kLast == 8:
						currentData[kLast] = (10, 6)
					elif kLast == 9:
						currentData[kLast] = (11, 6)
					elif kLast == 10:
						currentData[kLast] = (12, 6)
					else:
						currentData[kLast] = (13, 6)
				else:
					currentData[kLast] = (0, 7)
				
			# pair
			elif 0 == n:
				currentData[kCur] = (0, 7)
				if lastClickPos[0] == 2:
					if kLast == 8:
						currentData[kLast] = (10, 6)
					elif kLast == 9:
						currentData[kLast] = (11, 6)
					elif kLast == 10:
						currentData[kLast] = (12, 6)
					else:
						currentData[kLast] = (13, 6)
				else:
					currentData[kLast] = (0, 7)
			else:
				print("do nothing")
			clearBoxSelect()
	else:
		print("No-compliant operation!!!!!!!!!!!")
	print(currentData)
	return currentData

def leftTopCoordsOfBox(boxCol, boxRow):
    # Convert board coordinates to pixel coordinates
    left = boxCol * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxRow * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

def drawBoard(dataMatrix):
	fontObj = pygame.font.Font('freesansbold.ttf', 20)
	for i in range(ROWNUM):
		for j in range(COLUMNSNUM):
			k = COLUMNSNUM * i + j
			left, top = leftTopCoordsOfBox(j, i)
			pygame.draw.rect(DISPLAYSURF, PIECECOLORS[dataMatrix[k][1]], (left, top, BOXSIZE, BOXSIZE))
			num = dataMatrix[k][0]
			picPath = os.getcwd()
			if num > 0 and num < 9:
				if 1 == dataMatrix[k][1]:
					imagePath = picPath + '\\pic\\' + PIECESHAPES[num] + '.jpg'
				elif 2 == dataMatrix[k][1]:
					imagePath = picPath + '\\pic\\' + PIECESHAPES[num] + '2.jpg'
				else:
					print('color error')
				myImage = pygame.image.load(imagePath)
				DISPLAYSURF.blit(myImage, (left, top))
			elif num > 9 and num < 14:
				imagePath = picPath + '\\pic\\' + PIECESHAPES[num] + '.jpg'
				myImage = pygame.image.load(imagePath)
				DISPLAYSURF.blit(myImage, (left, top))
			else:
				textSurfaceObj = fontObj.render(PIECESHAPES[dataMatrix[k][0]], True, FONTCOLOR, PIECECOLORS[dataMatrix[k][1]])
				textRectObj = textSurfaceObj.get_rect()
				textRectObj.center = (left + BOXSIZE/2, top + BOXSIZE/2)
				DISPLAYSURF.blit(textSurfaceObj, textRectObj)
				

def clearBoxSelect():
	global selectFlag
	for i in range(ROWNUM + 1):
		pygame.draw.line(DISPLAYSURF, GAPLINECOLOR, (0, i*110+4), (450, i*110+4), clearLineSize)
	for j in range(COLUMNSNUM + 1):
		pygame.draw.line(DISPLAYSURF, GAPLINECOLOR, (j*110+4, 0), (j*110+4, 560), clearLineSize)
	selectFlag = False
			
def drawBoxSelect(left, top, bQuarantineFlag):
	global selectFlag
	if not bQuarantineFlag:
		pygame.draw.line(DISPLAYSURF, SELECTCOLOR, (left - 4, top - 3), (left + BOXSIZE, top - 3), selectLineSize)
		pygame.draw.line(DISPLAYSURF, SELECTCOLOR, (left + BOXSIZE + 1, top - 4), (left + BOXSIZE + 1, top + BOXSIZE), selectLineSize)
		pygame.draw.line(DISPLAYSURF, SELECTCOLOR, (left + BOXSIZE + 3, top + BOXSIZE + 1), (left, top + BOXSIZE + 1), selectLineSize)
		pygame.draw.line(DISPLAYSURF, SELECTCOLOR, (left - 3, top + BOXSIZE + 3), (left - 3, top), selectLineSize)
		selectFlag = True
	
def getBoxAtPixel(x, y):
	for boxRow in range(ROWNUM):
		for boxCol in range(COLUMNSNUM):
			left, top = leftTopCoordsOfBox(boxCol, boxRow)
			boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
			if boxRect.collidepoint(x, y):
				return (boxRow, boxCol)
	return (None, None)

def startGame():
	print("startGame")

def stopGame():
	print("stop game")

def main():
	global FPSCLOCK, DISPLAYSURF
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
	DISPLAYSURF.fill(BKCOLOR)
	pygame.display.set_caption("Arena chess")
	
	initData = getInitDispContent()
	originalData = getOriginalDispContent()
	currentData = initData
	drawBoard(currentData)
	clearBoxSelect()
	
	clickFlag = False
	mousex = 0
	mousey = 0
	
	lastClickPos = []
	curClickPos = []
	
	while True:
		mouseClicked = False	
		mousex, mousey = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.type == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				mouseClicked = True
		
		boxRow, boxCol = getBoxAtPixel(mousex, mousey)
		if boxRow != None and boxCol != None:
			k = COLUMNSNUM * boxRow + boxCol
			left, top = leftTopCoordsOfBox(boxCol, boxRow)
			
			if mouseClicked:
				if currentData[k][0] == 9:
					currentData[k] = originalData[k]
					clearBoxSelect()
				elif currentData[k][1] == BKCOLOR:
					continue
				else:
					drawBoard(currentData)
					clearBoxSelect()

					bQuarantineFlag = (currentData[k][0] > 9 and currentData[k][0] < 14) or currentData[k][0] == 0
					drawBoxSelect(left, top, bQuarantineFlag)
					
					if not clickFlag:
						clickFlag = True
						lastClickPos.append(boxRow)
						lastClickPos.append(boxCol)
					else:
						clickFlag = False
						curClickPos.append(boxRow)
						curClickPos.append(boxCol)
						currentData = policyDecision(currentData, lastClickPos, curClickPos)
						lastClickPos = []
						curClickPos = []	
			else:
				#pygame.draw.rect(DISPLAYSURF, PIECECOLORS[currentData[k][1] + 3], (left, top, BOXSIZE, BOXSIZE))
				pygame.display.update()
				continue

		drawBoard(currentData)
		pygame.display.update()
		FPSCLOCK.tick(FPS)

if __name__ == "__main__":
	main()
	
