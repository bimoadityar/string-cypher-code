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

# class VigenereFull(VigenereStandard):

# class VigenereAutoKey(VigenereStandard):

# class VigenereExtended(VigenereStandard):

# class Playfair:

# class SuperEncryption:
	
# class Affine:
	
# class Hill:
	
# class Enigma:
