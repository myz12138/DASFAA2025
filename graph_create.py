'''
    Target:  create graphs for different graph task
    Input:   (name_of_task,number_of_graphs,is_directed,graph_scale)
    Output:  json_file(node_list,edge_list,is_directed,graph_scale,task_node)
'''
import networkx as nx
import random
import json
import numpy as np
import os
import euler_undirected
_NUMBER_OF_NODES_RANGE = {
    "small":  (5, 15),
    "medium":  (16, 25),
    "large":  (26,35),
}

 #func of add_edge based probability
def rand_edge(G,vi, vj, p): 
    probability = random.random()
    if probability > p:
        G.add_edge(vi, vj) 
        return 
    else:
        not_existence_edges=(vi,vj)
        return not_existence_edges

def Graphs_for_CycleCheck(number_of_graphs,graph_scale,is_directed):
    graphs={}
    #graph generator
    cycle_p={
        "small":  0.83,
        "medium": 0.93,
        "large":  0.95,#0.96 *1000
    }
    for i in range(number_of_graphs):
        if not is_directed:
            G = nx.Graph() 
        else:
            G = nx.DiGraph()
        num_nodes =random.randint( _NUMBER_OF_NODES_RANGE[graph_scale][0],_NUMBER_OF_NODES_RANGE[graph_scale][1])
        G.add_nodes_from([node for node in range(num_nodes)]) 
        not_existence_edges=[]
        for node1 in range(num_nodes):
            for node2 in range(node1):
                probability = random.random()
                if probability >cycle_p[graph_scale]:
                    G.add_edge(node1, node2) 
                else:
                    not_existence_edges.append((node1,node2))  
        graphs[i]={
            'node_list':list(G.nodes()),
            'edge_list':list(G.edges()),
            'degree_list':[G.degree(i) for i in list(G.nodes())],
            'direct_bool':is_directed,
            'scale':graph_scale,
            'task':'cycle_check'
        }
        #task_specialized node generator
      
        
        
        try:
            path=[u for u,v in nx.find_cycle(G)]
            graphs[i]['answer']='Yes'
        except nx.NetworkXNoCycle:
            graphs[i]['answer']='No'

    return graphs
    

def Graphs_for_Reachability(number_of_graphs,graph_scale,is_directed):
    graphs={}
    #graph generator
    Reachability_p={
        "small":  0.81,#0.82* 1000
        "medium": 0.91,#0.91*1000
        "large":  0.93#0.94 *1000
    }
    for i in range(number_of_graphs):
        if not is_directed:
            G = nx.Graph() 
        else:
            G = nx.DiGraph()
        num_nodes =random.randint( _NUMBER_OF_NODES_RANGE[graph_scale][0],_NUMBER_OF_NODES_RANGE[graph_scale][1])
        H = nx.path_graph(num_nodes) 
        G.add_nodes_from(H) 
        not_existence_edges=[]
        for node1 in range(num_nodes):
            for node2 in range(node1):
                probability = random.random()
                if probability > Reachability_p[graph_scale]:
                    G.add_edge(node1, node2) 
                else:
                    not_existence_edges.append((node1,node2))  
            
           
        graphs[i]={
            'node_list':list(G.nodes()),
            'edge_list':list(G.edges()),
            'direct_bool':is_directed,
            'scale':graph_scale,
            'task':'reachability'
        }
    #task_specialized node generator
        source, target = random.sample(list(G.nodes()), k=2)
        graphs[i]['task_node']=[source, target]
        if nx.has_path(G, source, target):
            
            graphs[i]['answer'] = 'Yes'
        else:
            
            graphs[i]['answer']  = 'No'
        
    return graphs
 


def Graphs_for_EulerGrpah(number_of_graphs,graph_scale,is_directed):
    graphs={}
    #graph generator
    for i in range(number_of_graphs):
        num_nodes =random.randint( _NUMBER_OF_NODES_RANGE[graph_scale][0],_NUMBER_OF_NODES_RANGE[graph_scale][1])
        if random.random()<0.5:
            G = euler_undirected.create_eulerian_graph(num_nodes)
        else:
            G=euler_undirected.create_non_eulerian_graph(num_nodes)
        
        #print(len(G.edges())/(num_nodes*(num_nodes-1)/2))
        # G.add_nodes_from([node for node in range(num_nodes)]) 
        # not_existence_edges=[]
        # for node1 in range(num_nodes):
        #     for node2 in range(node1):
        #         probability = random.random()
        #         if probability > euler_p[graph_scale]:
        #             G.add_edge(node1, node2) 
        #         else:
        #             not_existence_edges.append((node1,node2)) 
           
           
        graphs[i]={
            'node_list':list(G.nodes()),
            'edge_list':list(G.edges()),
            'degree_list':[G.degree(i) for i in list(G.nodes())],
            'direct_bool':is_directed,
            'scale':graph_scale,
            'task':'euler_graph'
        }
    #task_specialized node generator
       
        try:
            path = [u for u, v in nx.eulerian_circuit(G,keys=False)]
            
            graphs[i]['answer'] ='Yes' 
        except nx.NetworkXError:
            graphs[i]['answer'] = 'No'
            #'There is no euler path from node %s.' % str(source_node)
        
    return graphs



def Graphs_for_HamiltonPath(number_of_graphs,graph_scale,is_directed):

    def is_hamiltonian(G):
    # 检查连通性
        if not nx.is_connected(G):
            return False
        
        n = G.number_of_nodes()
        
        # 检查 Dirac 定理条件
        if all(d >= n/2 for v, d in G.degree()):
            return True
        
        # 检查 Ore 定理条件
        if all(sum(d for v, d in G.degree() if v not in G[u]) >= n 
            for u in G.nodes()):
            return True
        
        # 如果以上条件都不满足，可以尝试暴力搜索或其他方法
        # 注意：这可能非常耗时，对于大图不实用
        try:
            path = nx.algorithms.tournament.hamiltonian_path(G)
            return len(path) == n
        except:
            return False  # 如果发生异常，说明图不是竞标赛图或没有哈密顿路径
    graphs={}
    #graph generator
    for i in range(number_of_graphs):
        if not is_directed:
            G = nx.Graph() 
            
        num_nodes =random.randint( _NUMBER_OF_NODES_RANGE[graph_scale][0],_NUMBER_OF_NODES_RANGE[graph_scale][1])
        H = nx.path_graph(num_nodes) 
        G.add_nodes_from(H) 
        not_existence_edges=[]
        for node1 in range(num_nodes):
            for node2 in range(node1):
                probability = random.random()
                if probability > 0.8:
                    G.add_edge(node1, node2) 
                else:
                    not_existence_edges.append((node1,node2)) 
           
           
        graphs[i]={
            'node_list':list(G.nodes()),
            'edge_list':list(G.edges()),
            'degree_list':[G.degree(i) for i in list(G.nodes())],
            'direct_bool':is_directed,
            'scale':graph_scale,
            'task':'euler_path'
        }
    #task_specialized node generator
        source_node= random.sample(list(G.nodes()), k=1)[0]
        graphs[i]['task_node']=source_node
        if is_hamiltonian(G):
            graphs[i]['answer'] ='Yes' 
        else:
            graphs[i]['answer'] ='No'
        
        
    return graphs

def Graphs_for_EdgeExistence(number_of_graphs,graph_scale,is_directed):
    graphs={}
    #graph generator
    for i in range(number_of_graphs):
        if not is_directed:
            G = nx.Graph() 
            
        num_nodes =random.randint( _NUMBER_OF_NODES_RANGE[graph_scale][0],_NUMBER_OF_NODES_RANGE[graph_scale][1])
        
        H = nx.path_graph(num_nodes) 
        G.add_nodes_from(H) 
        not_existence_edges=[]
        for node1 in range(num_nodes):
            for node2 in range(node1):
                probability = random.random()
                if probability > 0.8:
                    G.add_edge(node1, node2) 
                else:
                    not_existence_edges.append((node1,node2)) 
           
        graphs[i]={
            'node_list':list(G.nodes()),
            'edge_list':list(G.edges()),
            'direct_bool':is_directed,
            'scale':graph_scale,
            'task':'edge_existence'
        }
    #task_specialized node generator
        choice=random.sample(['existence','not_existence'], k=1)[0]
        if choice=='existence' and  len(graphs[i]['edge_list'])>0:
            edge=random.sample(graphs[i]['edge_list'], k=1)[0]
            source, target=edge[0],edge[1]
            graphs[i]['task_node']=(source, target)
            graphs[i]['answer']='Yes'
            
            
        else:
         
            edge=random.sample(not_existence_edges, k=1)[0]
            source, target=edge[0],edge[1]
            graphs[i]['task_node']=(source, target)
            graphs[i]['answer']='No'
        # except:
        #     edge=random.sample(graphs[i]['edge_list'], k=1)[0]
        #     source, target=edge[0],edge[1]
        #     graphs[i]['task_node']=(source, target)
        #     graphs[i]['answer']='Yes'

    return graphs

def Graphs_for_TopologicalSort(number_of_graphs,graph_scale,is_directed):
    graphs={}
    #graph generator
    for i in range(number_of_graphs):
        if not is_directed:
            G = nx.Graph() 
        else:
            G=nx.DiGraph()
        num_nodes =random.randint( _NUMBER_OF_NODES_RANGE[graph_scale][0],_NUMBER_OF_NODES_RANGE[graph_scale][1])
        H = nx.path_graph(num_nodes) 
        G.add_nodes_from(H) 
        not_existence_edges=[]
        for node1 in range(num_nodes):
            for node2 in range(node1):
                probability = random.random()
                if probability > 0.5:
                    G.add_edge(node1, node2) 
                else:
                    not_existence_edges.append((node1,node2)) 
           
           
        graphs[i]={
            'node_list':list(G.nodes()),
            'edge_list':list(G.edges()),
            'direct_bool':is_directed,
            'scale':graph_scale,
            'task':'topological_sort'
        }
    #task_specialized node generator
        try:
            sort_list=list(nx.topological_sort(G))
            
            graphs[i]['answer'] =sort_list
        except nx.NetworkXError:

            graphs[i]['answer'] = 'No'
            #'There is no euler path from node %s.' % str(source_node)
        
    return graphs

def Graphs_for_ShortestPath(number_of_graphs,graph_scale,is_directed):
    graphs={}
    #graph generator
    for i in range(number_of_graphs):
        if not is_directed:
            G = nx.Graph() 
            
        num_nodes =random.randint( _NUMBER_OF_NODES_RANGE[graph_scale][0],_NUMBER_OF_NODES_RANGE[graph_scale][1])
        H = nx.path_graph(num_nodes) 
        G.add_nodes_from(H) 
        not_existence_edges=[]
        for node1 in range(num_nodes):
            for node2 in range(node1):
                probability = random.random()
                if probability > 0.8:
                    G.add_edge(node1, node2) 
                else:
                    not_existence_edges.append((node1,node2))  
           
           
        graphs[i]={
            'node_list':list(G.nodes()),
            'edge_list':list(G.edges()),
            'direct_bool':is_directed,
            'scale':graph_scale,
            'task':'shortest_path'
        }
    #task_specialized node generator
        source, target = random.sample(list(G.nodes()), k=2)
        try:
            path = nx.shortest_path(G, source, target)
            graphs[i]['task_node']=(source, target)
            graphs[i]['answer'] =str(len(path)-1) 
        except nx.NetworkXNoPath:
            graphs[i]['task_node']=(source, target)
            graphs[i]['answer'] = 'There is no path from node %s to node %s.' % (str(source),str(target))
        
    return graphs


GRAPH_CLASS = {
    'edge_existence': Graphs_for_EdgeExistence,
    'cycle_check':  Graphs_for_CycleCheck,
    'reachability': Graphs_for_Reachability,
    'shortest_path': Graphs_for_ShortestPath,
    'euler_graph':Graphs_for_EulerGrpah,
    'topological_sort':Graphs_for_TopologicalSort,
    'hamilton_path':Graphs_for_HamiltonPath
    
    }

def default_dump(obj):
    """Convert numpy classes to JSON serializable objects."""
    if isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

if __name__=='__main__':
    graphs=Graphs_for_CycleCheck(number_of_graphs=1000,graph_scale='medium',is_directed=False)

    k=0
    for key,value in graphs.items():
        print(value['answer'])
        if value['answer']=='Yes':
            k+=1
    print(k/len(graphs))

    task_type='cycle_check'
    scale='medium'
    dirs = './new_code/'+task_type+'/'+scale
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    with open('./new_code/'+task_type+'/'+scale+'/'+task_type+'_datas.json', 'w',encoding='utf-8') as f:
        b = json.dump(graphs,f,default=default_dump,)