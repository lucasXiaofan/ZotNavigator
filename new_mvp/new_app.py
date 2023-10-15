# right now is for learning purpose 
import openai
import streamlit as st
import os
from dotenv import load_dotenv
from time import sleep

from parse import read_file
from doc_process import embed_doc
from qa import retrieve_info, get_response, writehistory
from student_profile import profile_school,profile_year,major

load_dotenv()
openai_api_key = os.getenv('openaikey')
# print(openai_api_key)
# av_us = './img/man.png'  #"🦖"  #A single emoji, e.g. "🧑‍💻", "🤖", "🦖". Shortcodes are not supported.
# av_ass = './img/robot.png'

with st.sidebar:
    # TODO need learn what is st.text_input, what is argument key means
    # so the first input is the label of the text_input
    # https://docs.streamlit.io/library/api-reference/widgets/st.text_input
    school: str = st.selectbox("school", options=profile_school)
    major: str = st.selectbox("major", options=major)
    year: str = st.selectbox("year", options=profile_year)
    
    uploaded_file = st.file_uploader(
    "Upload a pdf, docx, or txt file",
    type=["pdf", "txt"],
    help="Scanned documents are not supported yet!",
)


st.title("💬 Chatbot") 
# if "messages" not in st.session_state:
#     # the role here can change the picture of chatbot
#     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    
# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])


# read the file: 
db = None
if uploaded_file:
    st.info('upload file successfully!')
    file = read_file(uploaded_file)
    with st.spinner("Indexing document... This may take a while⏳"):
        db = embed_doc(file,openai_api_key)
        st.info('file embedded successfully')
    

# st.chat_input() is the chat bar
if "messages" not in st.session_state:
    st.session_state.messages = []
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"]):#,avatar=av_us):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):#,avatar=av_ass):
            st.markdown(message["content"])

if myprompt := st.chat_input("What is an AI model?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": myprompt})
    # Display user message in chat message container
    with st.chat_message("user"):#, avatar=av_us):
        st.markdown(myprompt)
        usertext = f"user: {myprompt}"
        writehistory(usertext)
        # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        best_practice = ['empty']
        if db != None:
            best_practice = retrieve_info(usertext,db)
        
        st.info(best_practice[0])
        st.info(f'is school empty? {school == ""} {school} ')
        st.info(f'is year empty? {year}')
        st.info(f'is major empty? {major}')
        
        school = 'UCI' if school == '' else school
        year = 'first-year' if year == '' else year
        major = 'undeclared' if major == '' else major
        
        res  =   get_response(myprompt,
                            best_practice,
                            openai_api_key,
                            school=school,
                            year=year,
                            major= major)
        response = res.split(" ")
        for r in response:
            full_response = full_response + r + " "
            message_placeholder.markdown(full_response + "▌")
            sleep(0.1)
        message_placeholder.markdown(full_response)
        asstext = f"assistant: {full_response}"
        writehistory(asstext)       
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# TODO first read the file 

# file = read_file(with uploaded_file)



# if show_full_doc:
#     with st.expander("Document"):
#         # Hack to get around st.markdown rendering LaTeX
#         st.markdown(f"<p>{wrap_doc_in_html(file.docs)}</p>", unsafe_allow_html=True)


# with st.form(key="qa_form"):
#     query = st.text_area("Ask a question about the document")
#     submit = st.form_submit_button("Submit")


# if submit:
#     if not is_query_valid(query):
#         st.stop()

#     # Output Columns
#     answer_col, sources_col = st.columns(2)

#     llm = get_llm(model=model, openai_api_key=openai_api_key, temperature=0)
#     result = query_folder(
#         folder_index=folder_index,
#         query=query,
#         return_all=return_all_chunks,
#         llm=llm,
#     )

#     with answer_col:
#         st.markdown("#### Answer")
#         st.markdown(result.answer)

#     with sources_col:
#         st.markdown("#### Sources")
#         for source in result.sources:
#             st.markdown(source.page_content)
#             st.markdown(source.metadata["source"])
#             st.markdown("---")