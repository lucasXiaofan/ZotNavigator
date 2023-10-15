
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

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

# TODO tweak around the prompt to generate better result
def get_response(question, advice,openai_key,year = 'first-year', major = 'undeclare',school = "UCI" ):
    llm = ChatOpenAI(openai_api_key=openai_key, temperature=0, model="gpt-3.5-turbo-16k-0613")

    template = """
    You are a Univeristy faculty that wish to help student thrive emotionally, academically, and socially. 
    I will share a {year} {major} {school} student's message with you and you will give me the best answer that 
    I should send to this student based on past advice, 
    and you will follow ALL of the rules below:

    1/ If there is link in the advice, include the link in exact way, 

    2/ If the advice are irrelevant, then say you don't know

    Below is a question I received from that student:
    {question}

    Here is advice of how we normally respond to student in similar scenarios:
    {advice}

    Please write the best response that I should send to this student:
    """

    prompt = PromptTemplate(
        input_variables=["question", "advice", "year", "major", "school"],
        template=template
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run(question=question, 
                        advice=advice,
                        year = year,
                        major = major,
                        school = school)
    return response 