from config import *


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
        except Exception as e:
            print(e)


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
        except Exception as e:
            print(e)


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
        except Exception as e:
            print(e)


def trending_search():
    """
    This returns the top trends from twitter
    :return: trends_list which is a list of trending topics
    """
    trends = api.trends_place(23424975)[0]["trends"]  # from the end of your code
    trends_list = [trend["name"] for trend in trends]
    return trends_list


def start_rest_probe_trends():
    """
    This starts the rest api probe
    :return:
    """
    print("REST API getting trending tweets")
    for i in trending_search():
        print("Retrieving tweets for {}".format(i))
        try:
            if i[0] == "#":
                hashtag_search(i[1:])
            else:
                text_search(i)
        except Exception as e:
            print(e)
