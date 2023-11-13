import streamlit as st
from dotenv import load_dotenv
from time import sleep
from parse import read_file
from doc_process import embed_doc
from qa import retrieve_info,qa_with_doc_memory
from student_profile import profile_school,profile_year,major
from pymongo import MongoClient 
from database import get_database

#-------------------------------------
# Get database, API key
dbname = get_database()

collection_name = dbname["test"]
load_dotenv()
openai_api_key = "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"
huggingface_api_key = "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"


#-------------------------------------------------------
# User Interface elements:
# Including selection in school, major, year type. check if use hugging face model. 
# Also a file upload to acquire enough information to make a response (need to be webscrape by itself)
with st.sidebar:
    # TODO need learn what is st.text_input, what is argument key means
    # so the first input is the label of the text_input
    school: str = st.selectbox("school", options=profile_school)
    major: str = st.selectbox("major", options=major)
    year: str = st.selectbox("year", options=profile_year)
    use_huggingface = st.checkbox('Use Huggingface model')
    uploaded_file = st.file_uploader(
    "Upload a pdf, docx, or txt file",
    type=["pdf", "txt"],
    help="Scanned documents are not supported yet!",
)
st.title("💬 UniGPT") 

#------------------------------------------------------------------------
# Read the uploaded file
if 'id' not in st.session_state:
    st.session_state.id = 0
    st.session_state.db = None
if uploaded_file and uploaded_file.id != st.session_state.id:
    st.session_state.id  = uploaded_file.id
    st.info('upload file successfully!')
    file = read_file(uploaded_file)
    with st.spinner("Indexing document... This may take a while⏳"):
        db = embed_doc(file,openai_api_key)
        st.info('file embedded successfully')
    
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
        best_practice = ['empty']
        if db != None:
            best_practice = retrieve_info(usertext,db)
        
        st.info(f'context: {best_practice[0]}')
        
        
        school = 'UCI' if school == '' else school
        year = 'first-year' if year == '' else year
        major = 'undeclared' if major == '' else major
        
        res, user_info = qa_with_doc_memory(
            
            question=myprompt,
            school=school,
            year = year,
            major=major,
            context=best_practice
            
        )

        #Processing LLM response. 1. presenting result to User. 2. store response to memory
        response = res.split(" ")
        with st.expander("history/memory"):
            st.session_state.memory
        for r in response:
            full_response = full_response + r + " "
            message_placeholder.markdown(full_response + "▌")
            sleep(0.1)
        message_placeholder.markdown(full_response)
        asstext = f"assistant: {full_response}"   
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        #Processing user_info: 1. Storing it to User cache 2. Store it to MongoDB
        collection_name.insert_one(user_info['text']['data'])


