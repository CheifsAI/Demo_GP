from langchain.llms import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

llm=ChatOpenAI(model="gpt-4o",temperature=0.7)
name=llm.invoke("what is 18 / 9")
print(name)