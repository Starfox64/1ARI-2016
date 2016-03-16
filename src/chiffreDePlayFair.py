from src.chiffreDuLivre import clearText


def parseText(text):
	text = clearText(text, 'Y')
	text = text.replace('W', 'V')
	size = len(text)

	for i in range(size):
		if i < size - 1 and text[i] == text[i + 1]:
			if text[i] != 'X':
				text = text[0 : i + 1] + 'X' + text[i + 1 : size]
			else:
				text = text[0 : i + 1] + 'L' + text[i + 1 : size]

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
