def sendMsgToOpenAI(msg):  
	# form ./OPENAIKEY.py import OPENAI_API_KEY
	# you should import your own OPENAI_API_KEY
	from OPENAIKEY import OPENAI_API_KEY
	from localSearch import localSearch

	from langchain.chains import LLMChain
	from langchain.llms import OpenAI
	from langchain.prompts import PromptTemplate

	template = """Question: {question}

	Answer: Let's think step by step."""
	template1 = """Please answer based on the following content,and if you cannot answer, do not fabricate, simply answer 'I don't know'.
	'\n'or'\\n' in content means a newline
    Context:{content}
    Question: {question}
    Answer:	"""
	
	#prompt = PromptTemplate(template=template, input_variables=["question"])
	prompt = PromptTemplate(template=template1, input_variables=["content", "question"])

	llm = OpenAI(openai_api_key=OPENAI_API_KEY)
	chain = LLMChain(llm=llm, prompt=prompt)
	question = msg
	content = localSearch(msg)[0]
	ans = chain.run(question=question, content=content)
	print(ans)
	return ans

if __name__ == '__main__':
    print(sendMsgToOpenAI('软件工程生命周期什么？'))