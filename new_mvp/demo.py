import streamlit as st
st.set_page_config(
    page_title='question and answering with context',
    page_icon='📜'
)
st.title("📖ZotNavigator Key Functions Demo")
st.write(
    """
    ZotNavigator is in the prototyping phase\n
    we are using a small web-scraped datasets from UCI websites, therefore the questions 
    our chatbot can answer with reference are limited\n
    you may check the web-scraped datasets here: https://drive.google.com/drive/u/0/folders/1G5KQwNhSR2Q7d40VhE0kRGdAn5XhNwvX \n
    
    """
)
st.info("✨ You may check out the page for each feature in the left side bar ✨")

st.subheader("Four Key Features")
st.warning("Due to the limitation of streamlit, many features promised in pitch video are not implement in this demo")
st.write("""
    We are using Streamlit as a platform for us to demonstrate the functionality of 4 key features\n
    1. 📚questions answering with student context and UCI-related database\n
    2. ✒️update student's tag through conversation\n
    3. 🤖collect information that match user's profile \n
    4. 🧑‍🏫recommendation system (in development)\n
    
    """
)

