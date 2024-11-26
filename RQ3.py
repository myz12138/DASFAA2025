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
task='reachability'
data_type='medium'
model_name="gpt-4o"#'gpt-4o''claude-3-sonnet-20240229'
data_file='100_case_data'
jsonfile_path='./'+data_file+'/'+task+'/'+data_type+'/countnodes_of_'+task+'_'+model_name+'.json'
json_file=read_json(jsonfile_path)
initial,new=0,0
for key,value in json_file.items():
    print(value['initial_judge'])
    initial+=int(value['initial_judge'])
    new+=int(value['new_judge'])
print(initial/100,new/100)