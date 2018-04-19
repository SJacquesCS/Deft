import operator
import pickle
import random
import re

from nltk import tokenize
from nltk import classify
from nltk import ngrams
from sklearn import svm


class Parser:
    @staticmethod
    def generate_wordset(data_filename, word_filename):
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

    @staticmethod
    def generate_charset(data_filename, char_filename):
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
        alphabet_file = open(alphabet_filename, "r", encoding="utf-8")
        alphabet = alphabet_file.read().split(",")
        alphabet_file.close()
        stopwords_file = open(stopwords_filename, "r", encoding="utf-8")
        stopwords = stopwords_file.read().split("\n")
        stopwords_file.close()

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
                output += sentiment + "," + self.clean_message(message, alphabet, stopwords) + "\n"
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

    @staticmethod
    def generate_dict(parsed_filename, dict_filename, is_transport):
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
        updated_dict_file = open(updated_dict_filename, 'r', encoding="utf-8")
        dict_data = updated_dict_file.read().split("\n")
        updated_dict_file.close()

        # Store allowed words in a list
        all_words = []
        for word in dict_data:
            all_words.append(word.split(",")[0])

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

            # Remove unwated words and add them to the output
            output += words[0] + "," + self.remove_unwated_words(words[1:], all_words) + "\n"

        # Output to parsed file
        final_parse_file = open(final_parse_filename, 'w', encoding='utf-8')
        final_parse_file.write(output[:-1])
        final_parse_file.close()

        # Print completion message
        if is_transport:
            print("Transport Second Parse Generated")
        else:
            print("Sentiment Second Parse Generated")

    def learn(self, parsed_filename, dict_filename, classifier_filename, classifier, type):
        # Load required files and split content
        data_file = open(parsed_filename, 'r', encoding='utf-8')
        data_lines = data_file.read().split("\n")
        data_file.close()
        dict_file = open(dict_filename, 'r', encoding='utf-8')
        dict_data = dict_file.read().split("\n")
        dict_file.close()

        # Prepare variables
        featuresets = []
        data = []
        sentiments = []

        for line in data_lines:
            data.append(line.split(","))

        # Add words to a set
        words = set()
        for line in dict_data:
            words.add(line.split(",")[0])

        print("Generating Featuresets")

        for datum in data:
            if classifier == "svm":
                sentiments.append(datum[0])
                featuresets.append(self.generate_features_binary(datum[1:], words))
            else:
                featuresets.append((self.generate_features_bool(datum[1:], words), datum[0]))

        print("Featuresets Generated")

        data_size = len(data)
        train_size = int(data_size * 0.8)

        training_set = featuresets[0:train_size]
        testing_set = featuresets[train_size:data_size]
        featuresets.clear()

        if str.lower(classifier) == "nb":
            print("Training Naive Bayes Classifier with Training Set of Size " + str(len(training_set)))
            clf = classify.NaiveBayesClassifier.train(training_set)
            print("Naive Bayes Classifier Trained")
        elif str.lower(classifier) == "dt":
            print("Training Decision Tree Classifier with Training Set of Size " + str(len(training_set)))
            clf = classify.DecisionTreeClassifier.train(training_set)
            print("Decision Tree Classifier Trained")
        elif str.lower(classifier) == "svm":
            print("Training Support Vector Classifier with Training Set of Size " + str(len(training_set)))
            clf = svm.SVC(C=1000, gamma=0.0001)
            clf.fit(training_set, sentiments[0:train_size])
            print("Support Vector Classifier Trained")

        training_set.clear()

        self.generate_matrix(data_filename=parsed_filename,
                             clf=clf,
                             classifier="svm",
                             featuresets=testing_set,
                             type="trsp",
                             all_words=words)

        classifier_file = open(classifier_filename, 'wb')

        pickle.dump(clf, classifier_file)

        classifier_file.close()

    @staticmethod
    def clean_message(message, alphabet, stopwords):
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
            word = re.sub(r'([a-z])\1{2}', r'\1', word)

            # Remove unwanted words
            if word not in stopwords:
                new_message += word + ","

        return new_message[:-1]

    @staticmethod
    def remove_unwated_words(message, all_words):
        new_message = ""

        for word in message:
            # Check if word is in updated dictionary
            if word in all_words:
                new_message += word + ","

        return new_message[:-1]

    @staticmethod
    def generate_features_bool(document, all_words):
        features = {}

        for word in all_words:
            if word in document:
                features[word] = True
            else:
                features[word] = False

        return features

    @staticmethod
    def generate_features_binary(document, all_words):
        features = []

        for word in all_words:
            if word in document:
                features.append(1)
            else:
                features.append(0)

        return features

    def classify(self, message, all_words, alphabet, stopwords, classifier, clf):
        clean_message = self.clean_message(message, alphabet, stopwords)
        ready_message = self.remove_unwated_words(clean_message.split(","), all_words)

        if clf == "nb":
            feature_set = self.generate_features_bool(ready_message.split(","), all_words)
            label = classifier.classify(feature_set)
        else:
            feature_set = self.generate_features_binary(ready_message.split(","), all_words)
            label = classifier.predict([feature_set])

        return label

    def generate_matrix(self, data_filename, featuresets, clf, classifier, all_words, type):
        data_file = open(data_filename, 'r', encoding='utf-8')
        data_lines = data_file.read().split("\n")
        data_file.close()

        sentiments = []

        for line in data_lines:
            sent = line.split(",")[0]
            sentiments.append(line.split(",")[0])

        total_ctr = len(featuresets)

        sentiments = sentiments[-total_ctr:]

        correct_ctr = 0
        percent = iterations = 0

        if type == "trsp":
            matrix = [[0, 0], [0, 0]]
        else:
            matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        for i, feature in enumerate(featuresets):
            if str.lower(classifier) == "nb":
                result = clf.classify(feature)
            else:
                result = clf.predict([feature])[0]

            if str.lower(type) == "trsp":
                if result == "UNK":
                    if sentiments[i] == "UNK":
                        correct_ctr += 1
                        matrix[0][0] += 1
                    else:
                        matrix[0][1] += 1
                else:
                    if sentiments[i] == "KNO":
                        correct_ctr += 1
                        matrix[1][1] += 1
                    else:
                        matrix[1][0] += 1
            else:
                if result == "POS":
                    if sentiments[i] == "POS":
                        correct_ctr += 1
                        matrix[0][0] += 1
                    elif sentiments[i] == "NEG":
                        matrix[0][1] += 1
                    elif sentiments[i] == "NEU":
                        matrix[0][2] += 1
                    else:
                        matrix[0][3] += 1
                elif result == "NEG":
                    if sentiments[i] == "POS":
                        matrix[1][0] += 1
                    elif sentiments[i] == "NEG":
                        correct_ctr += 1
                        matrix[1][1] += 1
                    elif sentiments[i] == "NEU":
                        matrix[1][2] += 1
                    else:
                        matrix[1][3] += 1
                elif result == "NEU":
                    if sentiments[i] == "POS":
                        matrix[2][0] += 1
                    elif sentiments[i] == "NEG":
                        matrix[2][1] += 1
                    elif sentiments[i] == "NEU":
                        correct_ctr += 1
                        matrix[2][2] += 1
                    else:
                        matrix[2][3] += 1
                else:
                    if sentiments[i] == "POS":
                        matrix[3][0] += 1
                    elif sentiments[i] == "NEG":
                        matrix[3][1] += 1
                    elif sentiments[i] == "NEU":
                        matrix[3][2] += 1
                    else:
                        correct_ctr += 1
                        matrix[3][3] += 1

        return_string = ""

        for i in range(0, len(matrix)):
            for j in range(0, len(matrix)):
                return_string += str(matrix[i][j]) + "\t"
            return_string += "\n"

        print("\n" + str(total_ctr) + ", " + str(correct_ctr) + "\n")
        print(str(correct_ctr / total_ctr) + "\n")
        print(return_string)

        test_file = open("../tests/tests_input_data.csv", 'r', encoding='utf-8')

        data = test_file.read().split("\n")

        output = ""

        alphabet_file = open("../alphabets/deft_alphabet.csv", 'r', encoding='utf-8')
        alphabet = alphabet_file.read().split(",")
        alphabet_file.close()
        stopwords_file = open("../stopwords/deft_stopwords.csv", 'r', encoding='utf-8')
        stopwords = stopwords_file.read().split("\n")
        stopwords_file.close()

        for line in data:
            iterations += 1

            if iterations % int(len(data) / 100) == 0:
                percent += 1
                print(str(percent) + "%")

            twid = line.split("\t")[0]
            message = line.split("\t")[1]

            clean_message = self.clean_message(message, alphabet, stopwords)
            final_message = self.remove_unwated_words(clean_message.split(","), all_words)

            output += str(twid) + "|"

            featureset = self.generate_features_binary(final_message, all_words)

            classified = clf.predict([featureset])

            output += classified[0] + "\n"

        result_file = open("../results/deft_results_ent_transport.csv", 'w', encoding='utf-8')
        result_file.write(output)
        result_file.close()

        return return_string

    def calculate_entropy(self, dictionary_filename, entropy_filename, parsed_filename, type):
        dictionary_file = open(dictionary_filename, 'r', encoding='utf-8')
        dictionary = dictionary_file.read().split("\n")
        dictionary_file.close()
        parsed_file = open(parsed_filename, 'r', encoding='utf-8')
        data = parsed_file.read().split("\n")
        parsed_file.close()

        messages = []
        labels = []

        for line in data:
            messages.append(line.split(",")[1:])
            labels.append(line.split(",")[0])

        all_words = []

        for line in dictionary:
            all_words.append(line.split(",")[0])

        output_dict = {}
        iterations = percent = 0

        if str.lower(type) == "trsp":
            for word in all_words:
                iterations += 1

                if iterations % int(len(all_words) / 100) == 0:
                    percent += 1
                    print(str(percent) + "%")

                trsp_ctr = 0
                not_ctr = 0
                for i, message in enumerate(messages):
                    if word in message:
                        if labels[i] == "KNO":
                            trsp_ctr += 1
                        else:
                            not_ctr += 1

                total = trsp_ctr + not_ctr
                entropy_diff = abs((trsp_ctr / total) - (not_ctr / total))

                output_dict[word] = entropy_diff

        output_dict = sorted(output_dict.items(), key=operator.itemgetter(1), reverse=True)

        output = ""

        for key, value in output_dict:
            output += key + "," + str(value) + "\n"

        print(output)

        entropy_file = open(entropy_filename, 'w', encoding='utf-8')
        entropy_file.write(output[:-1])
        entropy_file.close()

    def generate_ngrams(self, n, parsed_filename, ngrams_filename):
        parsed_file = open(parsed_filename, 'r', encoding='utf-8')
        data_lines = parsed_file.read().split("\n")
        parsed_file.close()

        output = ""
        percent = iterations = 0

        for line in data_lines:

            iterations += 1

            if iterations % int(len(data_lines) / 100) == 0:
                percent += 1
                print(str(percent) + "%")

            words = line.split(',')[1:]
            label = line.split(',')[0]
            message = ""

            for word in words:
                message += word + " "

            ngram = ngrams(list(message[:-1]), n)

            new_message = ""

            for gram in ngram:
                for char in gram:
                    new_message += str(char)
                new_message += ","

            output += label + "," + new_message[:-1] + "\n"

        ngrams_file = open(ngrams_filename, 'w', encoding='utf-8')
        ngrams_file.write(output[:-1])
        ngrams_file.close()

        print(output[:-1])
