import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

sentences = ["This is a bloody sentence.",
             "This is something else.",
             "I like to type random sentences.",
             "This is not a joke, I love writing stuff that is quite randomized."]

stop_words = set(stopwords.words("english"))

for sentence in sentences:
    words = word_tokenize(sentence)
    filtered_sentence = []

    for w in words:
        if w not in stop_words:
            filtered_sentence.append(w)

    print(filtered_sentence)
