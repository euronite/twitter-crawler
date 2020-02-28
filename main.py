from rest_api import *
from grouping import *
from streaming import run_stream

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
