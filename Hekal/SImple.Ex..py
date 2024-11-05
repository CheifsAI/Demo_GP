#Prompt
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage

llm = Ollama(model="llama3.1:8b")

prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
prompt.format(product="colorful socks")



text = "What would be a good company name for a company that makes colorful socks?"
messages = [HumanMessage(content=text)]

names = llm.invoke(text)
print(names)
# >> Feetful of Fun

"""chat_model.invoke(messages)
# >> AIMessage(content="Socks O'Color")

#Output parsers
from langchain.output_parsers import CommaSeparatedListOutputParser

output_parser = CommaSeparatedListOutputParser()
output_parser.parse("hi, bye")
# >> ['hi', 'bye']"""
