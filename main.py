#!/usr/bin/env python3
import tweepy
import json
from filter import *
with open("api.json", "r") as f:
    text = json.load(f)
auth = tweepy.OAuthHandler(text["TWITTER_APP_KEY"], text["TWITTER_APP_SECRET"])
auth.set_access_token(text["TWITTER_KEY"], text["TWITTER_SECRET"])

api = tweepy.API(auth)

tweet_list = []


# class TweetObject(object):
#     def __init__(self, status):
#         self.description = status.user.description
#         self.loc = status.user.location
#         self.text = status.text
#         self.coords = status.coordinates
#         self.name = status.user.screen_name
#         self.user_created = status.user.created_at
#         self.followers = status.user.followers_count
#         self.id_str = status.id_str
#         self.created = status.created_at
#         self.retweets = status.retweet_count
#         self.bg_color = status.user.profile_background_color


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        #tweet_list.append(TweetObject(status))
        #print(TweetObject(status))
        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color

    def on_error(self, status_code):
        if status_code == 420:
            return False


stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=filter_list, languages=['en'])
