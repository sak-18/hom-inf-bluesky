import pandas as pd
import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import math
from datetime import datetime

import networkx as nx

def create_feed_membership_graph(friendship_network, feeds):
    # Initialize a new graph of the same type as the original friendship network
    new_graph = type(friendship_network)()

    # Iterate over each user in the original friendship network
    for user, data in friendship_network.nodes(data=True):
        # Initialize a dictionary to store the state for each feed
        membership_state = {}
        user_subscriptions = data.get('subscriptions', [])

        # Iterate over all feeds and set the state to 1 if the user is a member, otherwise 0
        for feed in feeds:
            # Prepend 'feed_' to the feed name to ensure it's a valid GML key
            gml_safe_feed_name = f"feed_{feed}"
            membership_state[gml_safe_feed_name] = 1 if feed in user_subscriptions else 0

        # Combine membership states with existing attributes
        new_attributes = {**data, **membership_state}

        # Add the node to the new graph with combined attributes
        new_graph.add_node(user, **new_attributes)

    # Copy edges from the original friendship network
    new_graph.add_edges_from(friendship_network.edges)

    return new_graph

# Function to collect all unique feeds from a given friendship network
def collect_all_feeds(friendship_network):
    feeds = set()
    for _, data in friendship_network.nodes(data=True):
        subscriptions = data.get('subscriptions', [])
        feeds.update(subscriptions)
    return list(feeds)

# Load the friendship networks with feed subscriptions as attributes
friendship_network_t1 = nx.read_gml("friendship_network_t1_attributed.gml")
friendship_network_t2 = nx.read_gml("friendship_network_t2_attributed.gml")

# Collect all feeds across both time points
all_feeds_t1 = collect_all_feeds(friendship_network_t1)
all_feeds_t2 = collect_all_feeds(friendship_network_t2)

# Create new graphs with 0/1 membership states for each feed
membership_graph_t1 = create_feed_membership_graph(friendship_network_t1, all_feeds_t1)
membership_graph_t2 = create_feed_membership_graph(friendship_network_t2, all_feeds_t2)


# Save the new graphs with membership states to GEXF files
nx.write_gml(membership_graph_t1, "membership_graph_t1.gml")
nx.write_gml(membership_graph_t2, "membership_graph_t2.gml")

print("Graphs with membership states saved successfully'")
