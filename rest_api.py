from config import *


def hashtag_search(hashtag: str):
    """
    Searches for hashtag using twitter API
    :param hashtag:
    :return:
    """
    number_of_tweets = 100
    for tweet in tweepy.Cursor(api.search, q='#' + hashtag, rpp=100).items(number_of_tweets):
        