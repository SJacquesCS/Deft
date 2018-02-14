from source.DictionaryBuilder import Dictionary
from source.DatasetParser import Parser

dataset = "../datasets/airlines_dataset.csv"
parsed_dataset = "../datasets_parsed/parsed_airlines_dataset.csv"
dictionnary_dataset = "../datasets_dictionnaries/parsed_airlines_dictionnary.csv"

print("\nParsing Dataset\n")

p = Parser()
p.parsefile(dataset,
            parsed_dataset)

print("\nCreating Dictionnary\n")

d = Dictionary()
d.parsefile(parsed_dataset)
d.saveinfo(dictionnary_dataset)
