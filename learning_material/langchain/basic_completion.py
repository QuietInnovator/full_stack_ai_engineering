import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

st.title("Basic Completion")

text = st.text_input("Enter text:")

if st.button("Generate"):
    model = ChatOpenAI(model="gpt-4o-mini")
    response = model.invoke(text)
    st.markdown(f"**Response:** {response.content}")


    