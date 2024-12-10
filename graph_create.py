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

    Reachability_p={
        "small":  0.81,
        "medium": 0.91,
        "large":  0.93
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
       

    return graphs

GRAPH_CLASS = {
    'cycle_check':  Graphs_for_CycleCheck,
    'reachability': Graphs_for_Reachability,
    'euler_graph':Graphs_for_EulerGrpah,
   
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
