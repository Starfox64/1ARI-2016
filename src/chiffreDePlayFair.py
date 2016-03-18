import os
import pygame
import unicodedata
from pygame.locals import *

pygame.init()

FRAME_SIZE = (750, 560)
FRAME_PADDING = (10, 10)
mainFrame = pygame.display.set_mode(FRAME_SIZE)
pygame.display.set_caption('Play Fair Cipher')

SQUARE_SIZE = 100
SQUARE_MARGIN = 10

SQUARE_FONT = pygame.font.Font(None, 65)
TEXT_FONT = pygame.font.Font(None, 35)


def clearText(text):
	text = text.replace(' ', '')
	text = text.upper()

	# Removes accents from all characters.
	text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

	output = ''
	for char in text:
		if 65 <= ord(char) <= 90:
			output += char

	return output


def parseText(text):
	text = clearText(text)
	text = text.replace('W', 'V')
	breakOut = False

	# This loop is to restart the for loop when the string is changed
	while True:
		size = len(text)
		for i in range(size):
			if i == size - 1:
					breakOut = True

			if i < size - 1 and text[i] == text[i + 1] and i % 2 == 0:
				if text[i] != 'X':
					text = text[0:i + 1] + 'X' + text[i + 1:size]
				else:
					text = text[0:i + 1] + 'L' + text[i + 1:size]

				break

		if breakOut:
			break

	size = len(text)
	if size % 2 == 1:
		text += 'X' if text[size - 1] != 'X' else 'L'
	return text


def createKey(key):
	l = list()
	for i in range(5):
		internL = list()
		for j in range(5):
			internL.append(key[i * 5 + j])
		l.append(internL.copy())
	return l


def getIndex(key, char):
	for i in range(5):
		for j in range(5):
			if key[i][j] == char:
				return i, j


def encryptPos(pos1, pos2):
	if pos1[0] == pos2[0]:
		encryptedPos1 = ((pos1[0] + 1) % 5, pos1[1])
		encryptedPos2 = ((pos2[0] + 1) % 5, pos2[1])
	elif pos1[1] == pos2[1]:
		encryptedPos1 = (pos1[0], (pos1[1] + 1) % 5)
		encryptedPos2 = (pos2[0], (pos2[1] + 1) % 5)
	else:
		encryptedPos1 = (pos1[0], pos2[1])
		encryptedPos2 = (pos2[0], pos1[1])
	return encryptedPos1, encryptedPos2


def decryptPos(pos1, pos2):
	if pos1[0] == pos2[0]:
		decryptedPos1 = ((pos1[0] - 1) % 5, pos1[1])
		decryptedPos2 = ((pos2[0] - 1) % 5, pos2[1])
	elif pos1[1] == pos2[1]:
		decryptedPos1 = (pos1[0], (pos1[1] - 1) % 5)
		decryptedPos2 = (pos2[0], (pos2[1] - 1) % 5)
	else:
		decryptedPos1 = (pos1[0], pos2[1])
		decryptedPos2 = (pos2[0], pos1[1])
	return decryptedPos1, decryptedPos2


def encryptBigram(key, bigram):
	pos = encryptPos(bigram[0], bigram[1])
	return key[pos[0][0]][pos[0][1]], key[pos[1][0]][pos[1][1]]


def decryptBigram(key, bigram):
	pos = decryptPos(bigram[0], bigram[1])
	return key[pos[0][0]][pos[0][1]], key[pos[1][0]][pos[1][1]]


def encryptText(text, key): #KEY IS A 2D LIST, TEXT IS A STRING
	encryptedText = ''
	for i in range(0, len(text), 2):
		bigram = encryptBigram(key, (getIndex(key, text[i]), getIndex(key, text[i + 1])))
		encryptedText += bigram[0] + bigram[1]
	return encryptedText


def decryptText(text, key): #KEY IS A 2D LIST, TEXT IS A STRING
	decryptedText = ''
	for i in range(0, len(text), 2):
		bigram = decryptBigram(key, (getIndex(key, text[i]), getIndex(key, text[i + 1])))
		decryptedText += bigram[0] + bigram[1]
	return decryptedText


def stringToList(text):
	key = [[None for i in range(5)] for i in range(5)]
	for i in range(len(text)):
		char = text[i]
		key[i // 5][i % 5] = char

	return key


def init():
	global clickPos, charState, state, grid, useFile
	clickPos = list()
	charState = 65
	state = 0
	grid = [[None for i in range(5)] for i in range(5)]
	useFile = False


def parseInput(message, returnType="int", callback=None):
	while True:
		res = input(message)

		if returnType == "int":
			try:
				returnVal = int(res)
			except ValueError:
				continue

			if not callback or callback(returnVal):
				return returnVal
		elif returnType == "float":
			try:
				returnVal = float(res)
			except ValueError:
				continue

			if not callback or callback(returnVal):
				return returnVal
		elif returnType == "str":
			if not callback or callback(res):
				return res


def openFile(fileName):
	currentDir = os.path.dirname(os.path.realpath(__file__))
	if os.path.isfile(os.path.join(currentDir, 'crypto_files', fileName)):
		return open(os.path.join(currentDir, 'crypto_files', fileName), 'r')


def askFileNames(decrypt, askKey):
	data = parseInput(
		'Please enter the name of the file you wish to ' + ('decrypt' if decrypt else 'encrypt') + ' (inside crypto_files): ',
		'str',
		lambda s: openFile(s)
	)

	key = None
	if askKey:
		key = parseInput(
			'Please enter the name of the file containing the key (inside crypto_files): ',
			'str',
			lambda s: openFile(s)
		)

	return data, key


def addClickPos(x, y, width, height, type, params=None):
	clickPos.append({
		'x': x,
		'y': y,
		'width': width,
		'height': height,
		'type': type,
		'params': params
	})


def draw(data):
	pygame.draw.rect(mainFrame, (0, 0, 0), (0, 0, FRAME_SIZE[0], FRAME_SIZE[1]))  # Clears frame.

	clickPos.clear()

	for y in range(len(data)):
		yPos = FRAME_PADDING[1] + y * (SQUARE_SIZE + (SQUARE_MARGIN if y > 0 else 0))
		for x in range(len(data[0])):
			xPos = FRAME_PADDING[0] + x * (SQUARE_SIZE + (SQUARE_MARGIN if x > 0 else 0))
			pygame.draw.rect(mainFrame, (255, 0, 0), (xPos, yPos, SQUARE_SIZE, SQUARE_SIZE))
			addClickPos(xPos, yPos, SQUARE_SIZE, SQUARE_SIZE, 'square', {'x': x, 'y': y})

			if data[y][x] is not None:
				textSurface = SQUARE_FONT.render(data[y][x], True, (0, 0, 0), (255, 0, 0))
				rect = textSurface.get_rect()
				rect.centerx = xPos + 50
				rect.centery = yPos + 50
				mainFrame.blit(textSurface, rect)

	if state == 0:
		textSurface = TEXT_FONT.render('Please select ' + chr(charState), True, (255, 255, 255), (0, 0, 0))
		rect = textSurface.get_rect()
		rect.topright = (FRAME_SIZE[0] - 10, 10)
		mainFrame.blit(textSurface, rect)
	elif state == 1:
		textSurface = TEXT_FONT.render('Encrypt', True, (0, 0, 0), (255, 255, 255))
		rect = textSurface.get_rect()
		rect.topright = (FRAME_SIZE[0] - 10, 10)
		mainFrame.blit(textSurface, rect)

		addClickPos(rect.x, rect.y, rect.width, rect.height, 'encrypt')

		textSurface = TEXT_FONT.render('Decrypt', True, (0, 0, 0), (255, 255, 255))
		rect = textSurface.get_rect()
		rect.topright = (FRAME_SIZE[0] - 10, 50)
		mainFrame.blit(textSurface, rect)

		addClickPos(rect.x, rect.y, rect.width, rect.height, 'decrypt')
	else:
		textSurface = TEXT_FONT.render('Look at the console.', True, (255, 255, 255), (0, 0, 0))
		rect = textSurface.get_rect()
		rect.topright = (FRAME_SIZE[0] - 10, 10)
		mainFrame.blit(textSurface, rect)

	textSurface = TEXT_FONT.render('Use Key File', True, (0, 0, 0), (255, 255, 255))
	rect = textSurface.get_rect()
	rect.bottomright = (FRAME_SIZE[0] - 10, FRAME_SIZE[1] - 10)
	mainFrame.blit(textSurface, rect)

	addClickPos(rect.x, rect.y, rect.width, rect.height, 'file')


init()
quitGui = False
while not quitGui:
	draw(grid)

	for event in pygame.event.get():
		if event.type == QUIT:
			quitGui = True
			break

		if event.type == MOUSEBUTTONUP:
			for click in clickPos:
				if (
					click['x'] <= event.pos[0] <= (click['x'] + click['width']) and
					click['y'] <= event.pos[1] <= (click['y'] + click['height'])
				):
					if click['type'] == 'square' and state == 0:
						if grid[click['params']['y']][click['params']['x']] is None:
							grid[click['params']['y']][click['params']['x']] = chr(charState)
							charState += 1 if charState != 86 else 2
							if charState > 90:
								state = 1

					if click['type'] == 'encrypt':
						state = 2
						draw(grid)
						quitGui = True

					if click['type'] == 'decrypt':
						state = 3
						draw(grid)
						quitGui = True

					if click['type'] == 'file':
						useFile = True
						state = 1

	pygame.display.update()

	if state > 1:
		pygame.time.wait(2000)

pygame.quit()

if state == 2:
	dataFileName, keyFileName = askFileNames(False, useFile)

	dataFile = openFile(dataFileName)
	key = stringToList(clearText(openFile(keyFileName).read())) if useFile else grid

	encrypted = encryptText(parseText(clearText(dataFile.read())), key)

	print('Your message has been encrypted:\n' + encrypted)
elif state == 3:
	dataFileName, keyFileName = askFileNames(True, useFile)

	dataFile = openFile(dataFileName)
	key = stringToList(clearText(openFile(keyFileName).read())) if useFile else grid

	decrypted = decryptText(clearText(dataFile.read()), key)

	print('Your message has been decrypted:\n' + decrypted)
