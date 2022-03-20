import numpy as np
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


def addReply(data):
    commentId = data['commentId']
    splitCommentId = commentId.split(".")
    if len(splitCommentId) > 1:
        sql.insert_variable_into_replies(splitCommentId[0], commentId)


def getNumberOfSubs(id):
    details = Youtube.main(id)
    if len(details) == 3:
        return "NO"
    elif details['items'][0]['statistics']['hiddenSubscriberCount']:
        return "hidden"
    else:
        return details['items'][0]['statistics']['subscriberCount']


def getSentiment(text):
    sia = SentimentIntensityAnalyzer()
    ss = sia.polarity_scores(text)
    return emotion(ss)


def updateReplies():
    numberOfReplies = dict()
    for row in sql.query("original_comment_id", None, 'Replies'):
        if row[0] in numberOfReplies:
            numberOfReplies[row[0]] = numberOfReplies.get(row[0]) + 1
        else:
            numberOfReplies[row[0]] = 1
    for key in numberOfReplies:
        sql.update('Comments', "repliesAmount = " + str(numberOfReplies.get(key)), "cid = '" + key + "'")

def updateSubCount():
    concatId = []
    i = 0
    for row in sql.query("link", "evaluation_value <> 0 ", 'Comments'):
        concatId.append(row[0])
        i += 1
        if i == 50 or row is sql.query("link", "evaluation_value <> 0 ", 'Comments')[-1]:
            i = 0
            details = Youtube.main(','.join(concatId))
            concatId = []
            for items in details['items']:
                if items['statistics']['hiddenSubscriberCount']:
                    sql.update('Comments',
                               "subCount = -1",
                               "link = '" + items['id'] + "'")
                else:
                    sql.update('Comments',
                               "subCount = " + items['statistics']['subscriberCount'],
                               "link = '" + items['id'] + "'")


def getIntLikes(stringLikes):
    if '.' in stringLikes:
        if 'M' in stringLikes:
            return int(''.join(stringLikes.replace('M', '').split('.')) + '00000')
        else:
            return int(''.join(stringLikes.replace('K', '').split('.')) + '00')
    else:
        if 'M' in stringLikes:
            return int(''.join(stringLikes.replace('M', '') + '00000'))
        else:
            return int(''.join(stringLikes.replace('K', '') + '00'))

def main(comment):
    text = ''.join([c['text'] for c in comment['contentText'].get('runs', [])])
    # print("{0} has {1} subs".format(l['author'], getNumberOfSubs(l['channel'])))
    # print("replies are :{0}".format(findReplies(l['cid'], data)))
    sia = SentimentIntensityAnalyzer()
    # print(l['text'])
    ss = sia.polarity_scores(text)
    # storeScores.append(l['cid'], [emotion(ss), splitSentence(l, sia)])
    overall = emotion(ss)
    # emotionList = splitSentence(l, sia)
    # value = 0
    # for i in emotionList:
    #     if i < 0.5:
    # subCount = 0
    # if subCount == 'hidden':
    #     subCount = -1
    # repliesCount = 0
    # if len(l['cid'].split(".")) > 1:
    #     repliesCount = findReplies(l['cid'], data)
    sentiment = 'whatever'
    stringLikes = comment.get('voteCount', {}).get('simpleText', '0')
    likes = getIntLikes(stringLikes)
    if overall[1][1] > 0 and overall[3][1] > 0:
        sentiment = 'constructive'
    elif overall[1][1] > 0:
        sentiment = 'negative'
    elif overall[3][1] > 0:
        sentiment = 'positive'
    sql.insert_variable_into_table(comment['commentId'], sentiment,
                                   likes, 0, 0, comment.get('authorText', {}).get('simpleText', ''),
                                   text, comment['authorThumbnail']['thumbnails'][-1]['url'],
                                   comment['authorEndpoint']['browseEndpoint'].get('browseId', ''),
                                   overall[0][1])
