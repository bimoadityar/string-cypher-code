from string import ascii_lowercase
from random import shuffle
from abc import ABC, abstractmethod
import numpy as np

class Cipher(ABC):
    @abstractmethod
    def encrypt(self, text):
        pass

    @abstractmethod
    def decrypt(self, text):
        pass

    def toLower(self, text):
        return text.lower()

    def isLowerAlpha(self, c):
        return c.isalpha()

    def toLowerString(self, text):
        lowerText = self.toLower(text)
        return "".join([c for c in lowerText if self.isLowerAlpha(c)])

    def toNumber(self, c):
        return ord(c) - ord('a')

    def toLowerAlpha(self, num):
        return chr(num % 26 + ord('a'))

    def shiftLowerAlpha(self, c, num):
        return self.toLowerAlpha(self.toNumber(c) + num)

    def addLowerAlpha(self, c, d):
        return self.shiftLowerAlpha(c, self.toNumber(d))

    def subLowerAlpha(self, c, d):
        return self.shiftLowerAlpha(c, -self.toNumber(d))

    def inv26(self, a):
        if a % 2 == 0 or a % 13 == 0:
            raise "a is not relatively prime with 26"
        return ((a % 26) ** 11) % 26

    def rat26(self, a, b):
        for d in [2, 13]:
            while b % d == 0:
                if a % d != 0:
                    raise "divisor is not relatively prime with 26"
                a /= d
                b /= d
        return (a * self.inv26(b)) % 26


# Standard Vigenere Cipher
class VigenereStandard(Cipher):
    def __init__(self, key="vigenere"):
        self.changeKey(key)

    def changeKey(self, key):
        self.key = self.toLowerString(key)
        if not self.key:
            raise "Key does not contain lowercase alphabet"

    def encrypt(self, text):
        lowerText = self.toLowerString(text)
        keyIdx = 0
        resultArray = []
        for c in lowerText:
            resultArray.append(self.addLowerAlpha(c, self.key[keyIdx]))
            keyIdx = (keyIdx + 1) % len(self.key)
        return ''.join(resultArray)

    def decrypt(self, text):
        lowerText = self.toLowerString(text)
        keyIdx = 0
        resultArray = []
        for c in lowerText:
            resultArray.append(self.subLowerAlpha(c, self.key[keyIdx]))
            keyIdx = (keyIdx + 1) % len(self.key)
        return ''.join(resultArray)


# Full Vigenere Cipher
class VigenereFull(Cipher):
    def __init__(self, key="vigenere-full", matrixName=None):
        self.changeKey(key, matrixName)

    def changeKey(self, key, matrixName):
        self.key = self.toLowerString(key)
        if not self.key:
            raise "Key does not contain lowercase alphabet"
        if matrixName is None:
            self.matrix = self.createMatrix()
        else:
            self.matrix = np.load("./matrix/"+matrixName+".npy")
        self.invMatrix = self.inverseMatrix(self.matrix)

    def encrypt(self, text):
        lowerText = self.toLowerString(text)
        keyIdx = 0
        resultArray = []
        for c in lowerText:
            keyNum = self.toNumber(self.key[keyIdx])
            resultArray.append(self.matrix[keyNum][self.toNumber(c)])
            keyIdx = (keyIdx + 1) % len(self.key)
        return ''.join(resultArray)

    def decrypt(self, text):
        lowerText = self.toLowerString(text)
        keyIdx = 0
        resultArray = []
        for c in lowerText:
            keyNum = self.toNumber(self.key[keyIdx])
            resultArray.append(self.invMatrix[keyNum][self.toNumber(c)])
            keyIdx = (keyIdx + 1) % len(self.key)
        return ''.join(resultArray)

    def createMatrix(self):
        np.random.seed(135182)
        return np.array([np.random.permutation(26) for i in range(26)])

    def inverseMatrix(self, mat):
        inv = np.zeros((26, 26), dtype=int) - 1
        for i in range(26):
            for j in range(26):
                if inv[i][mat[i][j]] != -1:
                    raise "Matrix contains duplicate entry in the same row"
                inv[i][mat[i][j]] = j
        return inv

    def saveMatrix(self, matrixName):
        np.save("./matrix/"+matrixName, self.matrix)

# AutoKey Vigenere Cipher
class VigenereAutoKey(Cipher):
    def __init__(self, key="vigenere-auto-key"):
        self.changeKey(key)

    def changeKey(self, key):
        self.key = self.toLowerString(key)
        if not self.key:
            raise "Key does not contain lowercase alphabet"

    def encrypt(self, text):
        lowerText = self.toLowerString(text)
        keyIdx = 0
        resultArray = []
        for c in lowerText:
            keyChar = text[keyIdx - len(self.key)] if keyIdx >= len(self.key) else self.key[keyIdx]
            resultArray.append(self.addLowerAlpha(c, keyChar))
            keyIdx += 1
        return ''.join(resultArray)

    def decrypt(self, text):
        lowerText = self.toLowerString(text)
        keyIdx = 0
        resultArray = []
        for c in lowerText:
            keyChar = resultArray[keyIdx - len(self.key)] if keyIdx >= len(self.key) else self.key[keyIdx]
            resultArray.append(self.subLowerAlpha(c, keyChar))
            keyIdx += 1
        return ''.join(resultArray)


# Extended Vigenere Cipher
class VigenereExtended(Cipher):
    def __init__(self, key="vigenere-extended"):
        self.changeKey(key)

    def changeKey(self, key):
        self.key = key

    def encrypt(self, text):
        codes = text.encode("ascii") if type(text) == str else text
        keyCodes = self.key.encode("ascii")
        keyIdx = 0
        resultArray = []
        for c in codes:
            resultArray.append((c + keyCodes[keyIdx]) % 256)
            keyIdx = (keyIdx + 1) % len(keyCodes)
        return bytes(resultArray)

    def decrypt(self, text):
        codes = text.encode("ascii") if type(text) == str else text
        keyCodes = self.key.encode("ascii")
        keyIdx = 0
        resultArray = []
        for c in codes:
            resultArray.append((c - keyCodes[keyIdx]) % 256)
            keyIdx = (keyIdx + 1) % len(keyCodes)
        return bytes(resultArray)


class Playfair(Cipher):
    def __init__(self, key="playfair"):
        self.changeKey(key)

    def changeKey(self, newKey):
        alreadyOccur = set()
        self.pos = {}
        self.matrix = [[None for i in range(5)] for j in range(5)]
        x = 0
        y = 0
        newKey += "abcdefghijklmnopqrstuvwxyz"
        for c in newKey:
            if c in alreadyOccur or c == 'j':
                continue
            alreadyOccur.add(c)
            self.pos[c] = (x, y)
            self.matrix[x][y] = c
            y += 1
            if y == 5:
                x += 1
                y = 0

    def encrypt(self, text):
        lowerText = self.toLowerString(text)
        resultArray = []
        idx = 0
        while idx < len(lowerText):
            a = lowerText[idx] if lowerText[idx] != 'j' else 'i'
            idx += 1
            if idx == len(lowerText):
                b = 'x'
            elif a == lowerText[idx] or (a == 'i' and lowerText[idx] == 'j'):
                b = 'x'
            else:
                b = lowerText[idx] if lowerText[idx] != 'j' else 'i'
                idx += 1
            xa, ya = self.pos[a]
            xb, yb = self.pos[b]
            if xa == xb:
                c = self.matrix[xa][(ya + 1) % 5]
                d = self.matrix[xb][(yb + 1) % 5]
            elif ya == yb:
                c = self.matrix[(xa + 1) % 5][ya]
                d = self.matrix[(xb + 1) % 5][yb]
            else:
                c = self.matrix[xa][yb]
                d = self.matrix[xb][ya]
            resultArray.append(c)
            resultArray.append(d)
        return ''.join(resultArray)

    def decrypt(self, text):
        lowerText = self.toLowerString(text)
        resultArray = []
        idx = 0
        while idx < len(lowerText):
            a = lowerText[idx]
            b = lowerText[idx + 1]
            idx += 2
            xa, ya = self.pos[a]
            xb, yb = self.pos[b]
            if xa == xb:
                c = self.matrix[xa][(ya - 1) % 5]
                d = self.matrix[xb][(yb - 1) % 5]
            elif ya == yb:
                c = self.matrix[(xa - 1) % 5][ya]
                d = self.matrix[(xb - 1) % 5][yb]
            else:
                c = self.matrix[xa][yb]
                d = self.matrix[xb][ya]
            resultArray.append(c)
            resultArray.append(d)
        return ''.join(resultArray)

class SuperEncryption(VigenereStandard):
    def __init__(self, key="super-encryption"):
        self.changeKey(key)

    def encrypt(self, text):
        substituted = super().encrypt(text)
        resultArray = []
        for i in range(4):
            for j in range(i, len(substituted), 4):
                resultArray.append(substituted[j])
        return ''.join(resultArray)
	
    def decrypt(self, text):
        lowerText = self.toLowerString(text)
        length = len(lowerText) // 4
        offset = [0, length, 2 * length, 3 * length, len(lowerText)]
        for i in range(4):
            offset[i] += min(len(lowerText) % 4, i)
        resultArray = []
        for i in range(length + 1):
            for j in range(4):
                if offset[j] + i < offset[j + 1]:
                    resultArray.append(lowerText[offset[j] + i])
        return super().decrypt(''.join(resultArray))


class Affine(Cipher):
    def __init__(self, key="7,10"):
        self.changeKey(key)

    def changeKey(self, key):
        [a, b] = [int(x) for x in key.split(',')]
        self.key = (a, b, self.inv26(a))


    def encrypt(self, text):
        lowerText = self.toLowerString(text)
        resultArray = []
        for c in lowerText:
            num = self.toNumber(c)
            resultArray.append(self.toLowerAlpha(self.key[0] * num + self.key[1]))
        return ''.join(resultArray)

    def decrypt(self, text):
        lowerText = self.toLowerString(text)
        resultArray = []
        for c in lowerText:
            num = self.toNumber(c)
            resultArray.append(self.toLowerAlpha(self.key[2] * (num - self.key[1])))
        return ''.join(resultArray)

class Hill(Cipher):
    def __init__(self, key="1,2,3,4,5,6,7,8,9"):
        self.changeKey(key)

    def changeKey(self, key):
        [a, b, c, d, e, f, g, h, i] = [int(x) for x in key.split(',')]
        A = e * i - h * f
        B = f * g - d * i
        C = d * h - e * g
        D = h * c - b * i
        E = a * i - c * g
        F = b * g - a * h
        G = b * f - e * c
        H = c * d - a * f
        I = a * e - b * d
        det = a * A + b * B + c * C
        self.matrix = np.array([[a, b, c], [d, e, f], [g, h, i]])
        invMatrix = [[A, B, C], [D, E, F], [G, H, I]]
        self.invMatrix = np.array([[self.rat26(p, det) for p in row] for row in invMatrix])

    def encrypt(self, text):
        lowerText = self.toLowerString(text)
        resultArray = []
        for i in range(0, len(lowerText), 3):
            s = lowerText[i:i+3]
            while len(s) < 3:
                s += 'x'
            v = np.array([[self.toNumber(c)] for c in s])
            w = np.matmul(self.matrix, v)
            for d in w:
                resultArray.append(self.toLowerAlpha(d[0]))
        return ''.join(resultArray)

    def decrypt(self, text):
        lowerText = self.toLowerString(text)
        resultArray = []
        for i in range(0, len(lowerText), 3):
            s = lowerText[i:i+3]
            v = np.array([[self.toNumber(c)] for c in s])
            w = np.matmul(self.invMatrix, v)
            for d in w:
                resultArray.append(self.toLowerAlpha(d[0]))
        return ''.join(resultArray)

	
# class Enigma:
