from src.chiffreDePlayFair import parseText


def createKey(string, size):
	string = parseText(string, size)
	key = list()
	internL = list()
	for i in range(size):
		if string[i] not in internL:
			internL.append(string[i])
	for i in range(len(internL), 25):
		internL.append(chr(i + 65))
	for i in range(5):
		key.append(internL[i * 5 : i * 5 + 5])

	return key


def encryptLetter(letter, key):
	for i in range(5):
		for j in range(5):
			if letter == key[i][j]:
				return key[i][0], key[4][j]


def decryptBigram(bigram, key):
	gotI = 0
	gotJ = 0
	for i in range(5):
		for j in range(5):
			if bigram[0] == key[i][j]:
				gotI = i
				if gotJ != 0: break
			if bigram[1] == key[i][j]:
				gotJ = j
				if gotI != 0: break
	return key[gotI][gotJ]


def encryptText(text, size, key, integer):
	encryptedText = list()
	for i in range(size):
		encryptedWord1 = list()
		encryptedWord2 = list()
		for j in range(integer):
			bigram = encryptLetter(text[i], key)
			encryptedWord1.append(bigram[0])
			encryptedWord2.append(bigram[1])
			i += 1
		encryptedText.append(encryptedWord1)
		encryptedText.append(encryptedWord2)
	return encryptedText


def decryptText(text, size, key, integer):
	clearedText = ""
	for i in range(0, size, 2):
		for j in range(0, integer):
			clearedText += decryptBigram((text[i][j], text[i + 1][j]), key)
	return clearedText
