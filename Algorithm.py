import text2emotion as t2e

import Sqlite


def main(data):

    with open('negative-keywords.json', encoding="utf8") as f:
        for line in f:
            negative_list = line
    with open('positive-words.txt', encoding="utf8") as f:
        for line in f:
            positive_list = line
    for l in data:
        print(t2e.get_emotion(l['text']))
        positive = 0
        negative = 0
        text = l['text'].split()
        for word in text:
            if word in positive_list:
                positive += 1
            if word in negative_list:
                negative += 1
        Sqlite.insert_variable_into_table(l['cid'], l['votes'], positive, negative)

# def searchforemotions(s):
#     if s in emotions:
