from config import *
from textblob import TextBlob


def hashtag_search(search_hashtag: str):
    """
    Searches for hashtag using twitter API and returns 100 tweets which is then added to the DB
    :param search_hashtag:
    :return:
    """
    number_of_tweets = 100
    for status in tweepy.Cursor(api.search, q="#" + search_hashtag, rpp=100).items(
        number_of_tweets
    ):
        insert_tweet_to_db(status)


def user_search(user_name):
    """
    This gets tweets from a specific user
    :param user_name: this is the username of a twitter user
    :return:
    """
    tweets = api.user_timeline(screen_name=user_name, count=100, include_rts=True)
    for tweet in tweets:
        insert_tweet_to_db(tweet)
