from source.DatasetParser import Parser
import platform


dataset_file = "../datasets/deft_dataset.csv"
wordset_file = "../wordsets/deft_wordset.csv"
charset_file = "../charsets/deft_charset.csv"
transport_parse_file = "../parsed/deft_parse_transport.csv"
sentiment_parse_file = "../parsed/deft_parse_sentiment.csv"
alphabet_file = "../alphabets/deft_alphabet.csv"
stopwords_file = "../stopwords/deft_stopwords.csv"
transport_dictionary_file = "../dictionaries/deft_dictionary_transport.csv"
sentiment_dictionary_file = "../dictionaries/deft_dictionary_sentiment.csv"
transport_updated_dictionary_file = "../dictionaries/updated_deft_dictionary_transport.csv"
sentiment_updated_dictionary_file = "../dictionaries/updated_deft_dictionary_sentiment.csv"
transport_final_parse_file = "../parsed/final_deft_parse_transport.csv"
sentiment_final_parse_file = "../parsed/final_deft_parse_sentiment.csv"
transport_nb_classifier_file = "../classifiers/deft_nb_classifier_transport.pickle"
sentiment_nb_classifier_file = "../classifiers/deft_nb_classifier_sentiment.pickle"

parser = Parser()

parser.generate_wordset(data_filename=dataset_file,
                        word_filename=wordset_file)

parser.generate_charset(data_filename=dataset_file,
                        char_filename=charset_file)

parser.generate_first_parse(data_filename=dataset_file,
                            stopwords_filename=stopwords_file,
                            parsed_filename=transport_parse_file,
                            alphabet_filename=alphabet_file,
                            is_transport=True)

parser.generate_first_parse(data_filename=dataset_file,
                            stopwords_filename=stopwords_file,
                            parsed_filename=sentiment_parse_file,
                            alphabet_filename=alphabet_file,
                            is_transport=False)

parser.generate_dictionary(parsed_filename=transport_parse_file,
                           dict_filename=transport_dictionary_file,
                           is_transport=True)

parser.generate_dictionary(parsed_filename=sentiment_parse_file,
                           dict_filename=sentiment_dictionary_file,
                           is_transport=False)

parser.generate_second_parse(parse_filename=transport_parse_file,
                             final_parse_filename=transport_final_parse_file,
                             updated_dict_filename=transport_updated_dictionary_file,
                             is_transport=True)

parser.generate_second_parse(parse_filename=sentiment_parse_file,
                             final_parse_filename=sentiment_final_parse_file,
                             updated_dict_filename=sentiment_updated_dictionary_file,
                             is_transport=False)
#
# parser.learn_naive_bayes(parsed_filename=transport_final_parse_file,
#                          dict_filename=transport_updated_dictionary_file,
#                          nb_classifier_filename=transport_nb_classifier_file)
#
# parser.learn_naive_bayes(parsed_filename=sentiment_final_parse_file,
#                          dict_filename=sentiment_updated_dictionary_file,
#                          nb_classifier_filename=sentiment_nb_classifier_file)
