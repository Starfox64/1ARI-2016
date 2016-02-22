from random import randint


def clearText(text, size):
	for i in range(size):
		char = text[i]
		if char == ' ':
			text = text[0 : i] + text[i + 1 : size]
		elif char == 'à' or char == 'â' or char == 'ä':
			text[i] = 'a'
		elif char == 'é' or char == 'è' or char == 'ê' or 'ë':
			text[i] = 'e'
		elif char == 'î' or char == 'ï':
			text[i] = 'i'
		elif char == 'ô' or char == 'ô' or char == 'ö':
			text[i] = 'o'
		elif char == 'ù' or char == 'û' or char == 'ü':
			text[i] = 'u'
		text.upper()
	return text


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
	clearedText = list()
	for i in range(size):
		clearedText.append(decryptLetter(cryptedText[i], key))
	return clearedText
