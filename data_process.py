import task_create
import graph_create
import random
import json
import os

NUM_OF_GRAPHS=100
SCALE_OF_GRAPH = ["small",
    "medium",
    "large",]
    
task_list=[
    'edge_existence',
    'cycle_check',
    'reachability',
    'shortest_path',
    'euler_path',
    'topological_sort',
    'hamilton_path'
    ]


def count_distribution(task,graphs_dict):
    k=0
    for key,value in graphs_dict.items():
        if value['answer']=='Yes':
            k+=1
    return k/len(graphs_dict)
#all_graph generator
# for data_type in SCALE_OF_GRAPH:
#     for task in task_list:
#         graphs_dict=graph_create.GRAPH_CLASS[task](number_of_graphs=NUM_OF_GRAPHS,graph_scale=data_type,is_directed=False)
#         dirs = './new_code/data/'+task+'/'+data_type
#         if not os.path.exists(dirs):
#             os.makedirs(dirs)
#         with open('./new_code/data/'+task+'/'+data_type+'/'+task+'_datas.json', 'w',encoding='utf-8') as f1:
#             a= json.dump(graphs_dict,f1)
#         print(data_type,task,count_distribution(task,graphs_dict))
#         examples_dict=task_create.TASK_CLASS[task](graphs_dict,encoding_method='incident')
        
#         with open('./new_code/data/'+task+'/'+data_type+'/'+task+'_examples.json', 'w',encoding='utf-8') as f2:
#             b = json.dump(examples_dict,f2)

#special_graph generator
# task='shortest_path'
# for data_type in SCALE_OF_GRAPH:
#     graphs_dict=graph_create.GRAPH_CLASS[task](number_of_graphs=NUM_OF_GRAPHS,graph_scale=data_type,is_directed=False)
#     dirs = './new_code/data/'+task+'/'+data_type
#     if not os.path.exists(dirs):
#         os.makedirs(dirs)
#     with open('./new_code/data/'+task+'/'+data_type+'/'+task+'_datas.json', 'w',encoding='utf-8') as f1:
#         a= json.dump(graphs_dict,f1)
#     print(data_type,task,count_distribution(task,graphs_dict))
#     examples_dict=task_create.TASK_CLASS[task](graphs_dict,encoding_method='incident')
#     with open('./new_code/data/'+task+'/'+data_type+'/'+task+'_examples.json', 'w',encoding='utf-8') as f2:
#         b = json.dump(examples_dict,f2)

###########ablication data generator
task='cycle_check'#'reachability'#'euler_graph'#'cycle_check'#'edge_existence'
data_file='ablication_data'#'100_case_data'
print(111111111)
for data_type in SCALE_OF_GRAPH:
    graphs_dict=graph_create.GRAPH_CLASS[task](number_of_graphs=NUM_OF_GRAPHS,graph_scale=data_type,is_directed=False)
    dirs = './'+data_file+'/'+task+'/'+data_type
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    with open('./'+data_file+'/'+task+'/'+data_type+'/'+task+'_datas.json', 'w',encoding='utf-8') as f1:
        a= json.dump(graphs_dict,f1)
    print(data_type,task,count_distribution(task,graphs_dict))
    examples_dict=task_create.TASK_CLASS[task](graphs_dict,encoding_method='adjacency')
    with open('./'+data_file+'/'+task+'/'+data_type+'/'+task+'_examples.json', 'w',encoding='utf-8') as f2:
        b = json.dump(examples_dict,f2)


print('finish')
