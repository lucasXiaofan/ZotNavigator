import streamlit as st
from dotenv import load_dotenv
from time import sleep
from parse import read_file
from doc_process import embed_doc, retrieve_doc
from memory import retrieve_from_database, check_relevance
import os
# from qa import retrieve_info,qa_with_doc_memory
from newqa import qa_with_doc_memory
from student_profile import profile_school,profile_year,major,up_to_date_info
# from pymongo import MongoClient 
from database import get_database

#-------------------------------------
# Get database, API key
# dbname = get_database()

# collection_name = dbname["test"]
# load_dotenv()


#-------------------------------------------------------
# User Interface elements:
# Including selection in school, major, year type. check if use hugging face model. 
# Also a file upload to acquire enough information to make a response (need to be webscrape by itself)
if "school_database" not in st.session_state:
    st.session_state.school_database = ''

def Updated_info(profile_type):
    if profile_type == 'school':
        return up_to_date_info['school']

with st.sidebar:
    # TODO need learn what is st.text_input, what is argument key means
    # so the first input is the label of the text_input
    school: str = st.selectbox("school",  placeholder=" enter your school" ,index=None,options=profile_school,)
    
    st.write('your current school:', Updated_info('school'))
    
    major: str = st.selectbox("major", options=major)
    year: str = st.selectbox("year", options=profile_year)
    # use_huggingface = st.checkbox('Use Huggingface model')
    uploaded_file = st.file_uploader(
    "Upload a pdf, docx, or txt file",
    type=["pdf", "txt"],
    help="Scanned documents are not supported yet!",
)
st.title("💬 UniGPT") 

#------------------------------------------------------------------------
# Read the uploaded file
if "db" not in st.session_state:
    st.session_state.db = None
if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None


if uploaded_file is not None and uploaded_file != st.session_state.last_uploaded_file:
    st.info('upload file successfully!')
    file = read_file(uploaded_file)
    with st.spinner("Indexing document... This may take a while⏳"):
        try:
            st.session_state.db = embed_doc(file)
            st.info('file embedded successfully')
        except Exception as e:
            st.error(f'Error embedding document: {e}')
            uploaded_file = None
        st.session_state.last_uploaded_file = uploaded_file
#         print(type(uploaded_file), uploaded_file)
elif uploaded_file is not None:
    st.info('Using previously embedded document')
    
#-------------------------------------------------------
# Check whether user is starting a new conversation or resume its previous conversation

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []      

# depends on the context we can provide different chat_input suggestion
if myprompt := st.chat_input("ask me anything about your university"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": myprompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(myprompt)
        usertext = f"user: {myprompt}"
        # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        best_practice = []
        if st.session_state.db != None:
            best_practice = retrieve_doc(usertext,st.session_state.db)
        if check_relevance(usertext, best_practice):
            context_from_db = retrieve_from_database(usertext)
            
            best_practice.append(context_from_db)
        
        st.info(f'context: {best_practice}')
        
        
        school = 'UCI' if school == '' else school
        year = 'first-year' if year == '' else year
        major = 'undeclared' if major == '' else major
        
        res = qa_with_doc_memory(
            
            question=myprompt,
            school=school,
            year = year,
            major=major,
            context=best_practice
            
        )

        #Processing LLM response. 1. presenting result to User. 2. store response to memory
        response = res.split(" ")
        # with st.expander("history/memory"):
        #     st.session_state.memory
        for r in response:
            full_response = full_response + r + " "
            message_placeholder.markdown(full_response + "▌")
            sleep(0.1)
        message_placeholder.markdown(full_response)
        asstext = f"assistant: {full_response}"   
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        #Processing user_info: 1. Storing it to User cache 2. Store it to MongoDB
        # collection_name.insert_one(user_info['text']['data'])


