from config import *
from filter import *
import time


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        insert_tweet_to_db(status)

    def on_error(self, status_code):
        if status_code == 420:
            return False


def run_stream(runtime=1800):
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=filter_list, languages=["en"], is_async=True)
    time.sleep(runtime)
    stream.disconnect()
