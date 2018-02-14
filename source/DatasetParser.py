import re
import math


class Parser:
    def parsefile(self, in_file_name, out_file_name):

        file = open(in_file_name, 'r', encoding="utf8")

        new_content = ""
        percent = 0

        with file as f:
            content = f.readlines()

        for i in range(0, len(content)):

            if i % math.floor((len(content) - 1) / 100) is 0:
                percent += 1
                print(str(percent) + "%")

            try:
                sentiment, sentence = content[i].split(",")

                if sentiment != "positive"\
                    and sentiment != "negative"\
                    and sentiment != "neutral": continue

                # Remove white spaces
                sentence.strip()

                # Remove special characters
                special_chars = re.compile("["
                                      u"\U0001F600-\U0001F64F"  # emoticons
                                      u"\U0001F300-\U0001F5FF"  # symbols and pictographs
                                      u"\U0001F680-\U0001F6FF"  # transport and map symbols
                                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                      "]+", flags=re.UNICODE)
                sentence = special_chars.sub(r'', sentence)
                sentence = re.sub('[!@#$%^&*()\-_+}{|":?><.;/=~,“”]', ' ', sentence)

                # Split words
                splitsentence = sentence.split()
                sentence = sentiment + ","

                for word in splitsentence:
                    # Change word to lower case
                    word = str.lower(str(word))

                    # Remove all white spaces
                    word.strip()

                    # Remove words with 0 or 1 letter
                    if len(word) < 2: continue

                    # Remove stop words
                    # if word in stopwords.words("english"): continue

                    sentence += word + ","

                sentence = sentence[:-1]

                new_content += sentence + "\n"
            except ValueError:
                pass

        file.close()

        file = open(out_file_name, 'w', encoding="utf8")
        file.write(new_content)
        print("100%")
        file.close()
