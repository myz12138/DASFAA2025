import networkx as nx
import random
import matplotlib.pyplot as plt

def create_directed_eulerian_graph(num_nodes):
    while True:
        G = nx.DiGraph()
        G.add_nodes_from(range(num_nodes))
        
        for i in range(num_nodes):
            j = (i + 1) % num_nodes
            G.add_edge(i, j)

        for _ in range(num_nodes * 2):
            u, v = random.sample(range(num_nodes), 2)
            if not G.has_edge(u, v):
                G.add_edge(u, v)
        
        # 确保每个节点的入度等于出度
        in_degrees = dict(G.in_degree())
        out_degrees = dict(G.out_degree())
        for node in G.nodes():
            while in_degrees[node] != out_degrees[node]:
                if in_degrees[node] < out_degrees[node]:
                    target = random.choice(list(G.nodes()))
                    if target != node and not G.has_edge(node, target):
                        G.add_edge(node, target)
                        in_degrees[target] += 1
                        out_degrees[node] += 1
                else:
                    source = random.choice(list(G.nodes()))
                    if source != node and not G.has_edge(source, node):
                        G.add_edge(source, node)
                        in_degrees[node] += 1
                        out_degrees[source] += 1
        
        if nx.is_strongly_connected(G) and nx.is_eulerian(G):
            return G

def create_directed_non_eulerian_graph(num_nodes):
    while True:
        G = nx.DiGraph()
        G.add_nodes_from(range(num_nodes))
        
        for i in range(num_nodes):
            j = (i + 1) % num_nodes
            G.add_edge(i, j)
        
 
        for _ in range(num_nodes * 2):
            u, v = random.sample(range(num_nodes), 2)
            if not G.has_edge(u, v):
                G.add_edge(u, v)
    
        node = random.choice(list(G.nodes()))
        target = random.choice([n for n in G.nodes() if n != node])
        G.add_edge(node, target)
        
        if nx.is_strongly_connected(G) and not nx.is_eulerian(G):
            return G

def plot_directed_graph(G, title):
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=12, font_weight='bold', 
            arrows=True, arrowsize=20)
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


num_nodes = 20  
eulerian_graph = create_directed_eulerian_graph(num_nodes)
