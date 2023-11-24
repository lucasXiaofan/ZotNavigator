import streamlit as st
from student_profile import profile_school,profile_year,major,up_to_date_info
from extract_user_info import extract_User_info
from langchain.chat_models import ChatOpenAI
from app import openai_api_key
st.subheader("📑Student Profile")
st.write('**Major**:', up_to_date_info['major'])
st.write('**Year**:', up_to_date_info['year'])
st.write('**Tags**:', up_to_date_info['tags'])

# fail to extract feature
st.subheader("✒️Update student profile through conversation")
query = st.text_input("type your query here: ")
llm = ChatOpenAI(openai_api_key=openai_api_key, max_tokens= 200, temperature=0.1, model="gpt-3.5-turbo-16k-0613")
if query:
    tag = extract_User_info(llm=llm,question=query)
    st.info(f'get from user {tag}')