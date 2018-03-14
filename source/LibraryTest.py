from nltk.sentiment.util import *


def get_message(message):
    return {'message': message}

parse = open("../parsed_datasets/final_deft_parse.csv", 'r', encoding="utf-8")
sentiments = open("../sentiments/deft_sentiments.csv", 'r', encoding="utf-8")

parsed_data = parse.read().split("\n")
sentiments_data = sentiments.read().split("\n")

sentences = []

for i in range(0, 100):
    sentence = ""

    for word in parsed_data[i].split(","):
        sentence += word + " "

    print(mark_negation(sentence))

    sentences.append((sentence[:-1], sentiments_data[i]))

# featuresets = [(get_message(message), sentiment) for (message, sentiment) in sentences]
# train_set, test_set = featuresets[:55093], featuresets[55093:]
#
# classifier = nltk.NaiveBayesClassifier.train(train_set)
# classifier.show_most_informative_features(5)
#
# print(nltk.classify.accuracy(classifier, test_set))
