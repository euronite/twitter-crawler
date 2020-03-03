from config import *
from filter import *
import time
from pymongo.errors import DuplicateKeyError


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            insert_tweet_to_db(status)
        except DuplicateKeyError:
            # TODO ask for help with incrementing errors
            # TODO ask lecturer what sample data
            # TODO what is tabular data
            pass

    def on_error(self, status_code):
        if status_code == 420:
            return False


def run_stream(runtime=1800):
    """
    this runs the streaming API for the number of seconds specified by runtime. Default is 1800 if not specified
    :param runtime: int Number of seconds
    :return:
    """
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=filter_list, languages=["en"], is_async=True)
    time.sleep(runtime)
    stream.disconnect()
