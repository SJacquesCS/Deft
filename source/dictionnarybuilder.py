from source.wordobject import word


class dictionnary:
    def __init__(self):
        self.dictionnary = []

    def parsefile(self, filename):
        file = open(filename, "r", encoding="UTF-8")
        content = file.readlines()
        percent = 0
        print("0%")

        for i in range(0, len(content)):
            line = content[i].split(",")

            if i % (int(len(content) / 100)) is 0:
                percent += 1
                print(str(percent) + "%")

            for w in line[1:]:
                if not self.checkduplicates(w):
                    new_word = word(w)
                    self.dictionnary.append(new_word)

        print("100%")
        file.close()

    def checkduplicates(self, word):
        for words in self.dictionnary:
            if word == words.getword():
                words.addcount()
                return True
        return False

    def sortdictionnary(self):
        self.quicksort(self.dictionnary, 0, len(self.dictionnary) - 1)

    def quicksort(self, d, first, last):
        if first < last:
            splitter = self.partition(d, first, last)
            self.quicksort(d, first, splitter - 1)
            self.quicksort(d, splitter + 1, last)

    def partition(self, d, first, last):
        pivot = d[first].getcount()

        left = first + 1
        right = last

        done = False

        while not done:
                while left <= right and d[left].getcount() <= pivot:
                    left = left + 1

                while d[right].getcount() >= pivot and right >= left:
                    right = right - 1

                if right < left:
                    done = True
                else:
                    temp = d[left]
                    d[left] = d[right]
                    d[right] = temp

        temp = d[first]
        d[first] = d[right]
        d[right] = temp

        return right

    def saveinfo(self, filename):
        file = open(filename, "w", encoding="UTF-8")

        content = "Word,Count\n"

        for words in self.dictionnary:
            content += words.getinfo() + "\n"

        file.write(content)
