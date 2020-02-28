import matplotlib.pyplot as plt
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MiniBatchKMeans
from collections import Counter
from config import *


def get_all_new_tweets_text(all_new_tweets):
    """
    Gets a list of tweets text from new tweets
    :return: list of all tweets text
    """
    all_tweets_text = []
    for tweet in all_new_tweets:
        all_tweets_text.append(tweet["text"])
    return all_tweets_text


def statistics(all_new_tweets, all_retweets, all_quote_tweets):
    length_all_quote_tweets = len(all_quote_tweets)
    length_all_retweets = len(all_retweets)
    length_all_tweets = len(all_new_tweets)

    # print(db_twitter.collections.stats())
    print(
        "Number of tweets collected: {}".format(
            length_all_quote_tweets + length_all_retweets + length_all_tweets
        )
    )

    # Calculates mean sentiment, where 1 is very positive, -1 is very negative
    mean_sentiment = 0.0

    for tweet in all_new_tweets:
        mean_sentiment += tweet["sentiment_polarity"]
    mean_sentiment = mean_sentiment / length_all_tweets
    print("The mean sentiment of tweets is: ", mean_sentiment)

    # Calculates mean subjectivity, where 1 is very subjective, -1 is very objective
    mean_subjectivity = 0.0

    for tweet in all_new_tweets:
        mean_subjectivity += tweet["subjectivity"]
    mean_subjectivity = mean_subjectivity / length_all_tweets
    print("The mean subjectivity of retweets is: ", mean_subjectivity)


def cluster_text(list_of_text):
    """
    This uses k-means clustering from sklearn to cluster the text
    Based on the tutorial here: https://pythonprogramminglanguage.com/kmeans-text-clustering/
    :param list_of_text: This is a list of tweet texts
    :return:
    """

    vectorizer = TfidfVectorizer(stop_words="english")
    transform = vectorizer.fit_transform(list_of_text)

    true_k = 40
    model = MiniBatchKMeans(n_clusters=true_k, init="k-means++", max_iter=100, n_init=1)
    model.fit(transform)
    clusters = {}
    for i in model.labels_:
        if not i in clusters:
            clusters[i] = 1
        else:
            clusters[i] += 1

    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    print("Top terms per cluster:")
    for i in range(true_k):
        print("Cluster {}:".format(i))
        print("Number of tweets in this cluster: {}".format(clusters[i]))
        term_list = []
        for ind in order_centroids[i, :10]:
            term_list.append(terms[ind])
        print("Keywords: {}".format(", ".join(term_list)))


def directed_graph(list_of_tweets):
    """
    This generates a directed graph of users in regards to who tweeted whom
    :param list_of_tweets: THis is a list of tweet texts to analyse
    :return:
    """
    digraph = nx.DiGraph()
    for i in list_of_tweets:
        digraph.add_edge(i["retweet_user"], i["name"])
    nx.draw_networkx(digraph)
    plt.show()


def extract_important(tweet_objects_list):
    # This section extracts important information such as most common hashtags
    hashtag_dictionary = {}
    for tweet in tweet_objects_list:
        if "hashtags" in tweet:
            for individual_hashtag in tweet["hashtags"]:
                if not individual_hashtag["text"].lower() in hashtag_dictionary:
                    hashtag_dictionary[individual_hashtag["text"].lower()] = 1
                else:
                    hashtag_dictionary[individual_hashtag["text"].lower()] += 1
    frequency = Counter(hashtag_dictionary)
    most_frequent_hashtags = frequency.most_common(50)

    user_dictionary = {}
    for tweet in tweet_objects_list:
        if "user_mentions" in tweet:
            for individual_user in tweet["user_mentions"]:
                if not individual_user["screen_name"] in user_dictionary:
                    user_dictionary[individual_user["screen_name"].lower()] = 1
                else:
                    user_dictionary[individual_user["screen_name"].lower()] += 1
    frequency = Counter(user_dictionary)
    most_frequent_users = frequency.most_common(50)
    symbol_dictionary = {}
    for tweet in tweet_objects_list:
        if "symbols" in tweet:
            for individual_symbol in tweet["symbols"]:
                if not individual_symbol["text"] in symbol_dictionary:
                    symbol_dictionary[individual_symbol["text"]] = 1
                else:
                    symbol_dictionary[individual_symbol["text"]] += 1
    frequency = Counter(symbol_dictionary)
    most_frequent_symbols = frequency.most_common(50)
    print("Most mentioned users:", most_frequent_users)
    print("Most used symbols: ", most_frequent_symbols)
    print("Most used hashtags", most_frequent_hashtags)
    return most_frequent_hashtags
