from openai import OpenAI
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()


client = OpenAI(api_key=os.getenv('DEEPSEEKER_API'), base_url="https://api.deepseek.com")


response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)

def qa_with_doc_memory(question, year, major, school, context=[]):
    # if context == []:
    #     context = 'empty'
    # else:
    #     context = " ".join(context)
    print(f'context: {context}')
    # Initialize or update chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Limit chat history to last 5 exchanges
    max_history = 5
    st.session_state.chat_history = st.session_state.chat_history[-max_history:]
    
    # Format chat history for the prompt
    chat_history = "\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.chat_history])


    question_prompt = f"""
    You are a {school} University student staff that wishes to help students thrive.
    I will share a {year} {major} student's message with you,
    and you will give me the best answer that I should send to this student
    based on the given context of the student and question.
    Follow ALL of the rules below:
    1/ If possible, provide working URLs related to the questions.
    2/ Keep the response concise.
    Context related to the questions: {context}
    Student's question: {question}
    Conversation history:
    {chat_history}
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": question_prompt},
        ],
        stream=False
    )

    answer = response.choices[0].message.content

    # Update chat history in session state
    st.session_state.chat_history.append((question, answer))

    return answer