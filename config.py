import json
from textblob import TextBlob
import pymongo
import tweepy

db_client = pymongo.MongoClient(
    "mongodb://2314838k:37740025@localhost:27017/2314838kdb"
)
db_twitter = db_client["2314838kdb"]
new_tweet = db_twitter["new_tweet"]
quote_tweet = db_twitter["quote_tweet"]
retweet = db_twitter["retweet"]
hashtag = db_twitter["hashtag"]
# for collection in db_twitter.list_collection_names():
#     print(db_twitter[collection].drop())
"""
LOAD API KEYS IN A JSON FILE.
-----
api.json file needed containing API keys for twitter.
"""

with open("api.json", "r") as f:
    text = json.load(f)
auth = tweepy.OAuthHandler(text["TWITTER_APP_KEY"], text["TWITTER_APP_SECRET"])
auth.set_access_token(text["TWITTER_KEY"], text["TWITTER_SECRET"])
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def insert_tweet_to_db(status):
    name = status.user.screen_name
    description = status.user.description
    loc = status.user.location
    tweet_text = status.text
    coords = status.coordinates
    if coords is not None:  # convert coord to string
        coords = json.dumps(coords)
    user_created = status.user.created_at
    followers = status.user.followers_count
    id_string = status.id_str
    tweet_created = status.created_at
    hashtags = status.entities["hashtags"]
    user_mentions = status.entities["user_mentions"]
    retweets = status.retweet_count
    symbols = status.entities["symbols"]
    blob = TextBlob(tweet_text)
    sent = blob.sentiment
    polarity = sent.polarity
    subjectivity = sent.subjectivity
    tweet_json = {
        "description": description,
        "hashtags": hashtags,
        "user_mentions": user_mentions,
        "symbols": symbols,
        "name": name,
        "location": loc,
        "text": tweet_text,
        "coordinates": coords,
        "user_created": user_created,
        "followers": followers,
        "_id": id_string,
        "tweet_created": tweet_created,
        "retweets": retweets,
        "sentiment_polarity": polarity,
        "subjectivity": subjectivity,
    }

    if hasattr(status, "retweeted_status)"):
        tweet_json["retweet_user"] = status.retweeted_status.user.screen_name
        retweet.insert_one(tweet_json)
    elif status.is_quote_status:
        quote_tweet.insert_one(tweet_json)
    else:
        new_tweet.insert_one(tweet_json)
