import math
import re


class Dictionary:
    def __init__(self):
        self.dict = {}
        self.data_file = None
        self.dict_file = None
        self.char_file = None
        self.word_file = None

    def parsefile(self, filename, char_filename, word_filename):
        self.data_file = open(filename, "r", encoding="utf-8")

        content = str.lower(self.data_file.read())
        data = content.split()
        unique_words = set(data)
        unique_chars = set(content)

        output = "Count: " + str(len(unique_words)) + "\n\n"

        for word in unique_words:
            output += word + "\n"

        print("Wordset created")

        self.word_file = open(word_filename, 'w', encoding="UTF-8")
        self.word_file.write(output)

        output = "Count: " + str(len(unique_chars)) + "\n\n"

        for char in unique_chars:
            output += char + "\n"

        print("Charset created")

        self.char_file = open(char_filename, 'w', encoding="utf8")
        self.char_file.write(output)

        lines = content.split("\n")
        output = "Count: " + str(len(lines)) + "\n\n"

        for line in lines[1:]:
            words = line.split(",")

            for word in words:
                if word in self.dict:
                    self.dict[word] += 1
                else:
                    self.dict[word] = 1

        print("Dictionary created")
        # # For all lines in file
        # for i in range(0, len(content)):
        #     # Split line by delimiter
        #     line = content[i].split(",")
        #
        #     # For all words in line
        #     for w in line[1:]:
        #         if w in self.dict:
        #             # Increase count if already in dictionary
        #             self.dict[w] + 1
        #         else:
        #             # Add to dictionary if not
        #             self.dict[w] = 1
        #
        #     # Track progress
        #     if i % math.floor((len(content) - 1) / 100) is 0:
        #         percent += 1
        #         print(str(percent) + "%")
        #
        # file.close()
        #
        # # Track progress
        # print("100%")