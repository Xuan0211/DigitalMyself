def sendMsgToOpenAI(msg):  
	# form ./OPENAIKEY.py import OPENAI_API_KEY
	# you should import your own OPENAI_API_KEY
	from OPENAIKEY import OPENAI_API_KEY
	from localSearch import localSearch

	from langchain.chains import LLMChain
	from langchain.llms import OpenAI
	from langchain.prompts import PromptTemplate

	template1 = """Please answer based on the following content,and if you cannot answer, do not fabricate, simply answer 'Code: 1'.
	'\n'or'\\n' in content means a newline
    Context:{content}
    Question: {question}
    Answer:	"""
	
	prompt = PromptTemplate(template=template1, input_variables=["content", "question"])

	llm = OpenAI(openai_api_key=OPENAI_API_KEY)
	chain = LLMChain(llm=llm, prompt=prompt)
	question = msg
	content = ''
	localContent = localSearch(msg)
	for row in range(len(localContent)):
		content += localContent[row] + '\n'
	print("local search back: "+ content)
	ans = chain.run(question=question, content=content)
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
    print(sendMsgToOpenAI('软件工程生命周期什么？'))