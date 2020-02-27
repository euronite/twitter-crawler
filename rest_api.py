from config import *


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


def text_search(search_string: str):
    number_of_tweets = 100
    for status in tweepy.Cursor(api.search, q=search_string, rpp=100).items(
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


def trending_search():
    """
    This returns the top trends from twitter
    :return: trends_list which is a list of trending topics
    """
    trends = api.trends_place(23424975)[0]["trends"]  # from the end of your code
    trends_list = [trend["name"] for trend in trends]
    return trends_list


while True:
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
