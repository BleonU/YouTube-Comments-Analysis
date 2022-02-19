import text2emotion as t2e
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import Sqlite as sql

import Youtube

nltk.download('vader_lexicon')


def splitSentence(l, sia):
    splitStorage = []
    split = l['text'].split(".")
    for sentence in split:
        ss = sia.polarity_scores(sentence)
        splitStorage.append(emotion(ss))
    return splitStorage


def emotion(ss):
    storage = []
    for k in sorted(ss):
        storage.append([k, ss[k]])
    return storage


def findReplies(id, data):
    replies = []
    for l in data:
        if l['cid'].split(".")[0] == id and len(l['cid'].split(".")) > 1:
            replies.append(l['cid'])
    return len(replies)


def getNumberOfSubs(id):
    details = Youtube.main(id)
    if len(details) == 3:
        return "NO"
    elif details['items'][0]['statistics']['hiddenSubscriberCount']:
        return "hidden"
    else:
        return details['items'][0]['statistics']['subscriberCount']


def main(data):
    sql.delete_all_data_in_table()

    for l in data:
        # print("{0} has {1} subs".format(l['author'], getNumberOfSubs(l['channel'])))
        # print("replies are :{0}".format(findReplies(l['cid'], data)))
        sia = SentimentIntensityAnalyzer()
        # print(l['text'])
        ss = sia.polarity_scores(l['text'])
        # storeScores.append(l['cid'], [emotion(ss), splitSentence(l, sia)])
        overall = emotion(ss)
        # emotionList = splitSentence(l, sia)
        # value = 0
        # for i in emotionList:
        #     if i < 0.5:
        subCount = getNumberOfSubs(l['channel'])
        # repliesCount = 0
        # if len(l['cid'].split(".")) > 1:
        #     repliesCount = findReplies(l['cid'], data)
        if overall[1][1] > 0 and overall[3][1] > 0:
            sql.insert_variable_into_table(l['cid'], 'constructive', l['votes'], subCount, findReplies(l['cid'], data))
        elif overall[1][1] > 0:
            sql.insert_variable_into_table(l['cid'], 'negative', l['votes'], subCount, findReplies(l['cid'], data))
        elif overall[3][1] > 0:
            sql.insert_variable_into_table(l['cid'], 'positive', l['votes'], subCount, findReplies(l['cid'], data))
        elif overall[2][1] > 0:
            sql.insert_variable_into_table(l['cid'], 'whatever', l['votes'], subCount, findReplies(l['cid'], data))
