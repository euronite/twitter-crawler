#!/usr/bin/env python3
from textblob import TextBlob

from config import *
from filter import *


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        name = status.user.screen_name
        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        if coords is not None:  # convert coord to string
            coords = json.dumps(coords)
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_string = status.id_str
        tweet_created = status.created_at
        # retweets = status.retweet_count
        blob = TextBlob(text)
        sent = blob.sentiment
        polarity = sent.polarity
        subjectivity = sent.subjectivity
        user_col.insert_one({"description": description, "name": name, "location": loc, "text": text,
                             "coordinates": coords, "user_created": user_created, "followers": followers,
                             "id": id_string, "tweet_created": tweet_created, "sentiment_polarity": polarity,
                             "subjectivity": subjectivity})

    def on_error(self, status_code):
        if status_code == 420:
            return False


stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=filter_list, languages=['en'])
