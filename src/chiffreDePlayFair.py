from src.chiffreDuLivre import clearText


def parseText(text, size):
	text = clearText(text, size)
	#FIRST FUNCTION
	for i in range(size):
		if text[i] == 'w':
			text = text[0 : i] + 'v' + text[i+1 : size]
	#SECOND FUNCTION
	for i in range(size):
		if text[i] == text[i + 1]:
			if text[i] != 'x':
				text = text[0 : i + 1] + 'x' + text[i + 1 : size]
			else:
				text = text[0 : i + 1] + 'l' + text[i + 1 : size]
	#THIRD FUNCTION
	if size % 2 == 1:
		text += "x" if text[size - 1] != 'x' else 'l'
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
		encryptedPos1 = ( (pos1[0] + 1) % 5, pos1[1] )
		encryptedPos2 = ( (pos2[0] + 1) % 5, pos2[1] )
	elif pos1[1] == pos2[1]:
		encryptedPos1 = ( pos1[0], (pos1[1] + 1) % 5 )
		encryptedPos2 = ( pos2[0], (pos2[1] + 1) % 5 )
	else :
		encryptedPos1 = ( pos1[0], pos2[1] )
		encryptedPos2 = ( pos2[0], pos1[1] )
	return encryptedPos1, encryptedPos2


def decryptPos(pos1, pos2):
	if pos1[0] == pos2[0]:
		decryptedPos1 = ( (pos1[0] - 1) % 5, pos1[1] )
		decryptedPos2 = ( (pos2[0] - 1) % 5, pos2[1] )
	elif pos1[1] == pos2[1]:
		decryptedPos1 = ( pos1[0], (pos1[1] - 1) % 5 )
		decryptedPos2 = ( pos2[0], (pos2[1] - 1) % 5 )
	else :
		decryptedPos1 = ( pos1[0], pos2[1] )
		decryptedPos2 = ( pos2[0], pos1[1] )
	return decryptedPos1, decryptedPos2


def encryptBigram(key, bigram):
	pos = encryptPos(bigram[0], bigram[1])
	return key[pos[0][0]][pos[0][1]], key[pos[1][0]][pos[1][1]]


def decryptBigram(key, bigram):
	pos = decryptPos(bigram[0], bigram[1])
	return key[pos[0][0]][pos[0][1]], key[pos[1][0]][pos[1][1]]


def encryptText(text, size, key):
	encryptedText = ""
	for i in range(0, size, 2):
		bigram = encryptBigram(key,
							   (getIndex(key, text[i]),
								getIndex(key, text[i + 1])))
		encryptedText += bigram[0] + bigram[1]
	return encryptedText


def decryptText(text, size, key):
	decryptedText = ""
	for i in range(0, size, 2):
		bigram = decryptBigram(key,
							   (getIndex(key, text[i]),
								getIndex(key, text[i + 1])))
		decryptedText += bigram[0] + bigram[1]
	return decryptedText
