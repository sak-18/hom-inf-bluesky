import pandas as pd
import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import math
from datetime import datetime
import os

def randomize_homophily(G_t1, G_t2, feed):
    G_randomized = G_t2.copy()  # Create a copy of G_t2 for randomization

    # Step 1: Identify T_plus (added edges) and T_minus (removed edges)
    added_edges = list(set(G_t2.edges()) - set(G_t1.edges()))  # Edges added in G_t2
    removed_edges = list(set(G_t1.edges()) - set(G_t2.edges()))  # Edges removed from G_t1

    T_plus = added_edges.copy()
    T_minus = removed_edges.copy()

    # Shuffle the lists to randomize the selection process
    random.shuffle(T_plus)
    random.shuffle(T_minus)

    # Step 2: Randomize added edges (T_plus)
    for (u, v) in added_edges:
        neighbours_u = list(G_t1.neighbors(u))
        selected_edge = None
        for x in T_plus:
            (source_node, des_node) = x
            if des_node not in neighbours_u and des_node != u and x != (u, v):
                selected_edge = x
                break

        if selected_edge is not None:
            new_u, new_v = selected_edge

            # Remove the edge if it exists
            G_randomized.remove_edge(u, v) if G_randomized.has_edge(u, v) else None

            # Add the edge if it doesn't exist
            G_randomized.add_edge(u, new_v) if not G_randomized.has_edge(u, new_v) else None

            # Remove the selected edge from the target list
            T_plus.remove(selected_edge)

    # Step 3: Randomize removed edges (T_minus)
    for (u, v) in removed_edges:
        neighbours_u = list(G_t1.neighbors(u))
        selected_edge = None

        for x in T_minus:
            (source_node, des_node) = x
            if des_node in neighbours_u and x != (u, v):
                selected_edge = x
                break

        if selected_edge is not None:
            new_u, new_v = selected_edge

            # Add the edge if it doesn't exist
            G_randomized.add_edge(u, v) if not G_randomized.has_edge(u, v) else None

            # Remove the edge if it exists
            G_randomized.remove_edge(u, new_v) if G_randomized.has_edge(u, new_v) else None

            # Remove the selected edge from the target list
            T_minus.remove(selected_edge)

    return G_randomized

def homophily_significance_test(G_t1, G_t2, feed):
    print("Homophily for feed:", feed)
    # Compute observed homophily gain for this feed
    observed_homophily_gain = compute_assortativity(G_t2, feed) - compute_assortativity(G_t1, feed)

    # Generate randomized homophily gains
    homophily_gains = []
    num_randomizations = 100

    for _ in range(num_randomizations):
        G_randomized = randomize_homophily(G_t1, G_t2, feed)
        gain = compute_assortativity(G_randomized, feed) - compute_assortativity(G_t1, feed)
        homophily_gains.append(gain)

    # Significance test for homophily
    p_value_homophily = np.mean(np.abs(homophily_gains) >= np.abs(observed_homophily_gain))

    return p_value_homophily

def compute_assortativity(G, feed):
    return nx.attribute_assortativity_coefficient(G, feed)

def randomize_influence(G_t1, G_t2, attribute):
    G_randomized = G_t2.copy()

    # Step 1: Identify nodes with attribute changes
    added_attributes = {node for node in G_t2.nodes if G_t1.nodes[node][attribute] == 0 and G_t2.nodes[node][attribute] == 1}
    removed_attributes = {node for node in G_t2.nodes if G_t1.nodes[node][attribute] == 1 and G_t2.nodes[node][attribute] == 0}

    # Determine the number of attributes to be added and removed
    num_add = len(added_attributes)
    num_remove = len(removed_attributes)

    # Identify potential targets for adding and removing attributes
    potential_add_targets = [node for node in G_t1.nodes if G_t1.nodes[node][attribute] == 0 and node not in added_attributes]
    potential_remove_targets = [node for node in G_t1.nodes if G_t1.nodes[node][attribute] == 1 and node not in removed_attributes]

    # Shuffle the target lists to randomize the selection process
    random.shuffle(potential_add_targets)
    random.shuffle(potential_remove_targets)

    # Step 2: Apply randomization to add attributes (0 -> 1)
    add_targets = random.sample(potential_add_targets, min(num_add, len(potential_add_targets)))
    for node in add_targets:
        G_randomized.nodes[node][attribute] = 1

    # Flip original added attributes to 0 since we are assigning them to other nodes
    for node in added_attributes:
        G_randomized.nodes[node][attribute] = 0

    # Step 3: Apply randomization to remove attributes (1 -> 0)
    remove_targets = random.sample(potential_remove_targets, min(num_remove, len(potential_remove_targets)))
    for node in remove_targets:
        G_randomized.nodes[node][attribute] = 0

    # Flip original removed attributes to 1 since we are assigning them to other nodes
    for node in removed_attributes:
        G_randomized.nodes[node][attribute] = 1

    return G_randomized

def influence_significance_test(G_t1, G_t2, feed):
    print("Influence for feed:", feed)
    # Compute observed gain for this feed
    observed_assortativity_gain = compute_assortativity(G_t2, feed) - compute_assortativity(G_t1, feed)

    # Generate randomized gain
    num_randomizations = 100
    influence_gains = []

    for _ in range(num_randomizations):
        G_randomized = randomize_influence(G_t1, G_t2, feed)
        gain = compute_assortativity(G_randomized, feed) - compute_assortativity(G_t1, feed)
        influence_gains.append(gain)

    # Significance test for influence
    p_value_influence = np.mean(np.abs(influence_gains) >= np.abs(observed_assortativity_gain))

    return p_value_influence

def plot_graph(G, feed, title, save_path):
    plt.figure(figsize=(10, 7))
    
    # Generate a color map based on the feed attribute and count red nodes
    color_map = ['red' if G.nodes[node][feed] == 1 else 'black' for node in G.nodes()]
    red_node_count = sum(1 for color in color_map if color == 'red')
    
    # Use a layout that spreads the nodes out more effectively
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    
    # Draw the graph with smaller nodes and without labels
    nx.draw(G, pos, node_color=color_map, node_size=100, edge_color='gray')
    
    plt.title(title)
    plt.savefig(save_path)
    plt.close()

    # Print the number of red nodes
    print(f'Number of red nodes (feed = 1): {red_node_count}')

# Load the membership graphs
G_t1 = nx.read_gml("membership_graph_t1.gml")
G_t2 = nx.read_gml("membership_graph_t2.gml")

# Define the list of feed attributes (assuming all feed attributes start with 'feed_')
feeds = [attr for attr in G_t1.nodes[next(iter(G_t1.nodes))] if attr.startswith('feed_')]

feeds = random.sample(feeds, 10)

print(feeds)
# Create a directory to save plots if it doesn't exist
os.makedirs("plots", exist_ok=True)


# Perform significance tests for each feed and plot graphs
for feed in feeds:  # Pick first 2 feeds
    print(f"Testing feed: {feed}")
    
    # Perform homophily significance test for the feed
    p_value_homophily = homophily_significance_test(G_t1, G_t2, feed)
    print(f"Homophily p-value for {feed}: {p_value_homophily}")

    # Perform influence significance test for the feed
    p_value_influence = influence_significance_test(G_t1, G_t2, feed)
    print(f"Influence p-value for {feed}: {p_value_influence}")

    # Plot and save the graphs for t=1 and t=2
    plot_graph(G_t1, feed, f"Membership Graph at t=1 for {feed}", f"plots/membership_graph_t1_{feed}.png")
    plot_graph(G_t2, feed, f"Membership Graph at t=2 for {feed}", f"plots/membership_graph_t2_{feed}.png")

print("Graphs saved in 'plots' directory.")