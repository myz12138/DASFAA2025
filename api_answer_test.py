import json
task='reachability'
data_type='medium'
model_name='gpt-3.5-turbo'#"claude-3-sonnet-20240229"#'gpt-4o'
data_file='1000_data'#'ablication_data'

#reachability
#cycle_check
#euler_graph
num_graph=1000
with open('./'+data_file+'/'+task+'/'+data_type+'/'+task+'_examples.json','r') as f:
    example_dict=json.load(f)
    with open('./'+data_file+'/'+task+'/'+data_type+'/answer_of_'+task+'_'+model_name+'.json','r') as load_f:
        load_dict = json.load(load_f)
        print(len(load_dict))
        k1,k2=0,0
        k3=0
        
        
        for key,value in load_dict.items():
            if value["api_answer_initial"]=='Yes.':
                value["api_answer_initial"]='Yes'
            if value["api_answer_initial"]=='No.':
                value["api_answer_initial"]='No'

            
            if value["api_answer_initial"]==value['real_answer'] and value["api_answer_initial"]!='error.' and value["api_answer_new"]!='error': 
                
                k1+=1
            
        
                
        print("initial_rate:",k1/len(load_dict),'\n')
        for key,value in load_dict.items():
            if value["api_answer_new"]=='Yes.':
                value["api_answer_new"]='Yes'
            if value["api_answer_new"]=='No.':
                value["api_answer_new"]='No'
        
            if value["api_answer_new"]==value['real_answer'] and value["api_answer_initial"]!='error.' and value["api_answer_new"]!='error': 
                
                k2+=1
            if value['real_answer']=='Yes':
                k3+=1
            
        print("new_rate:",k2/len(load_dict),'\n')

        print("real_rate:",k3/len(load_dict),'\n')
            

