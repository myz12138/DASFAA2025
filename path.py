import networkx as nx
import random

def generate_graph(num_nodes, edge_probability):
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            if random.random() < edge_probability:
                G.add_edge(i, j)
    
    return G

def find_non_adjacent_pairs(G):
    non_adjacent_pairs = []
    for u in G.nodes():
        for v in G.nodes():
            if u < v and not G.has_edge(u, v):
                non_adjacent_pairs.append((u, v))
    return non_adjacent_pairs

def check_path_exists(G, u, v):
    return nx.has_path(G, u, v)


num_nodes = 10  
edge_probability = 0.9

G = generate_graph(num_nodes, edge_probability)

non_adjacent_pairs = find_non_adjacent_pairs(G)

pair_with_path = None
pair_without_path = None

for pair in non_adjacent_pairs:
    if pair_without_path is None and not check_path_exists(G, pair[0], pair[1]):
        pair_without_path = pair
    elif pair_with_path is None and check_path_exists(G, pair[0], pair[1]):
        pair_with_path = pair
    
    if pair_with_path and pair_without_path:
        break

