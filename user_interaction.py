def mentions_graph(tweets_list):
    """
    This creates a mentions dictionary, which is the number of times a user has mentioned another, such as:
    {user -> {"user": NumberOfMentions, "user2", "NumberOfMentions"}, "user2" -> {}} etc.
    :param tweets_list: list of tweet objects
    :return: user_dict: list of users and who they mention with frequency
    """
    user_dict = {}
    for tweet in tweets_list:
        if not tweet["name"] in user_dict:
            user_dict[tweet["name"]] = {}
        if len(tweet["user_mentions"]) == 0:
            # Ignore tweets with no mentions
            continue
        for mentioned in tweet["user_mentions"]:
            if mentioned["screen_name"] in user_dict[tweet["name"]]:
                # If the mentioned user is already been previously mentioned by the user
                user_dict[tweet["name"]][mentioned["screen_name"]] += 1
            else:
                # mentioned user has not been mentioned before, add this to dictionary for user
                user_dict[tweet["name"]][mentioned["screen_name"]] = 1
    return user_dict


def hashtags_groups(tweet_list):
    """
    This groups the hashtags in a similar format as user mentions, except excludes the frequency as d list in a dict.
    :param tweet_list: list of tweet objects
    :return: hashtag_dict dictionary of hashtags and a list of hashtags they appear with.
    """
    hashtag_dict = {}
    for tweet in tweet_list:
        if len(tweet["hashtags"]) == 0:
            # ignore tweets with no hashtags
            continue
        for hashtag in tweet["hashtags"]:
            if hashtag["text"] not in hashtag_dict:
                hashtag_dict[hashtag["text"]] = []
            for hashtag2 in tweet["hashtags"]:
                if (
                    hashtag2["text"] != hashtag["text"]
                    and hashtag2["text"] not in hashtag_dict[hashtag["text"]]
                ):
                    # add only unique hashtags to hashtags list
                    hashtag_dict[hashtag["text"]].append(hashtag2["text"])
    return hashtag_dict


def find_ties_triad(mentions_group_dict):
    """
    This finds ties and triads from a mentions group
    :param mentions_group_dict:
    :return:
    ties
        This the number of ties found
    triads
        This is the number of triads found
    """
    ties = 0
    for user in mentions_group_dict:
        for mention_user in mentions_group_dict[user]:
            if mention_user == user:
                # in the even user tags themselves, ignore
                continue
            if (
                mention_user in mentions_group_dict
                and user in mentions_group_dict[mention_user]
            ):
                # If the mentioned user is in a user in the dictionary and has mentioned the previously, add one tie
                ties += 1
    triads = 0
    for user in mentions_group_dict:
        for mention_user in mentions_group_dict[user]:
            if mention_user != user and check_mentions(
                mentions_group_dict, mention_user, user
            ):
                for second_mention_user in mentions_group_dict[user]:
                    if (
                        second_mention_user != mention_user
                        and user != mention_user
                        and check_mentions(
                            mentions_group_dict, second_mention_user, user
                        )
                    ):
                        # this checks that other users have mentioned back so we now know mentioned1 has mentioned
                        # original and mentioned2 has too.
                        if check_mentions(
                            mentions_group_dict, mention_user, second_mention_user
                        ) and check_mentions(
                            mentions_group_dict, second_mention_user, mention_user
                        ):
                            # This means that there's triad! the two people mentioned also mention each other
                            triads += 1
    return ties, triads


def check_mentions(mentions_group_dict, user1, user2):
    """
    This checks if user2 has been mentioned by the user1
    :param mentions_group_dict: dictionary holding users that have been mentioned
    :param user1: The person who has mentioned another
    :param user2:  The user we're checking has been mentioned by user1
    :return: Boolean whether this has been found
    """
    if user1 not in mentions_group_dict:
        return False
    if user2 in mentions_group_dict[user1]:
        return True
    else:
        return False


def user_interaction_graph_stats(mentions_graph_dict):
    """
    This returns the user who has mentioned the most number of times from mentions graph
    :param mentions_graph_dict:
    :return: most_mentioned_user str
    :return: most_mentioned_times int
    """
    most_mentioned_times = 0
    most_mentioned_user = None
    for user in mentions_graph_dict.keys():
        if len(mentions_graph_dict[user]) > most_mentioned_times:
            most_mentioned_times = len(mentions_graph_dict[user])
            most_mentioned_user = user
    return most_mentioned_user, most_mentioned_times
