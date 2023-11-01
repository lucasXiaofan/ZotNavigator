
from langchain.chat_models import ChatOpenAI
import streamlit as st
from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text
from langchain.prompts import PromptTemplate 
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain, RetrievalQA
from langchain.agents import AgentExecutor,Tool,ZeroShotAgent
from langchain.chains.question_answering import load_qa_chain

from langchain.llms import openai
# from langchain import HuggingFaceHub
from memory import memory_manager
import os

 #here your HF token
repo="HuggingFaceH4/starchat-beta"

def writehistory(text):
    with open('chathistory.txt', 'a') as f:
        f.write(text)
        f.write('\n')
    f.close()

def retrieve_info(query, db): # best_practice
    similar_response = db.similarity_search(query, k=2)

    best_practice = [doc.page_content for doc in similar_response]

    # print(page_contents_array)

    return best_practice

template = """
    You are a Univeristy faculty that wish to help student thrive emotionally, academically, and socially. 
    I will share a {year} {major} {school} student's message with you and you will give me the best answer that 
    I should send to this student based on given context of student and question, 
    and you will follow ALL of the rules below:

    1/ If there is link in the context, include the link in exact way, 

    2/ If the context are irrelevant to the question, then say you are not sure about the answer

    Below is a question I received from that student:
    {question}

    Here is context that related to the student and questions:
    {context}

    Please write the helpful and concise response that I should send to this student:
    """
new_template = """
    You are a Univeristy faculty that wish to help student thrive emotionally, academically, and socially. 
    I will share a {year} {major} {school} student's message with you and you will give me the best answer that 
    I should send to this student based on given context of student and question, 
    and you will follow ALL of the rules below:
    1/ If there is link in the context, include the link in exact way, 
    Here is context that related to the student and questions:
    {context}
    """



####################################################################
# with memory 
def qa_with_doc_memory(
    #the database
    question,
    year,
    major,
    school,
    openai_api_key,
    hugging_face_api_key,
    index,
    hugging_face = False,
    context = 'empty',
    
    
):
    question_prompt = f"""
                        You are a {school} Univeristy student staff that wish to help student thrive,
                        I will share a {year} {major} student's message with you 
                        and you will give me the best answer that I should send to this student 
                        based on given context of student and question, 
                        and you will follow ALL of the rules below:
                        1/ if possible provide working urls that related to the questions, 
                        2/ keep the response concise
                        here is context that related to the questions:{context}
                        """
    augment_prompt = question_prompt + "here is the questions from student: {question}, here is your conversation history {chat_history}"
    
    prompt = PromptTemplate(
        input_variables=[ 'question','chat_history'],
        template=augment_prompt
    )
    
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(memory_key="chat_history")
    else:
        st.session_state.memory.save_context({'input':question},{'output':''})
    llm = ChatOpenAI(openai_api_key=openai_api_key, max_tokens= 200, temperature=0.1, model="gpt-3.5-turbo-16k-0613")
    chain_conversation = LLMChain(
        llm=llm,
        memory=st.session_state.memory,
        prompt= prompt,   
    )

    return chain_conversation.run(question = question)

###################################################################
# TODO tweak around the prompt to generate better result
# 1. need to experiment how different conversation memory improve the quality of response [],

memory_queue = []

def get_response(question, 
                context,
                openai_key,
                hugging_face_key,
                hugging_face = False,
                year = 'first-year', 
                major = 'undeclare',
                school = "UCI" ):
    if hugging_face or len(openai_key) ==0:
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = hugging_face_key
        llm = None
        # llm =HuggingFaceHub(repo_id=repo , 
        #                  model_kwargs={"min_length":30,
        #                                "max_new_tokens":256, "do_sample":True, 
        #                                "temperature":0.2, "top_k":50, 
        #                                "top_p":0.95, "eos_token_id":49155})
    else:
        llm = ChatOpenAI(openai_api_key=openai_key, max_tokens= 200, temperature=0.1, model="gpt-3.5-turbo-16k-0613")
    # TODO improve the memory system, the start of conversation there is no history
    history = memory_manager(memory_queue,question)
    print(f'from qa: history: {history}')
    question_prompt = """
                        You are a Univeristy faculty that wish to help student thrive,
                        I will share a {year} {major} {school} student's message with you 
                        and you will give me the best answer that I should send to this student 
                        based on given context of student and question, 
                        and you will follow ALL of the rules below:
                        1/ If there is link in the context, include the link in exact way, 
                        the question I received from that student:{question} 
                        here is context that related to the questions:{context}
                        here is the context about the student:{history}"""
    prompt = PromptTemplate(
        input_variables=[ 'year', 'major', 'school', 'question','context','history'],
        template=question_prompt
    )
    
    # memory.chat_memory.add_user_message(question)
    
    chain = LLMChain(llm=llm, 
                    prompt=prompt,)
                    # memory=memory)

    response = chain.run(question=question, 
                        context=context,
                        year = year,
                        major = major,
                        school = school,
                        history = history)
    return response 


