import networkx as nx
import random
_NUMBER_OF_NODES_RANGE = {
    "small":  (5, 15),
    "medium":  (16, 25),
    "large":  (26,35),
}
def generate_graphs(graph_scale, is_directed,num_graphs):
    undirected_graphs = []
    directed_graphs = []
    if not is_directed:
        for _ in range(num_graphs):
            # undirected graph generation
            num_nodes=random.randint( _NUMBER_OF_NODES_RANGE[graph_scale][0],_NUMBER_OF_NODES_RANGE[graph_scale][1])
            if random.random() < 0.5:  # 50%的概率生成无环图
                g = nx.gnp_random_graph(num_nodes, 0.3, directed=False)
                while not nx.is_tree(g):
                    g = nx.gnp_random_graph(num_nodes, 0.3, directed=False)
            else:
                g = nx.gnp_random_graph(num_nodes, 0.3, directed=False)
            undirected_graphs.append(g)
        return undirected_graphs
    else:
        for _ in range(num_graphs):
            # directed graph generation
            num_nodes=random.randint( _NUMBER_OF_NODES_RANGE[graph_scale][0],_NUMBER_OF_NODES_RANGE[graph_scale][1])
            if random.random() < 0.5:  # 50%的概率生成无环图
                g = nx.gnp_random_graph(num_nodes, 0.3, directed=True)
                while nx.is_directed_acyclic_graph(g) == False:
                    g = nx.gnp_random_graph(num_nodes, 0.3, directed=True)
            else:
                g = nx.gnp_random_graph(num_nodes, 0.3, directed=True)
            directed_graphs.append(g)
        return directed_graphs
 
if __name__=="__main__":
# 使用方法
    nodes_scale = 10  # 可以根据需要修改节点数量
    undirected_graphs= generate_graphs(nodes_scale,num_graphs=100,is_directed=False)

    print(f"生成了 {len(undirected_graphs)} 个无向图和 ")

    # 验证无环图的比例
    undirected_acyclic = sum(1 for g in undirected_graphs if nx.is_tree(g))
    

    print(f"无向无环图比例: {undirected_acyclic / len(undirected_graphs):.2%}")
    