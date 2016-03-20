import unicodedata

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



cle = "service académique"
cle = parseText(clearText(cle))
cle = createKey(cle, len(cle))
chiffre = "JSJPS JCPTY TTYXS SPJJU UPTTP ZPTJS SJSSJ XZTPT YZSSS PJSCZ PTTPT YSSJU SSSTP ZPYZT JSJSU CSYPP TXTZS SPJSC JPTTP TPZCP SSJCS YPXTY XP"
chiffre = parseText(chiffre)
n = 7
chiffre = arrangeCryptedText(chiffre, len(chiffre), n)

print(decryptText(chiffre, cle))

test = "La petite bite à Valentin"
test = parseText(test)
test = encryptText(test, len(test), cle, 7)

print(decryptText(test, cle))