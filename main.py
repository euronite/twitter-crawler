from grouping import *
from rest_api import *
from streaming import run_stream
from user_interaction import *

print("Running Streaming API!")
run_stream(1)
print("Finished Streaming API!")
# start_rest_probe_trends()
all_new_tweets = list(new_tweet.find({}))
all_retweets = list(retweet.find({}))
all_quote_tweets = list(quote_tweet.find({}))
list_of_text = get_all_new_tweets_text(all_new_tweets)

# for user in most_frequent_users:
#     print("Collecting tweets from {}".format(user[0]))
#     user_search(user[0])

mean_sentiment, mean_subjectivity, total_tweets = statistics(
    all_new_tweets, all_retweets, all_quote_tweets
)
retweets_mentions_dict = mentions_graph(all_retweets)
quotes_mentions_dict = mentions_graph(all_quote_tweets)
hashtags_dict = hashtags_groups(all_new_tweets)

# Process all new tweets
# ======================
most_frequent_hashtags, most_frequent_users, most_frequent_symbols = extract_important(
    all_new_tweets
)
# for user in most_frequent_users:
#     print("Collecting tweets from {}".format(user[0]))
#     user_search(user[0])

mentions_dict = mentions_graph(all_new_tweets)
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

# Process the clusters
for cluster in clustering.keys():
    cluster_list = clustering[cluster]
    cluster_size = len(cluster_list)
    if cluster_size < 5:
        # disregard clusters of size 5 or less.
        continue
    print("Cluster number info: {}".format(cluster))
    print("Number of tweets: {}".format(cluster_size))
    cluster_mentions_dict = mentions_graph(cluster_list)
    cluster_ties, cluster_triads = find_ties_triad(cluster_mentions_dict)
    print("New tweet ties: {}".format(ties))
    print("New tweet triads: {}".format(triads))
