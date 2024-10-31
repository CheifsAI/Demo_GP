from langchain.llms import OpenAI
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

def petnamesGenerator():
    llm=OpenAI(api_key="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",temperature=0.7)
    name=llm.invoke("I have a dog pet and I want a cool name for it. Suggest me five cool names for my pet.")
    return name 

if __name__== "__main__":
    print(petnamesGenerator())