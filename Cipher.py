from string import ascii_lowercase
from random import shuffle
import numpy as np

# Standard Vigenere Cipher
class VigenereStandard:
    def __init__(self, key="vigenere"):
        self.key = key.lower()

    def changeKey(self, newKey):
        self.key = newKey.lower()

    def encrypt(self, text):
        text = "".join([c for c in text.lower() if c.isalpha()])
        text, key = self.__normalizeTextKey(text, self.key)
        text = list(map(lambda p: ord(p) % ord('a'), list(text)))
        key = list(map(lambda p: ord(p) % ord('a'), list(key)))
        cipherText = map(lambda p: chr((p[0] + p[1]) % 26 + ord('a')), zip(text, key))
        cipherText = ''.join(list(cipherText))
        return cipherText.upper()

    def decrypt(self, text):
        text = "".join([c for c in text.lower() if c.isalpha()])
        text, key = self.__normalizeTextKey(text, self.key)
        text = list(map(lambda p: ord(p) % ord('a'), list(text)))
        key = list(map(lambda p: ord(p) % ord('a'), list(key)))
        plainText = map(lambda p: chr((p[0] - p[1]) % 26 + ord('a')), zip(text, key))
        plainText = ''.join(list(plainText))
        return plainText.lower()

    def __normalizeTextKey(self, text, key):
        if (text.__len__() == key.__len__()):
            return text, key
        elif (text.__len__() > key.__len__()):
            key = (key * (text.__len__()//key.__len__())) + \
                key[0:text.__len__() % key.__len__()]
            return text, key
        else:
            key = key[0:text.__len__()]
            return text, key

# Full Vigenere Cipher
class VigenereFull(VigenereStandard):
    def __init__(self, key="vigenere", matrixName=None):
        self.key = key
        if (matrixName == None):
            self.matrix = self.createMatrix()
        else:
            self.matrix = np.load("./matrix/"+matrixName+".npy")

    def changeKey(self, newKey):
        self.key = newKey.lower()

    def encrypt(self, text):
        text = "".join([c for c in text.lower() if c.isalpha()])
        text, key = self.__normalizeTextKey(text, self.key)
        text = list(map(lambda p: ord(p) % ord('a'), list(text)))
        key = list(map(lambda p: ord(p) % ord('a'), list(key)))
        cipherText = map(lambda p: chr(
            (self.matrix[p[1]][p[0]]) % 26 + ord('a')), zip(text, key))
        cipherText = ''.join(list(cipherText))
        return cipherText.upper()

    def decrypt(self, text):
        text = "".join([c for c in text.lower() if c.isalpha()])
        text, key = self.__normalizeTextKey(text, self.key)
        text = list(map(lambda p: ord(p) % ord('a'), list(text)))
        key = list(map(lambda p: ord(p) % ord('a'), list(key)))
        plainText = map(lambda p: chr(
            (np.where(self.matrix[p[1]] == p[0])[0].item()) % 26 + ord('a')), zip(text, key))
        plainText = ''.join(list(plainText))
        return plainText.lower()

    def __normalizeTextKey(self, text, key):
        if (text.__len__() == key.__len__()):
            return text, key
        elif (text.__len__() > key.__len__()):
            key = (key * (text.__len__()//key.__len__())) + \
                key[0:text.__len__() % key.__len__()]
            return text, key
        else:  # text.length < key.length
            key = key[0:text.__len__()]
            return text, key

    def createMatrix(self):
        mat = np.arange(26)
        shuffle(mat)
        mat = np.array([np.roll(mat, i) for i in range(26)])
        return mat

    def saveMatrix(self, matrixName):
        if (self.matrix.any()):
            np.save("./matrix/"+matrixName, self.matrix)
        else:
            print("Error, matrix empty")

# class VigenereAutoKey(VigenereStandard):

# class VigenereExtended(VigenereStandard):

# class Playfair:

# class SuperEncryption:
	
# class Affine:
	
# class Hill:
	
# class Enigma:
