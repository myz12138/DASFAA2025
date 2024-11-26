import openai
from os import getenv
import json
import os
from openai import OpenAI
# from openai import OpenAI
# from openai import OpenAIError
import time
MAX_RETRIES = 5  # 最大重试次数
RETRY_DELAY = 10  # 重试延迟时间(秒)


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
    task_list=['reachability','euler_graph']
    type_list=['large','medium','small']
    for task in task_list:
        for data_type in type_list:
    #task='cycle_check'#'cycle_check'#'edge_existence'#'euler_graph'#'shortest_path'#'reachability'
    #data_type='large'
            model_name="gpt-3.5-turbo"#'gpt-4o''claude-3-sonnet-20240229'
            data_file='1000_data'
            answer_dic={}
            
            
            #记得修改数据类型，是否是原数据，还是消融实验
            jsonfile_path='./'+data_file+'/'+task+'/'+data_type+'/'+task+'_examples.json'
            json_file=read_json(jsonfile_path)


            write_path='./'+data_file+'/'+task+'/'+data_type+'/answer_of_'+task+'_'+model_name+'.json'
            write_file=read_json(write_path)
            client=OpenAI(
                api_key="sk-tU9zASoh0x5C2K0lC34fB1E7107b496c9e1dEc7955FaDfB6",#1119"sk-H2RpG0ChleAv2qZ65bB7F6CfFa0d4bE7A901B5894892B2Da",
                base_url='https://api.gptapi.us/v1'
            )
        
            print('start %s for %s for %s on %s graph'%(model_name,data_file,task,data_type))
            for key,value in json_file.items():
                if int(key)<400:
                    continue
                model=model_name,
                messages_initial=[#of alphabetical order separated by commas,Numeric,from Yes or No.Do not give any reasoning or logic for your answer.
                    {
                        'role':"system",
                        "content":"You are a graph analyst and you must need to give me the final answer. Do not give any reasoning or logic for your answer."
                    },
                {
                "role": "user",
                #"content":'In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. G describes a graph among nodes 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20.\nThe edges in G are: (0, 11) (1, 5) (2, 9) (4, 9) (4, 10) (4, 14) (4, 15) (4, 16) (6, 16) (7, 18) (9, 17) (10, 16) (14, 15) (18, 19). \nQ: Is there at least one cycle in this graph?'
                "content": value['initial_question'],
                }]
                messages_new=[
                        {
                        'role':"system",
                        "content":"You are a graph analyst and you must need to give me the finial answer. Do not give any reasoning or logic for your answer."
                    },
                {
                "role": "user",
                #"content":'In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. G describes a graph among nodes 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20.\nThe edges in G are: (0, 11) (1, 5) (2, 9) (4, 9) (4, 10) (4, 14) (4, 15) (4, 16) (6, 16) (7, 18) (9, 17) (10, 16) (14, 15) (18, 19). \nQ: Is there at least one cycle in this graph?'
                "content": value['new_question'],
                }]

                completion_initial, flag_initial = retry_on_payment_required(create_completion, model, messages_initial)
                # print(completion_initial)
                # if flag_initial == False or ('error' in completion_initial.keys()):
                    
                #     answer_dic[key]={"real_answer":value['answer'],"api_answer_initial":"error."}
                #     print(key,":initial_error")
                # else:
                    #print("completion_initial:\n\n",completion_initial)
                answer_dic[key]={"real_answer":value['answer'],"api_answer_initial": completion_initial.choices[0].message.content,"api_answer_new":""}
                    
                    #print(algorithm+key,":",answer_dic[algorithm+key])

                completion_new, flag_new = retry_on_payment_required(create_completion, model, messages_new)
                # if flag_new == False or ('error' in completion_new.keys()):
                    
                #     answer_dic[key]["api_answer_new"]="error"
                #     print(key,"new_answer:error")
                # else:
                    #print("completion_new:\n\n",completion_new)
                answer_dic[key]["api_answer_new"]=completion_new.choices[0].message.content
                    #completion_new.choices[0].message.content
                    
                print(key,":",answer_dic[key])
                answer_dic[key]['initial_judge'],answer_dic[key]['new_judge']='',''
                if int(key)>600:
                    break
                write_file.update({key:answer_dic[key]})
                with open('./'+data_file+'/'+task+'/'+data_type+'/answer_of_'+task+'_'+model_name+'.json', 'w',encoding='utf-8') as f:
                    b = json.dump(write_file,f,indent=1)
                
        
        

