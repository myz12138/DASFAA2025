import  graph_text_encoder
import random
import json
import networkx as nx
def self_deepwalk(node_list,edge_list,num_of_walks,max_length,is_random,start_nodes='None',):
    
    graph=nx.Graph()
    for node in node_list:
       graph.add_node(node)
    graph.add_edges_from(edge_list)
    all_walks=[]
    for start_node in start_nodes:
        step_walks=[]
        for i in range(num_of_walks):
            if is_random:
                random_node=random.sample(node_list,k=1)[0]
            else:
                random_node=start_node
            now_walk=[random_node]
            max_find=0
            try:
                while len(now_walk)<max_length and max_find<30 and len(list(graph.neighbors(random_node)))>0:
                    max_find+=1
                    neighbor_nodes=list(graph.neighbors(random_node))
                    choice_node=random.choice(neighbor_nodes)
                    if choice_node not in now_walk:
                        random_node=choice_node
                        now_walk.append(choice_node)
                        continue
            except:
                now_walk=[random_node]
            step_walks.append(now_walk)
        all_walks.append(step_walks)
    return all_walks

def Task_of_CycleCheck(graphs_dict,
      encoding_method,
      ):
    """The graph task to check if there is at least one cycle or not."""

    'You just need to give me the final answer.'
    examples_dict = {}
    for ind, graph in graphs_dict.items():
      task_description = '\nQ: Is there at least one cycle in this graph? You just need to give me the final answer.\nA: '
      new_question = graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method)
          

      new_question+="Now you need to check if there is at least one cycle or not. "# There is some useful information of node degrees in this graph may help you reason by using relative algorithm. "
      # sequences=graph['degree_list']
      # for k in range(len(sequences)):
      #    new_question+='The degree of node %s is %s. '%(str(k),sequences[k])

      new_question+="There is some useful information of paths in this graph may help you reason by using relative algorithm. These paths are represented by list and each element in the list represents a node. "
      
      sequences=self_deepwalk(graph['node_list'],graph['edge_list'],num_of_walks=10,max_length=len(graph['node_list']),start_nodes='None',is_random=True)
      
      new_question+='These paths are : '
      for k in range(len(sequences[0])-1):
        if len(sequences[0][k])>1:
          new_question+="%s," %sequences[0][k]
      new_question+="%s. " %sequences[0][-1]

      
      new_question+=task_description

      
      initial_question =graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method)
      initial_question+=task_description

      examples_dict[ind] = {
          'new_question': new_question,
          'initial_question':initial_question,
          'answer': graph['answer'],
          'nnodes': str(len(graph['node_list'])),
          'nedges': str(len(graph['edge_list'])),
          'nodes_list':graph['node_list'],
          'edge_list':graph['edge_list'],
          'path_list':sequences
      }
    return examples_dict

def  Task_of_EulerGraph(graphs_dict,
      encoding_method,
      ):
    """The graph task to check if this graph is an euler graph."""

    # You just need to give me the final answer.
    examples_dict = {}
    for ind, graph in graphs_dict.items():
      task_description = '\nQ: Is this graph an euler graph?\nA: '
      new_question = graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method)
      new_question+='Now you need to check if this graph is an euler graph or not. There is some useful information of node degrees in this graph may help you reason by using relative algorithm. '
      #new_question+='There are some knowledge may help you to reaosn: A graph is euler graph if and only if the graph is connected and the number of odd degree nodes in graph G is 0. To answer the question of euler graph, you can try to calculate the degree of each node in this graph firstly and then reason step by step.' 
      #'There are some information about the degree of nodes may help you understand this graph. '
      sequences=graph['degree_list']
      for k in range(len(sequences)):
         new_question+='The degree of node %s is %s. '%(str(k),sequences[k])
      new_question+=task_description
      
      initial_question =graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method)
      initial_question+=task_description

      examples_dict[ind] = {
          'new_question': new_question,
          'initial_question':initial_question,
          'answer': graph['answer'],
          'nnodes': str(len(graph['node_list'])),
          'nedges': str(len(graph['edge_list'])),
          'nodes_list':graph['node_list'],
          'edge_list':graph['edge_list'],
          'path_list':sequences
      }
    return examples_dict


def Task_of_Reachability(graphs_dict,
      encoding_method,
      ):
    """The graph task to check if there is a path from a source to target."""

    'You just need to give me the final answer.'
    examples_dict = {}
    for ind, graph in graphs_dict.items():
      task_description = '\nQ: Is there a path between node %s and node %s?\nA: '% (
          str(graph['task_node'][0]),
          str(graph['task_node'][1]),
      )
      new_question = graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method)

      new_question+="Now you need to check if there is a path between two nodes. There is some useful information of paths in this graph may help you reason by using relative algorithm. These paths are represented by list and each element in the list represents a node. "
      
      sequences=self_deepwalk(graph['node_list'],graph['edge_list'],num_of_walks=10,max_length=len(graph['node_list']),start_nodes=graph['task_node'],is_random=False)
      
      new_question+='These paths are start from node %s: '%graph['task_node'][0]
      for k in range(len(sequences[0])-1):
        if len(sequences[0][k])>1:
          new_question+="%s," %sequences[0][k]
      new_question+="%s. " %sequences[0][-1]

      new_question+='These paths are start from node %s: '%graph['task_node'][1]
      for k in range(len(sequences[1])-1):
        if len(sequences[0][k])>1:
          new_question+="%s," %sequences[1][k]
      new_question+="%s. " %sequences[1][-1]

      new_question+=task_description
      
      initial_question =graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method)
      initial_question+=task_description

      examples_dict[ind] = {
          'new_question': new_question,
          'initial_question':initial_question,
          'answer': graph['answer'],
          'nnodes': str(len(graph['node_list'])),
          'nedges': str(len(graph['edge_list'])),
          'node_ids': graph['task_node'],
          'nodes_list':graph['node_list'],
          'edge_list':graph['edge_list'],
          'path_list':sequences
      }
    return examples_dict

def  Task_of_ShortestPath(graphs_dict,
      encoding_method,
      ):
    """The graph task to check the length of the shortest path from a source to target."""

    
    examples_dict = {}
    for ind, graph in graphs_dict.items():
      task_description = '\nQ: what is the length of the shortest path from node %s to node %s? You just need to give me the final answer.\nAnswer: '% (
          str(graph['task_node'][0]),
          str(graph['task_node'][1]),
      )
      new_question = graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method)

      new_question+="There are some paths start from node "+str(graph['task_node'][0])+" in this graph may help you to reason. A list including nodes represents a path: "
      sequences=self_deepwalk(graph['node_list'],graph['edge_list'],num_of_walks=10,max_length=10,start_node=graph['task_node'][0],is_random=False)
      for k in range(len(sequences)-1):
        if len(sequences[k])>1:
          new_question+="%s," %sequences[k]
      new_question+="%s." %sequences[-1]
      new_question+=task_description
      
      initial_question =graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method)
      initial_question+=task_description

      examples_dict[ind] = {
          'new_question': new_question,
          'initial_question':initial_question,
          'answer': graph['answer'],
          'nnodes': str(len(graph['node_list'])),
          'nedges': str(len(graph['edge_list'])),
          'node_ids': graph['task_node'],
          'nodes_list':graph['node_list'],
          'edge_list':graph['edge_list'],
          'path_list':sequences
      }
    return examples_dict

def  Task_of_HamiltonPath(graphs_dict,
      encoding_method,
      ):
    """The graph task to check if the graph is Hamilton graph."""

    
    examples_dict = {}
    for ind, graph in graphs_dict.items():
      task_description = '\nQ: Is this graph a hamilton graph? You just need to give me the final answer.\nAnswer: '
      new_question = graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method)

      #new_question+="There are some paths start from node "+str(graph['task_node'])+" in this graph may help you to reason. A list including nodes represents a path: "
      # sequences=self_deepwalk(graph['node_list'],graph['edge_list'],num_of_walks=10,max_length=10,start_node=graph['task_node'],is_random=False)
      # for k in range(len(sequences)-1):
      #   if len(sequences[k])>1:
      #     new_question+="%s," %sequences[k]
      # new_question+="%s." %sequences[-1]
      # new_question+=task_description

      new_question+='There are some information about the degree of nodes may help you understand this graph. '
      sequences=graph['degree_list']
      for k in range(len(sequences)):
         new_question+='The degree of node %s is %s.'%(str(k),sequences[k])
      new_question+=task_description
      
      initial_question =graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method)
      initial_question+=task_description

      examples_dict[ind] = {
          'new_question': new_question,
          'initial_question':initial_question,
          'answer': graph['answer'],
          'nnodes': str(len(graph['node_list'])),
          'nedges': str(len(graph['edge_list'])),
          'node_ids': graph['task_node'],
          'nodes_list':graph['node_list'],
          'edge_list':graph['edge_list'],
          'path_list':sequences
      }
    return examples_dict

def  Task_of_TopologicalSort(graphs_dict,
      encoding_method,
      ):
    """The graph task to get the topological sort of this graph."""

    
    examples_dict = {}
    for ind, graph in graphs_dict.items():
      task_description = '\nQ:Please give me the topological sort of this graph. You just need to give me the final answer.\nAnswer: '
      new_question = graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method)

      new_question+="There are some paths in this graph may help you reason. A list including nodes represents a path: "
      sequences=self_deepwalk(graph['node_list'],graph['edge_list'],num_of_walks=20,max_length=10,is_random=False)
      for k in range(len(sequences)-1):
        if len(sequences[k])>1:
          new_question+="%s," %sequences[k]
      new_question+="%s." %sequences[-1]
      new_question+=task_description

      
      initial_question =graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method)
      initial_question+=task_description

      examples_dict[ind] = {
          'new_question': new_question,
          'initial_question':initial_question,
          'answer': graph['answer'],
          'nnodes': str(len(graph['node_list'])),
          'nedges': str(len(graph['edge_list'])),
          
          'nodes_list':graph['node_list'],
          'edge_list':graph['edge_list'],
          'path_list':sequences
      }
    return examples_dict

def Task_of_EdgeExistence(graphs_dict,
      encoding_method,
      ):
    """The graph task to check if an edge exist in a graph or not."""

    
    examples_dict = {}
    for ind, graph in graphs_dict.items():
      task_description = '\nQ: Is node %s connected to node %s? You just need to give me the final answer.\nA: '% (
          str(graph['task_node'][0]),
          str(graph['task_node'][1]),
      )
      new_question = graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method)

      new_question+="There are some paths start from node "+str(graph['task_node'][0])+" in this graph may help you to reason. A list including nodes represents a path: "
      sequences=self_deepwalk(graph['node_list'],graph['edge_list'],num_of_walks=10,max_length=10,start_node=graph['task_node'][0],is_random=True)
      for k in range(len(sequences)-1):
        if len(sequences[k])>1:
          new_question+="%s," %sequences[k]
      new_question+="%s." %sequences[-1]
      new_question+=task_description
      
      initial_question =graph_text_encoder.encode_graph(graph['node_list'],graph['edge_list'], encoding_method)
      initial_question+=task_description

      examples_dict[ind] = {
          'new_question': new_question,
          'initial_question':initial_question,
          'answer': graph['answer'],
          'nnodes': str(len(graph['node_list'])),
          'nedges': str(len(graph['edge_list'])),
          'node_ids': graph['task_node'],
          'nodes_list':graph['node_list'],
          'edge_list':graph['edge_list'],
          'path_list':sequences
      }
    return examples_dict
TASK_CLASS = {
    'edge_existence': Task_of_EdgeExistence,
    'cycle_check':  Task_of_CycleCheck,
    'reachability': Task_of_Reachability,
    'shortest_path':Task_of_ShortestPath,
    'euler_graph': Task_of_EulerGraph,
    'topological_sort':Task_of_TopologicalSort,
    'hamilton_path':Task_of_HamiltonPath
    
    }
if __name__=='__main__':
  task_type='cycle_check'
  scale='medium'
  with open('./new_code/'+task_type+'/'+scale+'/'+task_type+'_datas.json', 'r') as f:
      graphs_dict= json.load(f)
  examples_dict=Task_of_CycleCheck(graphs_dict,encoding_method='incident')
  with open('./new_code/'+task_type+'/'+scale+'/'+task_type+'_examples.json', 'w',encoding='utf-8') as f2:
      b = json.dump(examples_dict,f2,)