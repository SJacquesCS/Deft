from source.DatasetParser import Parser

dataset = "../datasets/airlines_dataset.csv"
parsed_dataset = "../parsed_datasets/parsed_airlines_dataset.csv"
dictionary = "../dictionaries/airlines_dictionary.csv"
charset = "../charsets/airlines_charset.txt"
wordset = "../wordsets/airlines_wordset.txt"
alphabet = "../alphabets/airlines_alphabet.txt"

parser = Parser()
parser.parsefile(dataset, parsed_dataset, alphabet)
parser.createdict(parsed_dataset, charset, wordset, dictionary)
parser.closefiles()
