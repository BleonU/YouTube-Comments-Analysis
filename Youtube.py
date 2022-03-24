import os

import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    return googleapiclient.discovery.build(
        api_service_name, api_version, developerKey='AIzaSyAxORJFV63_cYuAceJWuUCs0ZfoGlcAIeU')


def getChannelInfomation(listOfId):
    youtube = main()
    request = youtube.channels().list(
        part="statistics",
        maxResults=100,
        id=listOfId
    )

    response = request.execute()

    return response


def getCommentThreads(page, videoID):
    youtube = main()
    if page is None:
        request = youtube.commentThreads().list(
            part="id,snippet,replies",
            maxResults=100,
            order="time",
            textFormat="plainText",
            videoId=videoID
        )
    else:
        request = youtube.commentThreads().list(
            part="id,snippet,replies",
            maxResults=100,
            order="time",
            pageToken=page,
            textFormat="plainText",
            videoId=videoID
        )
    response = request.execute()

    return response


def getCommentReplies(commentID):
    youtube = main()
    request = youtube.comments().list(
        part="id,snippet",
        parentId=commentID
    )
    response = request.execute()

    return response
