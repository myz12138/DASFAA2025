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

# 设置参数
num_nodes = 10  # 可以根据需要修改节点数量
edge_probability = 0.9

# 生成图
G = generate_graph(num_nodes, edge_probability)

# 找到不相邻的节点对
non_adjacent_pairs = find_non_adjacent_pairs(G)

# 如果存在不相邻的节点对，找出一对有路径和一对无路径的
pair_with_path = None
pair_without_path = None

for pair in non_adjacent_pairs:
    if pair_without_path is None and not check_path_exists(G, pair[0], pair[1]):
        pair_without_path = pair
    elif pair_with_path is None and check_path_exists(G, pair[0], pair[1]):
        pair_with_path = pair
    
    if pair_with_path and pair_without_path:
        break

# 输出结果
print(f"生成的图有 {num_nodes} 个节点和 {G.number_of_edges()} 条边")

if pair_without_path:
    print(f"不相邻且没有路径的节点对: {pair_without_path}")
else:
    print("没有找到不相邻且没有路径的节点对")

if pair_with_path:
    print(f"不相邻但有路径的节点对: {pair_with_path}")
    path = nx.shortest_path(G, pair_with_path[0], pair_with_path[1])
    print(f"  路径: {' -> '.join(map(str, path))}")
else:
    print("没有找到不相邻但有路径的节点对")