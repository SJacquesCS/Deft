import operator
import pickle

from nltk import tokenize
from nltk.sentiment.util import *


class Parser:
    def generate_wordset(self, data_filename, word_filename):
        print("Generating Wordset")

        # Load required file and split content
        data_file = open(data_filename, "r", encoding="utf-8")
        data = set(data_file.read().split())
        data_file.close()

        # Create wordset
        output = "Count: " + str(len(data)) + "\n\n"
        for word in data:
            output += word + "\n"

        # Output wordset to file
        word_file = open(word_filename, 'w', encoding="utf-8")
        word_file.write(output)
        word_file.close()

        print("Wordset Generated")

    def generate_charset(self, data_filename, char_filename):
        print("Generating Charset")

        # Load required file and split content
        data_file = open(data_filename, "r", encoding="utf-8")
        data = set(data_file.read())
        data_file.close()

        # Create charset
        output = "Count: " + str(len(data)) + "\n\n"
        for char in data:
            output += char + "\n"

        # Output charset to file
        char_file = open(char_filename, 'w', encoding="utf-8")
        char_file.write(output)
        char_file.close()

        print("Charset Generated")

    def generate_first_parse(self, data_filename, alphabet_filename, stopwords_filename, parsed_filename, is_transport):
        # print starting message
        if is_transport:
            print("Generating Transport First Parse")
        else:
            print("Generating Sentiment First Parse")

        # Load required file and split content
        data_file = open(data_filename, "r", encoding="utf-8")
        data = data_file.read().split("\n")
        data_file.close()

        # Prepare variables
        output = ""
        percent = iterations = 0
        unk_ctr = kno_ctr = neu_ctr = mix_ctr = neg_ctr = pos_ctr = 0
        random.shuffle(data)

        print("0%")

        # Create parsed file
        for line in data:
            iterations += 1

            # Update progress
            if iterations % int(len(data) / 100) == 0:
                percent += 1
                print(str(percent) + "%")

            try:
                sentiment, message = line.split(",\"")

                # Rename sentiments and increase counters
                if is_transport:
                    if sentiment != "INCONNU":
                        sentiment = "KNO"
                        kno_ctr += 1
                    else:
                        sentiment = "UNK"
                        unk_ctr += 1
                else:
                    if sentiment == "POSITIF":
                        pos_ctr += 1
                        sentiment = "POS"
                    elif sentiment == "NEGATIF":
                        neg_ctr += 1
                        sentiment = "NEG"
                    elif sentiment == "MIXPOSNEG":
                        mix_ctr += 1
                        sentiment = "MIX"
                    elif sentiment == "NEUTRE":
                        neu_ctr += 1
                        sentiment = "NEU"
                    else:
                        continue

                # Clean message and add to output with sentiment
                output += sentiment + "," + self.clean_message(message, alphabet_filename, stopwords_filename) + "\n"
            except ValueError:
                pass

        # Output to parsed file
        parsed_file = open(parsed_filename, 'w', encoding="utf8")
        parsed_file.write(output[:-1])
        parsed_file.close()

        # Print completion message
        if is_transport:
            print("Transport First Parse Generated")
            print("\tKnown: " + str(unk_ctr))
            print("\tUnknown: " + str(kno_ctr))
        else:
            print("Sentiment First Parse Generated")
            print("\tMixed: " + str(mix_ctr))
            print("\tNegative: " + str(neg_ctr))
            print("\tNeutral: " + str(neu_ctr))
            print("\tPositive: " + str(pos_ctr))

    def generate_dictionary(self, parsed_filename, dict_filename, is_transport):
        # Print starting message
        if is_transport:
            print("Generating Transport Dictionary")
        else:
            print("Generating Sentiment Dictionary")

        # Load required file and split content
        parsed_file = open(parsed_filename, "r", encoding="utf-8")
        data = str.lower(parsed_file.read()).split("\n")
        parsed_file.close()

        # Prepare variables
        dictionary = {}
        iterations = percent = 0

        print("0%")

        # Create dictionary
        for line in data:
            iterations += 1

            # Update progress
            if iterations % int(len(data) / 100) == 0:
                percent += 1
                print(str(percent) + "%")

            words = line.split(",")

            for word in words[1:]:
                # Add words to dictionary or increase count if already in there
                if word in dictionary:
                    dictionary[word] += 1
                else:
                    dictionary[word] = 1

        # Sort dictionary in order of most popular words
        dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)

        output = ""

        for word, count in dictionary:
            output += word + "," + str(count) + "\n"

        # Output to dictionary file
        dict_file = open(dict_filename, "w", encoding="utf-8")
        dict_file.write(output[:-1])
        dict_file.close()

        # Print completion message
        if is_transport:
            print("Transport Dictionary Generated")
        else:
            print("Sentiment Dictionary Generated")

    # PROBLEM HERE!!!!
    def generate_second_parse(self, parse_filename, final_parse_filename, updated_dict_filename, is_transport):
        # Print starting message
        if is_transport:
            print("Generating Transport Second Parse")
        else:
            print("Generating Sentiment Second Parse")

        # Load required files and split content
        parse_file = open(parse_filename, 'r', encoding="utf-8")
        data = parse_file.read().split("\n")
        parse_file.close()

        # Prepare variables
        output = ""
        percent = iterations = 0

        print("0%")

        # Create parsed file
        for line in data:
            iterations += 1

            # Track progress
            if iterations % int(len(data) / 100) == 0:
                percent += 1
                print(str(percent) + "%")

            words = line.split(",")

            message = ""

            for word in words[1:]:
                message += word + ","

            # Remove unwated words and add them to the output
            output += words[0] + "," + self.remove_unwated_words(message[:-1], updated_dict_filename) + "\n"

        # Output to parsed file
        final_parse_file = open(final_parse_filename, 'w', encoding='utf-8')
        final_parse_file.write(output[:-1])
        final_parse_file.close()

        # Print completion message
        if is_transport:
            print("Transport Second Parse Generated")
        else:
            print("Sentiment Second Parse Generated")

    def learn_naive_bayes(self, parsed_filename, dict_filename, nb_classifier_filename):
        # Load required files and split content
        data_file = open(parsed_filename, 'r', encoding='utf-8')
        data_lines = data_file.read().split("\n")
        data_file.close()
        dict_file = open(dict_filename, 'r', encoding='utf-8')
        dict_data = dict_file.read().split("\n")
        dict_file.close()

        # Prepare variables
        iterations = percent = 0
        featuresets = []
        data = []

        for line in data_lines:
            data.append(line.split(","))

        # Add words to a set
        words = set()
        for line in dict_data:
            words.add(line.split(",")[0])

        print("Generating Featuresets\n0%")

        for datum in data:
            iterations += 1

            # Track progress
            if iterations % int(len(data_lines) / 100) == 0:
                percent += 1
                print(str(percent) + "%")

            featuresets.append((self.document_features(datum[1:], words), datum[0]))

        print("Featuresets Generated")

        data_size = len(data_lines)
        train_size = int(data_size * 0.8)

        training_set = featuresets[0:train_size]
        testing_set = featuresets[train_size:data_size]
        featuresets.clear()

        print("Training Naive Bayes Classifier with Training Set of Size " + str(len(training_set)))

        classifier = nltk.NaiveBayesClassifier.train(training_set)
        training_set.clear()

        print("Naive Bayes Classifier Trained")

        classifier.show_most_informative_features(20)

        print("Testing Accuracy with Testing Set of size " + str(len(testing_set)))
        print("Accuracy: " + str(nltk.classify.accuracy(classifier, testing_set)))
        testing_set.clear()

        nb_classifier_file = open(nb_classifier_filename, 'wb')
        pickle.dump(classifier, nb_classifier_file)
        nb_classifier_file.close()

    @staticmethod
    def clean_message(message, alphabet_filename, stopwords_filename):
        # Load required files and split content
        alphabet_file = open(alphabet_filename, "r", encoding="utf-8")
        alphabet = alphabet_file.read().split(",")
        alphabet_file.close()
        stopwords_file = open(stopwords_filename, "r", encoding="utf-8")
        french_stopwords = stopwords_file.read().split("\n")
        stopwords_file.close()

        # Remove URLs
        message = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', message, flags=re.MULTILINE)

        # Remove unintentional skiplines
        message = re.sub(r'\[[^\]]*\]', '', message)

        # Change all characters to lower case
        message = str.lower(str(message))

        message_list = list(message)
        new_message = ""

        for char in message_list:
            # Remove unwanted characters
            if char in alphabet:
                new_message += char

        # Tokenize words
        word_list = tokenize.word_tokenize(new_message, language='french')

        new_message = ""

        for word in word_list:
            # Remove character repetitions
            word = re.sub(r'([a-z])\1+', r'\1', word)

            # Remove unwanted words
            if word not in french_stopwords:
                new_message += word + ","

        return new_message[:-1]

    @staticmethod
    def remove_unwated_words(line, dictionary_filename):
        # Open required file and split content
        updated_dict_file = open(dictionary_filename, 'r', encoding="utf-8")
        dict_data = updated_dict_file.read().split("\n")
        updated_dict_file.close()

        # Store allowed words in a list
        allowed_words = []
        for line in dict_data:
            allowed_words.append(line.split(",")[0])

        words = line.split(",")
        new_words = []

        for word in words:
            # Check if word is in updated dictionary
            if word in allowed_words:
                new_words.append(word)

        new_line = ""

        for word in new_words:
            new_line += word + ","

        return new_line[:-1]

    @staticmethod
    def document_features(document, all_words):
        features = {}

        for word in all_words:
            if word in document:
                features[word] = True
            else:
                features[word] = False

        return features
