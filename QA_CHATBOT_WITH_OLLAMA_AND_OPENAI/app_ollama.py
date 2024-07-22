from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os

from dotenv import load_dotenv
load_dotenv()


## Langsmith Tracking
os.environ["LANGCHIAN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="QA_CHATBOT_WITH_OLLAMA"

## Prompt template
system_message = "You are a helpful assistant. Please respond to the queries"
prompt = ChatPromptTemplate.from_messages(
    [
        ("system",system_message),
        ("user","Question:{question}")
    ]
)

def generate_response(question,engine,temperature,max_tokens):
    
    llm=Ollama(model=engine)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer



## Title Of the App
st.title("Enhanced Q&A Chatbot with Ollama")

## Sidebar for parameters
st.sidebar.title("Settings")

## Dropdown for models
engine = st.sidebar.selectbox("Select a model",["gemma:2b","Mistral","Llama3"])

## Slider for temperature
temperature = st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)

## slider for max_tokens
max_tokens = st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)

## Main Interface for User Input
st.write("Ask me Anything")

user_input =st.text_input("You:")


if user_input:
    response = generate_response(user_input,engine,temperature,max_tokens)
    st.write(response)
else:
    st.write("No input has been provided!")