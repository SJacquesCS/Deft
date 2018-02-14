from source.DictionaryBuilder import Dictionary
from nltk.corpus import stopwords

dict = Dictionary()

dict.parsefile("../datasets/airlines_dataset.csv",
               "../charsets/airlines_charset.txt",
               "../wordsets/airlines_wordset.txt")
