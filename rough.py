import pandas as pd
import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import math
from datetime import datetime

#Functions
#Return user node ids subscribed to a target feed (node id as input)
#Input: node id of target feed
#Returns: a list of user node ids
def feed_user_list(target_feed_id):
  neighbors = list(user_community_int_graph.neighbors(target_feed_id))
  #Filter only members subscribed to the feed (not other feeds or creators)
  feed_users = [neighbor for neighbor in neighbors if user_community_int_graph.nodes[neighbor].get("category") == "member"]#member, feed, creator
  return feed_users

#Returns the date of user's subscription to a feed
#Input: feed node id, and user node id
#Returns: date of subscription as a string (%Y-%m-%dT%H:%M:%S.%fZ)
def feed_subscribed_date(feed_id, user_id):
  subscription_metadata = user_community_int_graph.get_edge_data(feed_id, user_id)
  return subscription_metadata["time"]


# Placeholder function to simulate getting followers at a specific time
#Input: target user node id along with snapshot_time in datetime format
#Output a list of user node ids
def get_following_at_time(target_user, snapshot_time):
    """
    Retrieve the list of users that the given target_user is following at a specific snapshot time.

    Args:
    - target_user (str): The user node id whose following list is to be retrieved.
    - snapshot_time (datetime): The time at which the relationships are considered.
    - graph (networkx.DiGraph): The graph representing user interactions with edges containing 'sign' and 'timestamp' attributes.

    Returns:
    - list of str: List of user ids that the target_user is following.
    """
    # Initialize a list to hold the users that the target_user is following
    following = []
    print(list(member_int_graph.successors(target_user)))
    # Iterate over all successors (nodes that the target_user has an edge towards)
    for successor in list(member_int_graph.successors(target_user)):
        # Check the edge data for the relationship between target_user and successor
        edge_data = member_int_graph.get_edge_data(target_user, successor)
        
        edge_formation_timestamp = datetime.strptime(edge_data['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        #print(edge_formation_timestamp)

        # Check if the interaction happened before or at the snapshot_time
        if edge_formation_timestamp <= snapshot_time:
            # Optionally, you could also filter by 'sign' if needed
            # For example, only consider positive interactions
            # if edge_data['sign'] == '+':
            following.append(successor)

    return following


#Returns the friendship network among the given users, at the given snapshot time.
#Input: list of user node ids, and the snapshot time at which friendship network is desired
#Returns: a networkx friendship directed network with given users as nodes and edges denoting follow relationship
def friendship_network(feed_user_list, snapshot_time):
    # Initialize a directed graph
    G = nx.DiGraph()

    # Add users as nodes to the graph
    G.add_nodes_from(feed_user_list)

    # Placeholder: Iterate over each user and build out-links at the given time
    # In a real-world scenario, this would involve querying a database or API
    # to get the list of users each person follows at the snapshot_time.

    for user in feed_user_list:
        # Placeholder: get_following_at_time() would return a list of user ids
        # that the 'user' follows at the snapshot_time.
        following = get_following_at_time(user, snapshot_time)

        for friend in following:
            if friend in feed_user_list:  # Only add edges if the friend is in the list
                G.add_edge(user, friend)
    return G


#############Implementation

#Metadata CSVs
feed_metadata = pd.read_csv("./metadata_under_review/feed_metadata_to_share.csv")
user_metadata = pd.read_csv("./metadata_under_review/user_metadata_to_share.csv")

#Network Graphs
creator_int_graph = nx.read_gexf("./networks_under_review/graph_dimension1_to_share.gexf")
member_int_graph = nx.read_gexf("./networks_under_review/graph_dimension2_to_share.gexf")
user_community_int_graph = nx.read_gexf("./networks_under_review/graph_dimension3_to_share.gexf")
multigraph = nx.read_gexf("./networks_under_review/multi_graph_to_share.gexf")

print("Loaded Network Graphs!")