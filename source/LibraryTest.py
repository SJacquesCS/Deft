import pickle

nb_classifier_file = open('../classifiers/deft_nb_classifier.pickle', 'rb')
classifier = pickle.load(nb_classifier_file)
nb_classifier_file.close()
