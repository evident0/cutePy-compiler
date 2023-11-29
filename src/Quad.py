class Quad:
    def __init__(self, op, arg1, arg2, arg3):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

    def __repr__(self):
        return f'{self.op} {self.arg1} {self.arg2} {self.arg3}'


class QuadList:
    def __init__(self):
        self.quads = []
        self.tempCounter = 0
        self.blockStart = 0
        self.blockEnd = 0

    def __repr__(self):
        string = ''
        for i in range(len(self.quads)):
            string += f'{i}: {self.quads[i]}\n'
        return string

    def genQuad(self, operator, operand1, operand2, operand3):
        self.quads.append(Quad(operator, operand1, operand2, operand3))

    def beginBlock(self):
        self.blockStart = len(self.quads)-1

    def endBlock(self):
        self.blockEnd = len(self.quads)

    def getLastBlock(self):
        return self.quads[self.blockStart:self.blockEnd]

    def nextQuad(self):
        return len(self.quads)

    def newTemp(self):
        ret = f'T%{self.tempCounter}'
        self.tempCounter += 1
        return ret

    def backPatch(self, labellist, label):
        for i in labellist:
            self.quads[i].arg3 = label

def emptyList():
    return []

def makeList(x):
    return [x]

def mergeList(list1, list2):
    return list1 + list2





