from source.DeftTool import Parser

sentiment_parse_final_file = "../parsed/final_re_deft_parse_sentiment.csv"
transport_entropy_parse_final_file = "../parsed/final_re_ent_deft_parse_transport.csv"
sentiment_dictionary_final_file = "../dictionaries/updated_re_deft_dictionary_sentiment.csv"
transport_entropy_dictionary_final_file = "../entropy/deft_entropy_transport_titan.csv"
sentiment_svm_final_classifier_file = "../classifiers/deft_svm_classifier_sentiment_final.pickle"
transport_entropy_svm_final_classifier_file = "../classifiers/deft_svm_classifier_transport_entropy_final.pickle"

parser = Parser()

parser.learn(transport_entropy_parse_final_file,
             transport_entropy_dictionary_final_file,
             transport_entropy_svm_final_classifier_file,
             classifier="svm",
             type="trsp")

# parser.calculate_entropy(dictionary_filename="../dictionaries/deft_dictionary_transport.csv",
#                          entropy_filename="../entropy/deft_entropy_transport.csv",
#                          parsed_filename="../parsed/deft_parse_transport.csv",
#                          type="trsp")
#
# parser.generate_second_parse(parse_filename="../parsed/deft_parse_transport.csv",
#                              final_parse_filename="../parsed/final_re_deft_parse_transport_2.csv",
#                              is_transport=True,
#                              updated_dict_filename="../dictionaries/updated_deft_dictionary_transport.csv")

# parser.generate_dict(parsed_filename="../parsed/final_re_deft_parse_transport.csv",
#                      dict_filename="../dictionaries/updated_re_deft_dictionary_transport.csv",
#                      is_transport=True)
