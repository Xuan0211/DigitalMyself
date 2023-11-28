#from getpass import getpass
#OPENAI_API_KEY = getpass()

# form ./OPENAIKEY.py import OPENAI_API_KEY
from OPENAIKEY import OPENAI_API_KEY

from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

llm = OpenAI(openai_api_key=OPENAI_API_KEY)
chain = LLMChain(llm=llm, prompt=prompt)
question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"
print(chain.run(question))