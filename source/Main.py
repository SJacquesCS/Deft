from source.DatasetParser import Parser
import platform

alphabet_file = "../alphabets/deft_alphabet.csv"
stopwords_file = "../stopwords/deft_stopwords.csv"
charset_file = "../charsets/deft_charset.csv"
dataset_file = "../datasets/deft_dataset.csv"
dictionary_file = "../dictionaries/deft_dictionary.csv"
updated_dictionary_file = "../dictionaries/deft_dictionary_updated.csv"
sentiments_file = "../sentiments/deft_sentiments.csv"
parsed_file = "../parsed_datasets/deft_parse.csv"
stopwords_file = "../stopwords/deft_stopwords.csv"
wordset_file = "../wordsets/deft_wordset.csv"
final_parse_file = "../parsed_datasets/final_deft_parse.csv"
featuresets_file = "../featuresets/deft_featuresets.csv"

print(platform.architecture())

parser = Parser()

# parser.generate_wordset(data_filename=dataset_file,
#                         word_filename=wordset_file)
#
# parser.generate_charset(data_filename=dataset_file,
#                         char_filename=charset_file)
#
# parser.generate_first_parse(data_filename=dataset_file,
#                             stopwords_filename=stopwords_file,
#                             sentiments_filename=sentiments_file,
#                             parsed_filename=parsed_file,
#                             alphabet_filename=alphabet_file)
#
# parser.first_dictionary(parsed_filename=parsed_file,
#                         dict_filename=dictionary_file)
#
# parser.second_parse(parse_filename=parsed_file,
#                     final_parse_filename=final_parse_file,
#                     updated_dict_filename=updated_dictionary_file)

parser.generate_featuresrets(parsed_filename=final_parse_file,
                             dict_filename=updated_dictionary_file,
                             featuresets_filename=featuresets_file,
                             sentiments_filename=sentiments_file)

parser.closefiles()
