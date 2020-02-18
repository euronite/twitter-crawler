import json

import pymongo
import tweepy

db_client = pymongo.MongoClient("mongodb://localhost:27017/")
db_twitter = db_client["twitter"]
new_tweet = db_twitter["new_tweet"]
retweet = db_twitter["retweet"]
hashtag = db_twitter["hashtag"]

with open("api.json", "r") as f:
    text = json.load(f)
auth = tweepy.OAuthHandler(text["TWITTER_APP_KEY"], text["TWITTER_APP_SECRET"])
auth.set_access_token(text["TWITTER_KEY"], text["TWITTER_SECRET"])
api = tweepy.API(auth)
