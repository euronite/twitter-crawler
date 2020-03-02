from rest_api import *
from grouping import *
from streaming import run_stream
from user_interaction import *

print("Running Streaming API!")
run_stream(1)
print("Finished Streaming API!")
# start_rest_probe_trends()
all_new_tweets = list(new_tweet.find({}))
all_retweets = list(retweet.find({}))
all_quote_tweets = list(quote_tweet.find({}))
print("Statistics: \n==============")
statistics(all_new_tweets, all_retweets, all_quote_tweets)
list_of_text = get_all_new_tweets_text(all_new_tweets)
cluster_text(list_of_text)
most_frequent_hashtags, most_frequent_users, most_frequent_symbols = extract_important(
    all_new_tweets
)
# for user in most_frequent_users:
#     print("Collecting tweets from {}".format(user[0]))
#     user_search(user[0])
mentions_dict = mentions_graph(all_new_tweets)
# retweets_mentions_dict = mentions_graph(all_retweets)
# quotes_mentions_dict = mentions_graph(all_quote_tweets)
# hashtags_dict = hashtags_groups(all_new_tweets)
ties, triads = find_ties_triad(mentions_dict)

print("ties: {}".format(ties))
print("triads: {}".format(triads))
