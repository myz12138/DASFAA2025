import openai
from os import getenv
import json
import os
from openai import OpenAI
import time
MAX_RETRIES = 5 
RETRY_DELAY = 10 


def read_json(jsonfile_path):
    
    f = open(jsonfile_path, 'r')
    content = f.read()
    a = json.loads(content)
    
    f.close()
    return a
def retry_on_payment_required(func, args, kwargs):
        retries = 0
        flag = True
        while retries < MAX_RETRIES:
            try:
                
                return func(args[0], kwargs) , flag
            # except KeyError as e:
            #     flag= False
            #     return ' ',flag
            # except openai.error.APIError  as e:
            #     retries += 1
            #     if retries == MAX_RETRIES:
            #         print("Error: Payment Required (max retries reached)")
            #         flag = False
            #         return ' ', flag
            #     else:
            #         print(f"Error: Payment Required (retrying in {RETRY_DELAY} seconds)")
            #         time.sleep(RETRY_DELAY)
            
            except Exception as e:
                raise e
def create_completion(model, messages):
    return client.chat.completions.create(
            model=model,
        messages=messages
    )

if __name__=="__main__":
    task_list=['reachability']
    type_list=['medium']
    for task in task_list:
        for data_type in type_list:
            model_name=""
            data_file=''
            answer_dic={}
        
            jsonfile_path='./'+data_file+'/'+task+'/'+data_type+'/answer_of_'+task+'_'+model_name+'.json'
            json_file=read_json(jsonfile_path)
            write_path='./'+data_file+'/'+task+'/'+data_type+'/countnodes_of_'+task+'_'+model_name+'.json'
            write_file=read_json(write_path)
            client=OpenAI(
                api_key="",
                base_url=''
            )
        
            print('start %s for %s for %s on %s graph'%(model_name,data_file,task,data_type))
            for key,value in json_file.items():

                model=model_name,
                messages_initial=[
                    {
                        'role':"system",
                        "content":"This context is the answer of graph question about euler graph task. Now you need to count how many places are there descriptions about graph information. Do not give any reasoning or logic for your answer. "
                    },
                {
                "role": "user",
                
                "content": value['api_answer_initial']+' Now you need to count how many places are there descriptions about graph information.',
                }]
                messages_new=[
                        {
                        'role':"system",
                        "content":"This context is the answer of graph question about euler graph task. Now you need to count how many places are there descriptions about graph information. Do not give any reasoning or logic for your answer."
                    },
                {
                "role": "user",
    
                "content": value['api_answer_new']+' Now you need to count how many places are there descriptions about graph information.',
                }]

                completion_initial, flag_initial = retry_on_payment_required(create_completion, model, messages_initial)
           
                answer_dic[key]={"count_answer_initial": completion_initial.choices[0].message.content,"count_answer_new":""}
    
                completion_new, flag_new = retry_on_payment_required(create_completion, model, messages_new)
          
                answer_dic[key]["count_answer_new"]=completion_new.choices[0].message.content
              
                    
                print(key,":",answer_dic[key])
                answer_dic[key]['initial_judge'],answer_dic[key]['new_judge']='',''

                write_file.update({key:answer_dic[key]})
                with open('./'+data_file+'/'+task+'/'+data_type+'/countnodes_of_'+task+'_'+model_name+'.json', 'w',encoding='utf-8') as f:
                    b = json.dump(write_file,f,indent=1)
                
        
        

