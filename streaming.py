from config import *
from filter import *
import time
from pymongo.errors import DuplicateKeyError
from rest_api import user_search

streaming_api_error = (
    0
)  # This is a global variable to count the duplicate key errors in streaming and REST


def return_streaming_errors():
    """
    This returns the number of duplicate tweets collected
    :return: streaming_api_error int
    """
    return streaming_api_error


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            insert_tweet_to_db(status)
        except DuplicateKeyError:
            global streaming_api_error
            streaming_api_error += 1
        if status.user.followers_count > 100000:
            # Ideally this would be done async
            user_search(status.user.screen_name)

    def on_error(self, status_code):
        if status_code == 420:
            return False


def run_stream(additional_keywords, runtime=1800):
    """
    this runs the streaming API for the number of seconds specified by runtime. Default is 1800 if not specified
    :param runtime: int Number of seconds
    :param additional_keywords these are additional keywords to search for
    :return:
    """
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(
        track=filter_list + additional_keywords, languages=["en"], is_async=True
    )
    time.sleep(runtime)
    stream.disconnect()
