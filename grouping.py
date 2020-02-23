from config import *
import matplotlib.pyplot as plt
import networkx as nx

all_tweets = list(new_tweet.find({}))
all_retweets = list(retweet.find({}))

# Calculates mean sentiment, where 1 is very positive, -1 is very negative
mean_sentiment = 0
for tweet in all_tweets:
    mean_sentiment += tweet['sentiment_polarity']
mean_sentiment = mean_sentiment / len(all_tweets)
print("The mean sentiment of tweets is: ", mean_sentiment)

# Calculates mean subjectivity, where 1 is very subjective, -1 is very objective
mean_subjectivity = 0
for tweet in all_tweets:
    mean_subjectivity += tweet['subjectivity']
    mean_subjectivity = mean_subjectivity / len(all_retweets)
print("The mean subjectivity of retweets is: ", mean_subjectivity)

# graph = nx.DiGraph()
# for i in all_retweets:
# graph.add_edge(i['retweet_user'], i['name'])
# nx.draw_networkx(graph)
# plt.show()
