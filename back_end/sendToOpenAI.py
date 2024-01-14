# -*- coding: utf-8 -*-
# @Time    : 2023.12.2
# @Author  : Xuan
# @Email   : 2022134346@qq.com
# @File    : sendToOpenAI.py
# @Software: Vscode
"""
	本模块用于和OPENAI的大语言模型交互
"""

from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# form ./OPENAIKEY.py import OPENAI_API_KEY
# you should import your own OPENAI_API_KEY
from OPENAIKEY import OPENAI_API_KEY
from localSearch import localSearch


def sendMsgToOpenAI(msg):  
    # 第一个template1，用于查询数据库
	template1 = """Please answer based on the following content,and if you cannot answer, do not fabricate, simply answer 'Code: 1'.
	'\n'or'\\n' in content means a newline
    Context:{content}
    Question: {question}
    Answer:	"""
	
	prompt = PromptTemplate(template=template1, input_variables=["content", "question"])

	# 模型准备
	llm = OpenAI(openai_api_key=OPENAI_API_KEY)
	chain = LLMChain(llm=llm, prompt=prompt)
	
	# 参数生成
	question = msg
	content = ''
	localContent = localSearch(msg)
	for row in range(len(localContent)):
		content += localContent[row] + '\n'
	print("local search back: "+ content)
 
	ans = chain.run(question=question, content=content)
 
	# 本地查询失败，调用全局
	if ans == 'Code: 1' or ans == 'Code: 1.':
		print("anwser with global knowledge")
		template2 = """answer the following question, and answer with header '在知识库中没有查询到该消息，但是您可以参考以下内容\n'
    	Question: {question}
  		Answer:"""
		prompt = PromptTemplate(template=template2, input_variables=["question"])		
		llm = OpenAI(openai_api_key=OPENAI_API_KEY)
		chain = LLMChain(llm=llm, prompt=prompt)		
		ans = chain.run(question=question)
	print(ans)
	return ans

if __name__ == '__main__':
	# 模块设计
    print(sendMsgToOpenAI('软件工程生命周期什么？'))