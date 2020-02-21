from config import *
import matplotlib.pyplot as plt
import networkx as nx

all_tweets = list(new_tweet.find({}))
all_retweets = list(retweet.find({}))
graph = nx.DiGraph()
for i in all_retweets:
    print(i)
    graph.add_edge(i['retweet_user'], i['name'])

nx.draw_networkx(graph)
plt.show()
