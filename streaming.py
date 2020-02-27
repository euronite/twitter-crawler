from config import *
from filter import *


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        insert_tweet_to_db(status)

    def on_error(self, status_code):
        if status_code == 420:
            return False


# retweet['retweet'].drop()
stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=filter_list, languages=["en"])
