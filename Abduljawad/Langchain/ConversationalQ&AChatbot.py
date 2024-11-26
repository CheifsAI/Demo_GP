## Conversational Q&A Chatbot 
import streamlit as st
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage, AIMessage

## Streamlit UI
st.set_page_config(page_title="Conversational Q&A Chatbot")
st.header("Hey, Let's Chat")

chat = ChatOllama(model="llama3.1", temperature=0.7)

if "flowmessages" not in st.session_state:
    st.session_state["flowmessages"] = [
        SystemMessage(content="You are a helpful AI assistant")
    ]
    
def get_chatmodel_response(question):
    
    st.session_state["flowmessages"].append(HumanMessage(content = question))
    answer = chat(st.session_state["flowmessages"])
    st.session_state["flowmessages"].append(AIMessage(content = answer.content))
    return answer.content


question = st.text_input("Enter your question:", key="input")

# Submit Button
if st.button("Ask the question"):
    if question.strip():  # Ensure input is not empty
        with st.spinner("Fetching response..."):
            response = get_chatmodel_response(question)
        st.subheader("Response:")
        st.write(response)
    else:
        st.warning("Please enter a valid question.")