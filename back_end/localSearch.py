# -*- coding: utf-8 -*-
# @Time    : 2023.1.13
# @Author  : Xuan
# @Email   : 2022134346@qq.com
# @File    : localSearch.py
# @Software: Vscode

import os
import sys
import pandas as pd
from pathlib import Path
from similarities import BertSimilarity

import globalSetting

from fileManager import FileManager

def localSearch(problem: str):

    sys.path.append('..')
    
    # 1. 获得所有已启用的数据库列表， 放入DataFrame中
    file_manager = FileManager()
    enableFileList = file_manager.getEnableFileList()
    
    csv_files = []
    for file in enableFileList:
        file = list(file)
        csv_files.append(globalSetting.OUTPUT_FOLDER + str(file[0]) + ".csv")
    
    dfs = []
    for file in csv_files:
        df = pd.read_csv(file, header=None)
        dfs.append(df)
    
    # 2. 合并DataFrame，得到一个大的DataFrame，便于计算相似度。
    concatenated_df = pd.concat(dfs)

    # 3. 计算 cosine similarity between two sentences
    sentences = [problem]
    corpus = concatenated_df.iloc[:, 0].tolist()
    model = BertSimilarity(model_name_or_path="shibing624/text2vec-base-chinese")
    similarity_scores = model.similarity(sentences, corpus)

    # 4. 执行top 3搜索
    model.add_corpus(corpus)

    res = []
    for i in list(model.search(sentences[0], topn=3)[0].keys()):
        res.append(corpus[i])
    return res

if __name__ == '__main__':
    # 单元测试
    print(localSearch('参考书是什么'))
