#!/usr/bin/env python
# coding: utf-8
# By：玉龙同学在炼丹(B站UP)、ChatGPT3.5(OpenAI)

# In[1]:


import json
import numpy as np
import pandas as pd
import os


# In[40]:


def get_jsonlist(data):
    
    #以下代码均由ChatGPT3.5生成
    # 读取 CSV 文件
    data.replace(' ', np.nan, inplace=True)
    # 新建空列表
    dialogue_list = []
    dialogue_json =''
    # 逐行遍历数据集
    i = 0
    while i < len(data):
        # 判断对话开始的标志
        if pd.isnull(data.iloc[i, 0]):
            prompt = ''
            completion = ''
            i += 1
            continue
        elif pd.isnull(data.iloc[i, 1]):
            prompt = data.iloc[i, 0]
            completion = ''
        else:
            raise ValueError("Wrong format. Expecting prompt in first column.")

        # 拼接对话内容
        try:#玉龙：这里我自己+一个判断，因为GPT的代码一直没给我处理最后几行时找不到我的回复或者没有对方的消息的边界情况，那么我直接扔了后面数据
            while not pd.isnull(data.iloc[i, 0]):
                prompt += data.iloc[i, 0] + '\n'
                i += 1
            while not pd.isnull(df.iloc[i, 1]):
                completion += data.iloc[i, 1] + '\n'
                i += 1
            i += 1
        except IndexError:
            break

        # 保存对话内容为 JSON 格式
        # 玉龙：根据实际任务，字段内容也可以保存为prompt和completion，context和summary等等..，只用改dialogue_dict里面的引号中的对应内容即可。
        dialogue_dict = {'context': prompt, 'target': completion}
        dialogue_json = json.dumps(dialogue_dict, ensure_ascii=False)
        dialogue_list.append(dialogue_json)
    
    return dialogue_list


# In[41]:


dialogue_lists=[]
#dialogue_lists=[{'prompt': '你是谁', 'completion': '我恁爹'}]#如果有需要的话，可以加入一些自定义内容，记得将该内容多重复几遍
list_filename=[]
list_filename=os.listdir('微信聊天导出/')
for filename in list_filename:
    df = pd.read_csv('微信聊天导出/'+filename, header=None, usecols=[1, 2], skiprows=3)
    df.replace(' ', np.nan, inplace=True)#将无消息时的空格替换为Nan
    drop_content=['[语音]', '[动画表情]','[应用消息或表情]','[图片]','[视频]','<revokemsg>已撤回</revokemsg>']
    #df=df.drop(df[df[1].isin(drop_content)].index)#移除对方消息中的drop_content。根据需要开启
    #df=df.drop(df[df[0].isin(drop_content)].index)#移除我方消息中的drop_content。根据需要开启
    dialogue_lists+=get_jsonlist(df)
    print('Is Done!_________'+filename)
# 将所有对话内容保存到一个 JSON或JSONline 文件中

#outputname='allmy_wechat_data.json'
# with open(outputname, 'w',encoding='utf-8') as f:
#     f.write('[')
#     for i, dialogue in enumerate(dialogue_lists):
#         f.write(dialogue)
#         if i != len(dialogue_lists) - 1:
#             f.write(',')
#     f.write(']')

outputname='allmy_wechat_data.jsonl'
with open(outputname, 'w',encoding='utf-8') as f:
    for i, dialogue in enumerate(dialogue_lists):
        f.write(dialogue)
        if i != len(dialogue_lists) - 1:
            f.write('\n')
print('所有微信聊天记录已处理并保存在: '+outputname)


# In[ ]:




