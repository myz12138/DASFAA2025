import networkx as nx
import random

def create_eulerian_graph(num_nodes):
    while True:
        G = nx.Graph()
        G.add_nodes_from(range(num_nodes))
        
        # 先创建一个连通图
        for i in range(1, num_nodes):
            G.add_edge(i-1, i)
        
        # 添加随机边，确保每个节点的度数都是偶数
        for _ in range(random.randint(0, num_nodes)):
            u = random.randint(0, num_nodes-1)
            v = random.randint(0, num_nodes-1)
            if u != v and not G.has_edge(u, v):
                G.add_edge(u, v)
        
        # 如果有奇数度的节点，随机连接它们
        odd_degree_nodes = [n for n in G.nodes() if G.degree(n) % 2 != 0]
        while odd_degree_nodes:
            u = odd_degree_nodes.pop()
            v = odd_degree_nodes.pop()
            G.add_edge(u, v)
        
        if nx.is_connected(G) and all(G.degree(n) % 2 == 0 for n in G.nodes()):
            return G

def create_non_eulerian_graph(num_nodes):
    while True:
        G = nx.Graph()
        G.add_nodes_from(range(num_nodes))
        
        # 先创建一个连通图
        for i in range(1, num_nodes):
            G.add_edge(i-1, i)
        
        # 添加随机边
        for _ in range(random.randint(0, num_nodes)):
            u = random.randint(0, num_nodes-1)
            v = random.randint(0, num_nodes-1)
            if u != v and not G.has_edge(u, v):
                G.add_edge(u, v)
        
        # 确保至少有一个节点的度数为奇数
        if all(G.degree(n) % 2 == 0 for n in G.nodes()):
            node = random.choice(list(G.nodes()))
            neighbor = random.choice(list(G.neighbors(node)))
            G.remove_edge(node, neighbor)
        
        if nx.is_connected(G) and any(G.degree(n) % 2 != 0 for n in G.nodes()):
            return G


if __name__=="__main__":
    # 主程序
    num_nodes = 50 # 可以根据需要修改节点数量

    # 生成并绘制欧拉图
    eulerian_graph = create_eulerian_graph(num_nodes)
    print("欧拉图是否为欧拉图：", nx.is_eulerian(eulerian_graph))


    # 生成并绘制非欧拉图
    non_eulerian_graph = create_non_eulerian_graph(num_nodes)
    print("非欧拉图是否为欧拉图：", nx.is_eulerian(non_eulerian_graph))


    # 打印每个图中各节点的度数
    print("\n欧拉图节点度数：")
    for node, degree in eulerian_graph.degree():
        print(f"节点 {node}: 度数 {degree}")

    print("\n非欧拉图节点度数：")
    for node, degree in non_eulerian_graph.degree():
        print(f"节点 {node}: 度数 {degree}")