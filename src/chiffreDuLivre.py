from random import randint


def parseClearText(clearText, size):
	parsedText= ""

	for i in range(size):
		if clearText[i] == ' ':
			print()
	return parsedText


def createDict(keyText, size):
	dico = dict()
	fakeOccurence = size
	for i in range(65, 91):
		key = chr(i)
		l = list()
		isInText = False

		for j in range(size):
			if keyText[j] == key:
				isInText = True
				l.append(j)

		if isInText is False:
			l.append(fakeOccurence)
		dico[key] = l.copy()
		fakeOccurence += 1
	return dico


def encryptLetter(letter, key):
	x = randint(0, len(key[letter]))
	return key[letter][x]


def encryptText(text, size, key):
	l = list()
	for i in range(size):
		l.append(encryptLetter(text[i], key))
	return l


def decryptLetter(index, key):
	for i in range(65, 91):
		if index in key[chr(i)]:
			return chr(i)
		return 0


def decryptText(cryptedText, size, key):
	clearText = list()
	for i in range(size):
		clearText.append(decryptLetter(cryptedText[i], key))
	return clearText
