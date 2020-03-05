from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MiniBatchKMeans
from collections import Counter


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
    """
    Produces statistics of the database
    :param all_new_tweets:
    :param all_retweets:
    :param all_quote_tweets:
    :return: mean_sentiment, mean_subjectivity, total_tweets
    """
    length_all_quote_tweets = len(all_quote_tweets)
    length_all_retweets = len(all_retweets)
    length_all_tweets = len(all_new_tweets)

    # print(db_twitter.collections.stats())
    total_tweets = length_all_quote_tweets + length_all_retweets + length_all_tweets
    print(f"Number of all tweets collected: {total_tweets}")
    print(f"Number of new tweets collected: {length_all_tweets}")
    print(f"Number of retweets collected: {length_all_retweets}")
    print(f"Number of quote tweets collected: {length_all_quote_tweets}")

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
    return mean_sentiment, mean_subjectivity, total_tweets


def cluster_text(list_of_text):
    """
    This uses k-means clustering from sklearn to cluster the text
    Based on the tutorial here: https://pythonprogramminglanguage.com/kmeans-text-clustering/
    :param list_of_text: This is a list of tweet texts
    :return: model.labels_ This is a list of integer number where each tweet is in a specific cluster.
    """
    print("Clustering text info saved the clustering.txt")
    vectorizer = TfidfVectorizer(stop_words="english")
    transform = vectorizer.fit_transform(list_of_text)

    true_k = 20
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
    with open("clustering.txt", "w+") as f:
        f.write("Top terms per cluster:\n")
    for i in range(true_k):
        with open("clustering.txt", "a") as f:
            f.write(f"Cluster {i}\n")
            f.write(f"Number of tweets in this cluster: {clusters[i]}\n")
        term_list = []
        for ind in order_centroids[i, :10]:
            with open("clustering.txt", "a") as f:
                f.write(terms[ind] + "\n")
            term_list.append(terms[ind] + "\n")
    return model.labels_


def extract_important(tweet_objects_list):
    """
    this extracts most mentioned users, symbols and hashtags and returns them as a list
    :param tweet_objects_list: list of tweet objects
    :return: most_frequent_hashtags, most_frequent_users, most_frequent_symbols
    """
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
    return most_frequent_hashtags, most_frequent_users, most_frequent_symbols
