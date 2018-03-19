import random

from nltk import classify

data_file = open("../parsed_datasets/final_deft_parse.csv", 'r', encoding='utf-8')
sent_file = open("../sentiments/deft_sentiments.csv", 'r', encoding='utf-8')
dict_file = open("../dictionaries/deft_dictionary_updated.csv", 'r', encoding='utf-8')

data_lines = data_file.read().split("\n")
sentiments_lines = sent_file.read().split("\n")
all_words = []

for line in dict_file.read().split("\n"):
    all_words.append(line.split(",")[0])


def document_features(document):
    features = {}

    for word in all_words:
        if word in document:
            features['contains({})'.format(word)] = True
        else:
            features['contains({})'.format(word)] = False

    return features


data_size = 700
data = data_lines[:data_size]
sentiments = sentiments_lines[:data_size]
train_size = int(data_size * 0.8)

feature_sets = [(document_features(lines), sents) for lines in data for sents in sentiments]

random.shuffle(feature_sets)

train_set, test_set = feature_sets[:train_size], feature_sets[train_size:]

classifier = classify.NaiveBayesClassifier.train(train_set)

print(classify.accuracy(classifier, test_set))

classifier.show_most_informative_features(5)

# import random
#
# from nltk.classify import NaiveBayesClassifier
# from nltk.sentiment import SentimentAnalyzer
# from nltk.sentiment.util import *
#
# parse_file = open("../parsed_datasets/final_deft_parse.csv", 'r', encoding='utf-8')
# sentiment_file = open("../sentiments/deft_sentiments.csv", 'r', encoding='utf-8')
#
# parse_data = parse_file.read().split("\n")
# sentiment_data = sentiment_file.read().split("\n")
#
# dataset = []
# data_size = 5
#
# for i in range(0, data_size):
#     line = parse_data[i].split(",")
#     dataset.append(line)
#
# random.shuffle(dataset)
#
# train_size = int(data_size * 0.8)
#
# train_doc = dataset[:train_size]
# test_doc = dataset[train_size:]
#
# sent_analyzer = SentimentAnalyzer()
#
# all_words = sent_analyzer.all_words(dataset)
# unigram_feats = sent_analyzer.unigram_word_feats(all_words, min_freq=1)
#
# print(unigram_feats)
#
# sent_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
#
# train_set = sent_analyzer.apply_features(train_doc)
# test_set = sent_analyzer.apply_features(test_doc)
#
# print(train_doc)
# print(train_set)
#
# trainer = NaiveBayesClassifier.train
# classifier = sent_analyzer.train(trainer, train_set)
#
# for key, value in sorted(sent_analyzer.evaluate(test_set).items()):
#     print(str(key) + ", " + str(value))
