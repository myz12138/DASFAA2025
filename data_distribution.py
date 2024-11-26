import json
task='reachability'
data_type='medium'
model_name="gpt-4o"
#edge_existence
#reachability
#cycle_check
#计算答案分布情况
with open('./new_code/data/'+task+'/'+data_type+'/'+task+'_examples.json','r') as load_f:
    load_dict = json.load(load_f)
    k1=0
    k2=0
    for key,value in load_dict.items():
        
        for path_i in value['path_list']:
            
            if value['node_ids'][0] in path_i:
                k2+=1
        
        if value['answer']=='Yes':
            k1+=1
    print(k1/len(load_dict))
    print(k2/len(load_dict))
    a=1




            

