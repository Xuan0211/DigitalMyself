def sendMsgToOpenAI(msg):  
	# form ./OPENAIKEY.py import OPENAI_API_KEY
	# you should import your own OPENAI_API_KEY
	from OPENAIKEY import OPENAI_API_KEY

	from langchain.chains import LLMChain
	from langchain.llms import OpenAI
	from langchain.prompts import PromptTemplate

	template = """Question: {question}

	Answer: Let's think step by step."""

	prompt = PromptTemplate(template=template, input_variables=["question"])

	llm = OpenAI(openai_api_key=OPENAI_API_KEY)
	chain = LLMChain(llm=llm, prompt=prompt)
	question = msg
	ans = chain.run(question)
	print(ans)
	return ans