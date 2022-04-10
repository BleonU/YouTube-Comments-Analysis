import math

import numpy as np
import text2emotion as t2e
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import Sqlite as sql

import Youtube

nltk.download('vader_lexicon')


def emotion(ss):
    storage = []
    for k in sorted(ss):
        storage.append([k, ss[k]])
    return storage


def addReply(data):
    commentId = data['commentId']
    splitCommentId = commentId.split(".")
    if len(splitCommentId) > 1:
        sql.insertVariableIntoReplies(splitCommentId[0], commentId)


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
    counter = 0
    for row in sql.query("link", "evaluation_value <> 0 ", 'Comments'):
        concatId.append(row[0])
        counter += 1
        if counter == 50 or row[0] == sql.query("link", "evaluation_value <> 0 ", 'Comments')[-1][0]:
            counter = 0
            details = Youtube.getChannelInfomation(','.join(concatId))
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


# def getIntLikes(stringLikes):
#     if '.' in stringLikes:
#         if 'M' in stringLikes:
#             return int(''.join(stringLikes.replace('M', '').split('.')) + '00000')
#         else:
#             return int(''.join(stringLikes.replace('K', '').split('.')) + '00')
#     else:
#         if 'M' in stringLikes:
#             return int(''.join(stringLikes.replace('M', '') + '00000'))
#         else:
#             return int(''.join(stringLikes.replace('K', '') + '00'))


def updateSentiment():
    highestLike = sql.query('likes', "likes > -1 ORDER BY likes", 'Comments')[-1][0]
    for row in sql.query('*', None, 'Comments'):
        sia = SentimentIntensityAnalyzer()
        ss = sia.polarity_scores(row[6])
        overall = emotion(ss)
        likeAmplifier = round(row[4] / highestLike, 4)
        sentiment = 'whatever'
        if overall[0][1] != 0:
            if overall[1][1] > 0 and overall[3][1] > 0:
                if len(row[6].split('.')) > 2:
                    sentiment = 'constructive'
            elif overall[1][1] + likeAmplifier > 0.5:
                sentiment = 'negative'
            elif overall[3][1] + likeAmplifier > 0.5:
                sentiment = 'positive'
            sql.update('Comments',
                       "evaluation = '" + sentiment + "'",
                       "cid = '" + row[0] + "'")
            sql.update('Comments',
                       "evaluation_value = " + str(overall[0][1] + likeAmplifier),
                       "cid = '" + row[0] + "'")





def main(item):
    snippet = item['snippet']['topLevelComment']['snippet']
    id = item['snippet']['topLevelComment']['id']
    replies = item['snippet']['totalReplyCount']
    if snippet['authorDisplayName'] != '':
        sql.insertVariableIntoComments(id, 'whatever', snippet['likeCount'], replies, 0,
                                       snippet['authorDisplayName'], snippet['textOriginal'],
                                       snippet['authorProfileImageUrl'],
                                       snippet['authorChannelId']['value'], 0, 'yes')
    if replies > 0:
        details = Youtube.getCommentReplies(id)
        for item in details['items']:
            snippet = item['snippet']
            id = item['id']
            if snippet['authorDisplayName'] != '':
                sql.insertVariableIntoComments(id, 'whatever', snippet['likeCount'], replies, 0,
                                               snippet['authorDisplayName'], snippet['textOriginal'],
                                               snippet['authorProfileImageUrl'],
                                               snippet['authorChannelId']['value'], 0, 'no')
                sql.insertVariableIntoReplies(snippet['parentId'], id)
    # text = ''.join([c['text'] for c in comment['contentText'].get('runs', [])])
    # stringLikes = comment.get('voteCount', {}).get('simpleText', '0')
    # likes = getIntLikes(stringLikes)
    # sql.insert_variable_into_table(comment['commentId'], 'whatever',
    #                                likes, 0, 0, comment.get('authorText', {}).get('simpleText', ''),
    #                                text, comment['authorThumbnail']['thumbnails'][-1]['url'],
    #                                comment['authorEndpoint']['browseEndpoint'].get('browseId', ''), 0)
