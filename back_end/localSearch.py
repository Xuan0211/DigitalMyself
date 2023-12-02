# -*- coding: utf-8 -*-
"""
	@file:localSearch.py
	@author:Xuan(2022134346@qq.com)
	@description: 本地文本匹配搜索
"""
def localSearch(problem: str):  

	import sys
	import pandas as pd
	from pathlib import Path
	from similarities import BertSimilarity
	sys.path.append('..')

	LOCAL_PATH = str(Path(__file__).parent)

	df = pd.read_csv(LOCAL_PATH + '/store/test.csv', header=None)

	# 1.Compute cosine similarity between two sentences.
	sentences = [problem]
	corpus = df.iloc[:, 0].tolist()
	model = BertSimilarity(model_name_or_path="shibing624/text2vec-base-chinese")

	# 2.Compute similarity between two list
	similarity_scores = model.similarity(sentences, corpus)

	# 3.Semantic Search
	model.add_corpus(corpus)
 
	res = []
	for i in list(model.search(sentences[0], topn=3)[0].keys()):
		res.append(corpus[i])
	return res

if __name__ == '__main__':
    print(localSearch('软件工程生命周期什么？'))