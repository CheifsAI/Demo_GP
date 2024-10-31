import os
from langchain_community.llms import OpenAI  # Update this as per LangChain's latest structure

# Load API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key is missing. Set it as an environment variable.")

llm = OpenAI(api_key=api_key, temperature=0.7)
name = llm.invoke("I have a dog pet and I want a cool name for it. Suggest me five cool names for my pet.")
print(name)
