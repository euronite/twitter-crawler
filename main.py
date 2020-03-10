from grouping import *
from rest_api import *
from streaming import run_stream, return_streaming_errors
from user_interaction import *
from config import sample_data

# Setting up and running streaming API
# ======================================
trending_keywords = (
    start_rest_probe_trends()
)  # This gets trends and also gets 100 tweets per trend before starting streaming API
print("Running Streaming API!")
run_stream(
    trending_keywords, 1
)  # runs stream based on top 100 most common words and trending keywords
print("Finished Streaming API!")
print("Now processing tweets")
all_new_tweets = list(new_tweet.find({}))
sample_data(all_new_tweets[:100])  # This was used to generate sample data for 100 rows
all_retweets = list(retweet.find({}))
all_quote_tweets = list(quote_tweet.find({}))

list_of_text = get_all_new_tweets_text(all_new_tweets)
retweets_mentions_dict = mentions_graph(all_retweets)
quotes_mentions_dict = mentions_graph(all_quote_tweets)
hashtags_dict, count_hashtags = hashtags_groups(all_new_tweets)
print("Number of hashtags in new tweets: {}".format(count_hashtags))
retweet_hashtags_dict, retweet_count_hashtags = hashtags_groups(all_retweets)
print("Number of hashtags in retweets tweets: {}".format(retweet_count_hashtags))
quote_hashtags_dict, quote_count_hashtags = hashtags_groups(all_quote_tweets)
print("Number of hashtags in quote tweets: {}".format(quote_count_hashtags))
# Process all new tweets
# ======================
most_frequent_hashtags, most_frequent_users, most_frequent_symbols = extract_important(
    all_new_tweets
)
mentions_dict = mentions_graph(all_new_tweets)

# print out mentions graph stats

print(
    "Biggest group of hashtags for all tweets is is:{}".format(
        ", ".join(hashtag_interaction_stats(hashtags_dict))
    )
)
print(
    "The size of cluster of hashtags is {}".format(
        len(hashtag_interaction_stats(hashtags_dict))
    )
)
user_most, number_most = user_interaction_graph_stats(mentions_dict)
print(
    "User who has mentioned the most number of users is {} and mentioned {} people for all new tweets.".format(
        user_most, number_most
    )
)
user_most, number_most = user_interaction_graph_stats(retweets_mentions_dict)
print(
    "User who has mentioned the most number of users is {} and mentioned {} people for all retweets.".format(
        user_most, number_most
    )
)
user_most, number_most = user_interaction_graph_stats(quotes_mentions_dict)
print(
    "User who has mentioned the most number of users is {} and mentioned {} people for all quote tweets.".format(
        user_most, number_most
    )
)
print(
    "Size of the all new tweets users in mentions interaction graph is {}".format(
        len(mentions_dict)
    )
)
print(
    "Size of the all retweets users in mentions interaction graph is {}".format(
        len(retweets_mentions_dict)
    )
)
print(
    "Size of the all quote tweets users in mentions interaction graph is {}".format(
        len(quotes_mentions_dict)
    )
)

ties, triads = find_ties_triad(mentions_dict)
print("New tweet ties: {}".format(ties))
print("New tweet triads: {}".format(triads))

# Process all retweets
# ====================
most_frequent_retweet_hashtags, most_frequent_retweet_users, most_frequent_retweet_symbols = extract_important(
    all_retweets
)
mentions_dict_retweets = mentions_graph(all_retweets)
ties, triads = find_ties_triad(mentions_dict_retweets)
print("Retweet ties: {}".format(ties))
print("Retweet triads: {}".format(triads))

# Process all quote tweets
# ========================
most_frequent_quote_hashtags, most_frequent_quote_users, most_frequent_quote_symbols = extract_important(
    all_quote_tweets
)
mentions_dict_quotes = mentions_graph(all_quote_tweets)
ties, triads = find_ties_triad(mentions_dict_quotes)
print("Quote ties: {}".format(ties))
print("Quote triads: {}".format(triads))

# Cluster all tweets
print("Clustering text...")
tweet_cluster_number = cluster_text(list_of_text)
clustering = {}
for num, tweet in zip(tweet_cluster_number, all_new_tweets):
    # This puts tweets into a list, in a dictionary
    if num in clustering:
        clustering[num].append(tweet)
    else:
        clustering[num] = [tweet]
average_length = sum(len(cluster_list) for cluster_list in clustering.values()) / len(
    clustering
)
print("Average cluster size: {}".format(average_length))

# Process the clusters
max_size_cluster = 0
name_max_cluster = None
min_size_cluster = 10000000
name_min_size_cluster = None
ignored = 0  # number of clusters that are too small and therefore ignored
for cluster in clustering.keys():
    cluster_list = clustering[cluster]
    cluster_size = len(cluster_list)
    if cluster_size < min_size_cluster:
        # gets the minimum cluster size
        min_size_cluster = cluster_size
        name_min_size_cluster = cluster
    if cluster_size > max_size_cluster:
        # gets maximum cluster size
        max_size_cluster = cluster_size
        name_max_cluster = cluster
    if cluster_size < 5:
        ignored += 1
        # disregard clusters of size 5 or less.
        continue
    print("Cluster number info: {}".format(cluster))
    print("Number of tweets: {}".format(cluster_size))
    cluster_mentions_dict = mentions_graph(cluster_list)
    cluster_ties, cluster_triads = find_ties_triad(cluster_mentions_dict)
    print("Cluster ties: {}".format(ties))
    print("Cluster triads: {}".format(triads))
print(
    "Minimum cluster size is cluster {} and has {} tweets".format(
        name_min_size_cluster, min_size_cluster
    )
)
print(
    "Maximum cluster size is cluster {} and has {} tweets".format(
        name_max_cluster, max_size_cluster
    )
)
print("Number of clusters ignored as they are too small is {}".format(ignored))

mean_sentiment, mean_subjectivity, total_tweets = statistics(
    all_new_tweets, all_retweets, all_quote_tweets
)

print("Number of Streaming API Duplicates found: {}".format(return_streaming_errors()))
print("Number of REST API Duplicates found: {}".format(return_rest_errors()))
