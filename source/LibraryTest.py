import os

path_1 = "C:/Users/Jacques/Desktop/DEFT/CSV/deft_dataset.csv"
path_2 = "C:/Users/Jacques/Desktop/DEFT/CSV/deft_dataset_sentiment.csv"
content = ""

file_1 = open(path_1, 'r', encoding='utf-8')
file_2 = open(path_2, 'r', encoding='utf-8')

lines_1 = file_1.readlines()
lines_2 = file_2.readlines()

percent = 0

for i in range(0, len(lines_1)):
    if i % int(len(lines_1) / 100) == 0:
        percent += 1
        print(str(percent) + "%")

    message = lines_1[i].split("\t")[1]
    sentiment = lines_2[i].split("|")[1].strip()
    content += sentiment + "," + message

file_2 = open("C:/Users/Jacques/Desktop/DEFT/CSV/deft_dataset_final.csv", 'w', encoding='utf-8')

file_2.write(content)
