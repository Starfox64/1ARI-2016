from random import randint
import os
#import unicodedata


def clearText(text):
	text = text.replace(' ', '')
	text = text.upper()
	output = ''
	for char in text:
		if 65 <= ord(char) <= 90:
			output += char

	#text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

	return output


def createDict(keyText):
	dico = dict()
	fakeOccurence = len(keyText)
	for i in range(65, 91):
		key = chr(i)
		l = list()
		isInText = False

		for j in range(len(keyText)):
			if keyText[j] == key:
				isInText = True
				l.append(j)

		if isInText is False:
			l.append(fakeOccurence)
		dico[key] = l.copy()
		fakeOccurence += 1
	return dico


def encryptLetter(letter, key):
	x = randint(0, len(key[letter]) - 1)
	return key[letter][x]


def encryptText(text, key):
	l = list()
	for char in text:
		l.append(encryptLetter(char, key))

	return l


def decryptLetter(index, key):
	for letter, values in key.items():
		if index in values:
			return letter

	return ''


def decryptText(cryptedText, key):
	clearedText = ''
	parsedText = parseEncryptedText(cryptedText)

	for number in parsedText:
		clearedText += decryptLetter(number, key)

	return clearedText


def parseEncryptedText(text):
	numbers = text.split(',')
	output = list()

	for number in numbers:
		try:
			output.append(int(number))
		except ValueError:
			continue

	return output


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


advanced = parseInput(
	'Do you wish to use advanced mode (include special characters) (Y/N)? ',
	'str',
	lambda s: s.upper() == 'Y' or s.upper() == 'N'
)
mode = parseInput('Do you wish to:\n1) Encrypt\n2) Decrypt\n', 'int', lambda n: n <= 2)

if mode == 1:
	dataFileName = parseInput(
		'Please enter the name of the file you wish to encrypt (inside crypto_files): ',
		'str',
		lambda s: openFile(s)
	)
	keyFileName = parseInput(
		'Please enter the name of the file containing the key (inside crypto_files): ',
		'str',
		lambda s: openFile(s)
	)

	dataFile = openFile(dataFileName)
	keyFile = openFile(keyFileName)

	encrypted = encryptText(clearText(dataFile.read()), createDict(clearText(keyFile.read())))
	print('Your message has been encrypted:\n' + ', '.join(map(str, encrypted)))
else:
	dataFileName = parseInput(
		'Please enter the name of the file you wish to decrypt (inside crypto_files): ',
		'str',
		lambda s: openFile(s)
	)
	keyFileName = parseInput(
		'Please enter the name of the file containing the key (inside crypto_files): ',
		'str',
		lambda s: openFile(s)
	)

	dataFile = openFile(dataFileName)
	keyFile = openFile(keyFileName)

	decrypted = decryptText(dataFile.read(), createDict(clearText(keyFile.read())))
	print('Your message has been decrypted:\n' + decrypted)
