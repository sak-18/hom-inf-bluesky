import pandas as pd
import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import math
from datetime import datetime

# Function to get subscriptions for users in the provided friendship network
def get_user_subscriptions(friendship_network, multigraph):
    user_subscriptions = {}

    # Iterate over each user in the friendship network
    for user in friendship_network.nodes:
        # Check if the user exists in the multigraph
        if user in multigraph.nodes:
            subscriptions = []
            # Iterate over the successors of the user in the multigraph
            for successor in multigraph.successors(user):
                successor_data = multigraph.nodes[successor]
                # Check if the successor node is categorized as a feed
                if successor_data.get('category') == "feed":
                    subscriptions.append(successor)
            user_subscriptions[user] = subscriptions
        else:
            user_subscriptions[user] = []  # If no subscriptions found

    return user_subscriptions

# Add subscription data to the friendship network
def add_subscriptions_to_friendship_network(network, user_subscriptions):
    count = 0
    for user in network.nodes:
        print(f"======================================{count}====================================================")
        print("Adding as subscriptions attribute:", user_subscriptions.get(user))
        print("==========================================================================================")
        # Add the subscriptions as an attribute
        network.nodes[user]['subscriptions'] = user_subscriptions.get(user)
        count+=1
    print("Iterated over users:", count)

friendship_network_t1 = nx.read_gexf('friendship_network_t1.gexf')

friendship_network_t2 = nx.read_gexf('friendship_network_t2.gexf')

#Metadata CSVs
feed_metadata = pd.read_csv("./metadata_under_review/feed_metadata_to_share.csv")
user_metadata = pd.read_csv("./metadata_under_review/user_metadata_to_share.csv")

#Network Graphs
#creator_int_graph = nx.read_gexf("./networks_under_review/graph_dimension1_to_share.gexf")

#member_int_graph = nx.read_gexf("./networks_under_review/graph_dimension2_to_share.gexf")

#user_community_int_graph = nx.read_gexf("./networks_under_review/graph_dimension3_to_share.gexf")

multigraph = nx.read_gexf("./networks_under_review/multi_graph_to_share.gexf")


# Gather subscriptions for users in the first friendship network
user_subscriptions_t1 = get_user_subscriptions(friendship_network_t1, multigraph)
# Add subscriptions to the first friendship network
add_subscriptions_to_friendship_network(friendship_network_t1, user_subscriptions_t1)

# Repeat the process for the second friendship network if needed
user_subscriptions_t2 = get_user_subscriptions(friendship_network_t2, multigraph)
add_subscriptions_to_friendship_network(friendship_network_t2, user_subscriptions_t2)

# Optional: Verify the attributes were added correctly
#print(friendship_network_t1.nodes(data=True))
#print(friendship_network_t2.nodes(data=True))

nx.write_gml(friendship_network_t1, "friendship_network_t1_attributed.gml")
nx.write_gml(friendship_network_t2, "friendship_network_t2_attributed.gml")

#Write errors
# nx.write_gexf(friendship_network_t1, "friendship_network_t1_attributed.gexf")
# nx.write_gexf(friendship_network_t2, "friendship_network_t2_attributed.gexf")



