from langchain_google_genai import ChatGoogleGenerativeAI

# Create an instance of the LLM, using the 'gemini-pro' model with a specified creativity level
llm = ChatGoogleGenerativeAI(model='gemini-pro', temperature=0.9)

# Send a creative prompt to the LLM
response = llm.invoke('Write a paragraph about life on Mars in year 2100.')
print(response.content)