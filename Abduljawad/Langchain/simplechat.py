from langchain_community.llms import Ollama
import streamlit as st

# Initialize Ollama LLM
llm = Ollama(model="llama3.1")

# Function to get a response from the model
def get_llama_response(question):
    # Use the globally initialized `llm` to process the question
    response = llm(question)
    return response

# Streamlit Page Configuration
st.set_page_config(page_title="Q&A Demo")

# Streamlit App Header
st.header("LangChain Ollama Q&A App")

# User Input
question = st.text_input("Enter your question:", key="input")

# Submit Button
if st.button("Ask the question"):
    if question.strip():  # Ensure input is not empty
        with st.spinner("Fetching response..."):
            response = get_llama_response(question)
        st.subheader("Response:")
        st.write(response)
    else:
        st.warning("Please enter a valid question.")