from source.DeftTool import Parser

parser = Parser()

parser.generate_first_parse(data_filename="outfile.csv", alphabet_filename="../alphabets/deft_alphabet.csv", stopwords_filename="../stopwords/deft_stopwords.csv", parsed_filename="../parsed/test_parsed.csv", is_transport=True)

# test_file = open("../tests/tests_input_data.csv", 'r', encoding='utf-8')
#
# test_data = test_file.read().split("\n")
#
# messages = []
# output = ""
#
# for line in test_data:
#     twid = line.split("\t")[0]
#     message = line.split("\t")[1]
#     print(message)
#     output += str(twid) + "," + message + "\n"
#
# out_file = open("outfile.csv", 'w', encoding='utf-8')
# out_file.write(output)
# out_file.close()



# import pickle
#
# dict_filename = "../entropy/deft_entropy_transport.csv"
# alphabet_filename = "../alphabets/deft_alphabet.csv"
# stopwords_filename = "../stopwords/deft_stopwords.csv"
# classifier_filename = "../classifiers/deft_svm_classifier_transport_re_ent.pickle"
#
# test_file = open("../tests/tests_input_data.csv", 'r', encoding='utf-8')
#
# data = test_file.read().split("\n")
#
# output = ""
#
# parser = Parser()
#
# percent = iterations = 0
#
# dictionary = open(dict_filename, 'r', encoding='utf-8')
# dict_data = dictionary.read().split("\n")
# dictionary.close()
# alphabet_file = open(alphabet_filename, 'r', encoding='utf-8')
# alphabet = alphabet_file.read().split(",")
# alphabet_file.close()
# stopwords_file = open(stopwords_filename, 'r', encoding='utf-8')
# stopwords = stopwords_file.read().split("\n")
# stopwords_file.close()
# classifier_file = open(classifier_filename, 'rb')
# classifier = pickle.load(classifier_file)
# classifier_file.close()
#
# all_words = []
#
# for line in dict_data:
#     all_words.append(line.split(",")[0])
#
# trsp = True
#
# if trsp:
#     unk_ctr = 0
#     kno_ctr = 0
# else:
#     pos_ctr = 0
#     neg_ctr = 0
#     mix_ctr = 0
#     neu_ctr = 0
#
# for line in data:
#     iterations += 1
#
#     if iterations % int(len(data) / 100) == 0:
#         percent += 1
#         print(str(percent) + "%")
#
#     twid = line.split("\t")[0]
#     message = line.split("\t")[1]
#
#     output += str(twid) + "|"
#
#     classified = parser.classify(message=message,
#                                  all_words=all_words,
#                                  alphabet=alphabet,
#                                  classifier=classifier,
#                                  clf="svm",
#                                  stopwords=stopwords)
#
#     if trsp:
#         if classified[0] == "UNK":
#             unk_ctr += 1
#         else:
#             kno_ctr += 1
#     else:
#         if classified[0] == "POS":
#             pos_ctr += 1
#         elif classified[0] == "NEG":
#             neg_ctr += 1
#         elif classified[0] == "MIX":
#             mix_ctr += 1
#         else:
#             neu_ctr += 1
#
#     output += classified[0] + "\n"
#
# result_file = open("../results/deft_results_ent_transport.csv", 'w', encoding='utf-8')
# result_file.write(output)
# result_file.close()
#
# if trsp:
#     print("kno=" + str(kno_ctr) + ", unk=" + str(unk_ctr))
# else:
#     print("pos=" + str(pos_ctr) + ", neg=" + str(neg_ctr) + ", mix=" + str(mix_ctr) + ", neu=" + str(neu_ctr))
