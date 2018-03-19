import operator
import sys
import re
import nltk

from nltk import tokenize
from nltk.sentiment.util import *


class Parser:
    def __init__(self):
        self.dict = {}
        self.data_file = None
        self.stopwords_file = None
        self.alphabet_file = None
        self.dict_file = None
        self.char_file = None
        self.word_file = None
        self.updated_dict_file = None
        self.final_parse_file = None

    def generate_wordset(self, data_filename, word_filename):

        # Load required file
        self.data_file = open(data_filename, "r", encoding="utf-8")

        # Read file and split contents
        content = self.data_file.read()
        data = content.split()
        unique_words = set(data)

        # Create wordset
        output = "Count: " + str(len(unique_words)) + "\n\n"
        for word in unique_words:
            output += word + "\n"

        # Output wordset to file
        self.word_file = open(word_filename, 'w', encoding="utf-8")
        self.word_file.write(output)
        self.word_file.close()
        print("Wordset created")

    def generate_charset(self, data_filename, char_filename):

        # Load required file
        self.data_file = open(data_filename, "r", encoding="utf-8")

        # Read file and split contents
        content = self.data_file.read()
        unique_chars = set(content)

        # Create charset
        output = "Count: " + str(len(unique_chars)) + "\n\n"
        for char in unique_chars:
            output += char + "\n"

        # Output charset to file
        self.char_file = open(char_filename, 'w', encoding="utf-8")
        self.char_file.write(output)
        self.char_file.close()
        print("Charset created")

    def generate_first_parse(self, data_filename, stopwords_filename, parsed_filename, sentiments_filename, alphabet_filename):

        # Load required files to do the parsing
        self.data_file = open(data_filename, "r", encoding="utf-8")
        self.alphabet_file = open(alphabet_filename, "r", encoding="utf-8")
        self.stopwords_file = open(stopwords_filename, "r", encoding="utf-8")

        # Read the files and split contents
        content = self.data_file.read()
        lines = content.split("\n")
        alphabet = self.alphabet_file.read().split(",")
        french_stopwords = self.stopwords_file.read().split("\n")
        print(french_stopwords)

        # Prepare variables
        output = ""
        sentiments = ""
        percent = 0
        iterations = 0
        print("0%")

        # Create parsed file
        for line in lines:
            iterations += 1

            if iterations % int(len(lines) / 100) == 0:
                percent += 1
                print(str(percent) + "%")

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

                # Remove unintentional skiplines
                message = re.sub(r'\[[^\]]*\]', '', message)

                # Change all characters to lower case
                message = str.lower(str(message))

                message_list = list(message)
                new_message = ""

                for char in message_list:
                    if char in alphabet:
                        new_message += char

                word_list = tokenize.word_tokenize(new_message, language='french')

                new_message = ""

                for word in word_list:
                    # Remove character repetitions
                    word = re.sub(r'([a-z])\1+', r'\1', word)

                    if word not in french_stopwords:
                        new_message += word + ","

                output += new_message[:-1] + "\n"
            except ValueError:
                pass

        # Output to parsed file
        parsed_file = open(parsed_filename, 'w', encoding="utf8")
        parsed_file.write(output)
        parsed_file.close()

        # Sentiments to sentiments file
        sentiment_file = open(sentiments_filename, "w", encoding="utf-8")
        sentiment_file.write(sentiments)
        sentiment_file.close()
        print("File parsed")

    def first_dictionary(self, parsed_filename, dict_filename):
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

    def second_parse(self, parse_filename, final_parse_filename, updated_dict_filename):
        self.final_parse_file = open(final_parse_filename, 'w', encoding="utf-8")
        self.updated_dict_file = open(updated_dict_filename, 'r', encoding="utf-8")

        allowed_words = []

        dict_content = self.updated_dict_file.read()
        dict_lines = dict_content.split("\n")

        for line in dict_lines:
            allowed_words.append(line.split(",")[0])

        parse_file = open(parse_filename, 'r', encoding="utf-8")
        content = parse_file.read()
        parse_file.close()

        lines = content.split("\n")

        new_content = ""
        percent = 0

        print("0%")

        iterations = 0

        for line in lines:
            iterations += 1

            if iterations % int(len(lines) / 100) == 0:
                percent += 1
                print(str(percent) + "%")

            words = line.split(",")
            new_words = []

            for word in words:
                if word in allowed_words:
                    new_words.append(word)

            new_words = mark_negation(new_words)
            new_line = ""

            for word in new_words:
                new_line += word + ","

            new_content += new_line[:-1] + "\n"

        self.final_parse_file.write(new_content[:-1])

        print("Finished second parse")

    def generate_featuresrets(self, parsed_filename, dict_filename, sentiments_filename, featuresets_filename):
        data_file = open(parsed_filename, 'r', encoding='utf-8')
        dict_file = open(dict_filename, 'r', encoding='utf-8')
        sent_file = open(sentiments_filename, 'r', encoding='utf-8')

        data_lines = data_file.read().split("\n")
        data = []

        for line in data_lines:
            data.append(line.split(","))

        sent_lines = sent_file.read().split("\n")
        all_words = set()

        for line in dict_file.read().split("\n")[:2000]:
            all_words.add(line.split(",")[0])

        featuresets = []

        iterations = 0
        percent = 0

        print("0%")

        for i in range(0, len(data_lines)):
            iterations += 1

            if iterations % int(len(data_lines) / 100) == 0:
                percent += 1
                print(str(percent) + "%")

            featuresets.append((self.document_features(data[i], all_words), sent_lines[i]))

        data_size = len(data_lines)
        train_size = int(data_size * 0.8)

        random.shuffle(featuresets)
        training_set = featuresets[:train_size]
        testing_set = featuresets[train_size:data_size]

        classifier = nltk.NaiveBayesClassifier.train(training_set)

        classifier.show_most_informative_features()

        print(nltk.classify.accuracy(classifier, testing_set))

    @staticmethod
    def document_features(document, all_words):
        features = {}

        for word in all_words:
            if word in document:
                features[word] = True
            else:
                features[word] = False

        return features

    def closefiles(self):
        if self.data_file: self.data_file.close()
        if self.alphabet_file: self.alphabet_file.close()
        if self.dict_file: self.dict_file.close()
        if self.char_file: self.char_file.close()
        if self.word_file: self.word_file.close()
        if self.updated_dict_file: self.updated_dict_file.close()
        if self.final_parse_file: self.final_parse_file.close()
