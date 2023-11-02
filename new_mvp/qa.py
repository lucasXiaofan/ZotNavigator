
from langchain.chat_models import ChatOpenAI
import streamlit as st
from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text
from langchain.prompts import PromptTemplate 
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain


# Constant vairable set up: including API, schema for extracting information from conversation, and LLM model
openai_api_key = "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"
person_schema = Object(
        id="person",
        description="Personal information about a college student",
        attributes = [
            Text(
                id="current_major",
                description = "The current major of a college student.",
            ),
            Text(
                id="intended_major",
                description = "A student's academic interest.",
            ),
            Text(
                id="school",
                description = "The university a college students attend.",
            ),
            Text(
                id = "year",
                description="The year a college student is currently at",
            )
        
        ],
        examples = [
            ("Hello. My name is Alexander, a freshman from University of California, Irvine. My major is currently computer science \
            and I want to do some projects in computer science",
            [
                {"current_major": "computer science"},
                {"intended_major": "computer science"},
                {"school": "University of California, Irvine"},
                {"year": "freshman"}
            ]
            ),
            (
                "My major is currently computer engineering, but I wish to transfer to computer science. \
                Do you know how to transfer to computer science?",
                [
                    {"current_major": "computer engineering"},
                    {"intended_major": "computer science"},
                ]
            ),
            (
                "I'm a PhD student currently in Stanford University. I've studied 4 years in University of California, Irvine, majoring \
                    in computer science. Now i wish to pursue computer engineering. Can you give me some resources on computer science?",
                    [
                        {"intended_major": "computer science", "school": ["Stanford University", "University of California, Irvine"]},
                    ]
            ),
            (
                "I'm ready to be a graduate student in University of California, Los Angeles. Before that I'm a graduate student in Harvard \
                University. Can you give me some resources in UCLA?",
                [{"school": ["Harvard University", "University of California, Los Angeles"]}]
            )

        ]

    )
llm = ChatOpenAI(openai_api_key=openai_api_key, max_tokens= 200, temperature=0.1, model="gpt-3.5-turbo-16k-0613")

# Accessory function:
#  1. Managing memory of LLm, 
def memory_manager(queue,query):
    while len(queue) > 10: 
        queue.pop(0)
    queue.append(query)
    return ", ".join(queue)

# 2. Retrieving user information 
def retrieve_info(query, db): # best_practice
    similar_response = db.similarity_search(query, k=2)
    best_practice = [doc.page_content for doc in similar_response]
    return best_practice


####################################################################
# Processing User input
# Output: response, user information
def qa_with_doc_memory(
    question,
    year,
    major,
    school,
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
    
    chain_conversation = LLMChain(
        llm=llm,
        memory=st.session_state.memory,
        prompt= prompt,   
    )
    chain_user_info = create_extraction_chain(llm,person_schema)

    return chain_conversation.run(question = question), chain_user_info(question)

###################################################################
# TODO tweak around the prompt to generate better result
# 1. need to experiment how different conversation memory improve the quality of response [],

