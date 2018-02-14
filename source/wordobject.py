class word:
    def __init__(self, w):
        self.word = w
        self.count = 1
        self.weight = 0.5

    def getword(self):
        return self.word

    def setword(self, w):
        self.word = w

    def getcount(self):
        return self.count

    def addcount(self):
        self.count += 1

    def getweight(self):
        return self.weight

    def changeweight(self, weight):
        self.weight += weight

    def getinfo(self):
        return self.word\
               + "," + str(self.count)
