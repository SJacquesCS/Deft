import operator
import re


class Parser:
    def __init__(self):
        self.dict = {}
        self.data_file = None
        self.alphabet_file = None
        self.dict_file = None
        self.char_file = None
        self.word_file = None

    def parsefile(self, data_filename, char_filename, word_filename, parsed_filename, alphabet_filename):
        self.data_file = open(data_filename, "r", encoding="utf-8")
        self.alphabet_file = open(alphabet_filename, "r", encoding="utf-8")

        content = self.data_file.read()
        lines = content.split("\n")
        alphabet = self.alphabet_file.read().split(",")
        data = content.split()
        unique_words = set(data)
        unique_chars = set(content)

        output = "Count: " + str(len(unique_words)) + "\n\n"

        for word in unique_words:
            output += word + "\n"

        self.word_file = open(word_filename, 'w', encoding="utf-8")
        self.word_file.write(output)
        self.word_file.close()

        print("Wordset created")

        output = "Count: " + str(len(unique_chars)) + "\n\n"

        for char in unique_chars:
            output += char + "\n"

        self.char_file = open(char_filename, 'w', encoding="utf-8")
        self.char_file.write(output)
        self.char_file.close()

        print("Charset created")

        output = ""
        sentiments = ""

        print(len(lines))

        for line in lines:
            try:
                sentiment, message = line.split(",\"")

                sentiments += sentiment + "\n"

                sentiment = str.lower(sentiment)

                # If line is not starting by a sentiment, skip it
                if sentiment != "positif" \
                        and sentiment != "negatif" \
                        and sentiment != "neutre"\
                        and sentiment != "mixposneg"\
                        and sentiment != "inconnu":
                    continue

                # Remove URLs
                message = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', message, flags=re.MULTILINE)

                words = message.split()
                new_message = ""

                for word in words:
                    new_word = ""

                    # Change word to lower case
                    word = str.lower(str(word))

                    # Remove special characters
                    for char in word:
                        if char in alphabet:
                            new_word += char

                    # Remove white spaces
                    new_word.strip()

                    # Remove character repetitions
                    new_word = re.sub(r'([a-z])\1+', r'\1', new_word)

                    new_message += new_word + ","

                output += new_message[:-1] + "\n"
            except ValueError:
                pass

        parsed_file = open(parsed_filename, 'w', encoding="utf8")
        parsed_file.write(output)
        parsed_file.close()

        sentiment_file = open("sentiments.csv", "w", encoding="utf-8")
        sentiment_file.write(sentiments)
        sentiment_file.close()

        print("File parsed")

    def createdict(self, parsed_filename, dict_filename):
        parsed_file = open(parsed_filename, "r", encoding="utf-8")
        content = str.lower(parsed_file.read())

        lines = content.split("\n")
        output = "count," + str(len(lines)) + "\n\n"

        for line in lines[1:]:
            words = line.split(",")

            for word in words[1:]:
                if word in self.dict:
                    self.dict[word] += 1
                else:
                    self.dict[word] = 1

        self.dict = sorted(self.dict.items(), key=operator.itemgetter(1), reverse=True)

        for word, count in self.dict:
            output += word + "," + str(count) + "\n"

        self.dict_file = open(dict_filename, "w", encoding="utf-8")
        self.dict_file.write(output)

        print("Dictionary created")

    def closefiles(self):
        self.data_file.close()
        self.alphabet_file.close()
        self.dict_file.close()
        self.char_file.close()
        self.word_file.close()
