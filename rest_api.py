from config import *
from textblob import TextBlob


def hashtag_search(search_hashtag: str):
    """
    Searches for hashtag using twitter API and returns 100 tweets
    :param search_hashtag:
    :return:
    """
    number_of_tweets = 100
    for status in tweepy.Cursor(api.search, q='#' + search_hashtag, rpp=100).items(number_of_tweets):
            name = status.user.screen_name
            description = status.user.description
            loc = status.user.location
            text = status.text
            coords = status.coordinates
            if coords is not None:  # convert coord to string
                coords = json.dumps(coords)
            user_created = status.user.created_at
            followers = status.user.followers_count
            id_string = status.id_str
            tweet_created = status.created_at
            hashtags = status.entities['hashtags']
            retweets = status.retweet_count
            blob = TextBlob(text)
            sent = blob.sentiment
            polarity = sent.polarity
            subjectivity = sent.subjectivity
            tweet_json = {"description": description, "hashtags": hashtags, "name": name, "location": loc, "text": text,
                          "coordinates": coords, "user_created": user_created, "followers": followers,
                          "id": id_string, "tweet_created": tweet_created, "retweets": retweets,
                          "sentiment_polarity": polarity,
                          "subjectivity": subjectivity}
            if "RT @" in status.text:
                tweet_json['retweet_user'] = status.retweeted_status.user.screen_name
                retweet.insert_one(tweet_json)
            else:
                new_tweet.insert_one(tweet_json)


hashtag_search("Brexit")
