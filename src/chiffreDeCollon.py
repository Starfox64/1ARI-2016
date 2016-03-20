import unicodedata
import os

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

	return text


def createKey(string, size):
	key = list()
	internL = list()
	for i in range(size):
		if string[i] not in internL:
			internL.append(string[i])
	for i in range(0, 26):
		if chr(i + 65) != 'W' and chr(i + 65) not in internL:
			internL.append(chr(i + 65))
	for i in range(5):
		key.append(internL[i * 5 : i * 5 + 5])

	return key


def listToString(l):
	string = ""
	for i in range(len(l[0])):
		string += l[0][i] + l[1][i]
	return string


def arrangeCryptedText(string, size, integer):
	text = list()
	l = list()
	boolean = size % integer != 0
	for i in range(size // integer + (1 if boolean else 0) ):
		word = ""
		for j in range(integer):
			if i * 7 + j + 1 > size: break
			word += string[i * integer + j]
		l.append(word)

	subText1 = list()
	subText2 = list()
	for i in range(0, len(l), 2):
		subText1.append(l[i])
		subText2.append(l[i + 1])
	text.append(subText1.copy())
	text.append(subText2.copy())
	return text


def encryptLetter(letter, key):
	for i in range(5):
		for j in range(5):
			if letter == key[i][j]:
				return key[i][0], key[4][j]


def decryptBigram(bigram, key):
	gotI = 0
	gotJ = 0
	for j in range(5):
		if bigram[1] == key[4][j]:
			gotJ = j
			break
	for i in range(5):
		if bigram[0] == key[i][0]:
			gotI = i
			break
	return key[gotI][gotJ]


def encryptText(text, size, key, integer):
	encryptedText = list()
	eList1 = list()
	eList2 = list()
	for i in range(size // 7):
		encryptedWord1 = ""
		encryptedWord2 = ""
		for j in range(integer):
			bigram = encryptLetter(text[i * integer + j], key)
			encryptedWord1 += bigram[0]
			encryptedWord2 += bigram[1]
		eList1.append(encryptedWord1)
		eList2.append(encryptedWord2)
	encryptedText.append(eList1)
	encryptedText.append(eList2)
	return encryptedText


def decryptText(text, key):
	clearedText = ""
	for i in range(0, len(text[0])):
		for j in range(0, len(text[0][i])):
			clearedText += decryptBigram((text[0][i][j], text[1][i][j]), key)
	return clearedText


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


def askFileNames(decrypt):
	data = parseInput(
		'Please enter the name of the file you wish to ' + ('decrypt' if decrypt else 'encrypt') + ' (inside crypto_files): ',
		'str',
		lambda s: openFile(s)
	)

	key = parseInput(
		'Please enter the name of the file containing the key (inside crypto_files): ',
		'str',
		lambda s: openFile(s)
	)

	return data, key


mode = parseInput('Do you wish to:\n1) Encrypt\n2) Decrypt\n', 'int', lambda n: 0 < n <= 2)

wordLength = parseInput(
	'Enter the word length: ',
	'int',
	lambda n: n > 0
)

if mode == 1:
	dataFileName, keyFileName = askFileNames(False)

	dataFile = openFile(dataFileName)
	keyFile = openFile(keyFileName)

	key = parseText(keyFile.read())
	key = createKey(key, len(key))

	data = parseText(dataFile.read())

	encrypted = encryptText(data, len(data), key, wordLength)
	print('Your message has been encrypted:\n' + listToString(encrypted))
else:
	dataFileName, keyFileName = askFileNames(True)

	dataFile = openFile(dataFileName)
	keyFile = openFile(keyFileName)

	key = parseText(keyFile.read())
	key = createKey(key, len(key))

	data = parseText(dataFile.read())
	data = arrangeCryptedText(data, len(data), wordLength)

	decrypted = decryptText(data, key)
	print('Your message has been decrypted:\n' + decrypted)
