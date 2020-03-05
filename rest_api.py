from config import *
from pymongo.errors import DuplicateKeyError

rest_api_error = 0


def hashtag_search(search_hashtag: str):
    """
    Searches for hashtag using twitter API and returns 100 tweets which is then added to the DB
    :param search_hashtag: hashtag to search for on twitter
    :return: None
    """
    number_of_tweets = 100
    for status in tweepy.Cursor(api.search, q="#" + search_hashtag, rpp=100).items(
        number_of_tweets
    ):
        try:
            insert_tweet_to_db(status)
        except DuplicateKeyError:
            global rest_api_error
            rest_api_error += 1


def text_search(search_string: str):
    """
    REST request for a specific text. Retrieves 100 tweets based on that.
    :param search_string: search string to look for on twitter
    :return: None
    """
    number_of_tweets = 100
    for status in tweepy.Cursor(api.search, q=search_string, rpp=100).items(
        number_of_tweets
    ):
        try:
            insert_tweet_to_db(status)
        except DuplicateKeyError:
            global rest_api_error
            rest_api_error += 1


def user_search(user_name):
    """
    This gets tweets from a specific user
    :param user_name: this is the username of a twitter user
    :return: None
    """
    tweets = api.user_timeline(screen_name=user_name, count=200, include_rts=True)
    for tweet in tweets:
        try:
            insert_tweet_to_db(tweet)
        except DuplicateKeyError:
            global rest_api_error
            rest_api_error += 1


def trending_search():
    """
    This returns the top trends from twitter in the UK
    :return: trends_list which is a list of trending topics
    """
    trends = api.trends_place(23424975)[0][
        "trends"
    ]  # The integer is the location of the UK
    trends_list = [trend["name"] for trend in trends]
    return trends_list


def start_rest_probe_trends():
    """
    This starts the rest api probe for trending keywords.  and returns the top trending words
    :return: trending_list list of trending keyboards
    """
    print("REST API getting trending tweets")
    trending_list = trending_search()[:14]  # get the top 14 trending topics
    for i in trending_list:
        print("Retrieving tweets for {}".format(i))
        try:
            if i[0] == "#":
                hashtag_search(i[1:])
            else:
                text_search(i)
        except Exception as e:
            print(e)
    return trending_list
