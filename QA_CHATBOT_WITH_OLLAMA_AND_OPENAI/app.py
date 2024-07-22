import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()

## Langsmith Tracking for our project
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")


## Prompt template
system_message = "You are a helpful assistant. Please respond to the queries"
prompt = ChatPromptTemplate.from_messages(
    [
        ("system",system_message),
        ("user","Question:{question}")
    ]
)

def generate_response(question,api_key,llm,temperature,max_tokens):
    openai.api_key=api_key
    llm=ChatOpenAI(model=llm)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer


## Title Of the App
st.title("Enhanced Q&A Chatbot with OpenAI")

## Sidebar for parameters
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API key: ",type="password")

## Dropdown for models
llm = st.sidebar.selectbox("Select a model",["gpt-4o","gpt-4-Turbo","gpt-4"])

## Slider for temperature
temperature = st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)

## slider for max_tokens
max_tokens = st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)

## Main Interface for User Input
st.write("Ask me Anything")

user_input =st.text_input("You:")


if user_input:
    response = generate_response(user_input,api_key,llm,temperature,max_tokens)
    st.write(response)
else:
    st.write("No input has been provided!")