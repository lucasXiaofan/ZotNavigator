
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def writehistory(text):
    with open('chathistory.txt', 'a') as f:
        f.write(text)
        f.write('\n')
    f.close()

def retrieve_info(query, db): # best_practice
    similar_response = db.similarity_search(query, k=3)

    best_practice = [doc.page_content for doc in similar_response]

    # print(page_contents_array)

    return best_practice

# TODO tweak around the prompt to generate better result
def get_response(query, best_practice, openai_key):
    llm = ChatOpenAI(openai_api_key=openai_key, temperature=0, model="gpt-3.5-turbo-16k-0613")

    template = """
    You are a Univeristy faculty that wish to help student thrive emotionally, academically, and socially. 
    I will share a student's message with you and you will give me the best answer that 
    I should send to this student based on past best practies, 
    and you will follow ALL of the rules below:

    1/ Response should be very similar or even identical to the past best practies, 

    2/ If the best practice are irrelevant, then say you don't know

    Below is a question I received from the student:
    {question}

    Here is a list of best practies of how we normally respond to student in similar scenarios:
    {best_practice}

    Please write the best response that I should send to this student:
    """

    prompt = PromptTemplate(
        input_variables=["question", "best_practice"],
        template=template
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run(question=query, best_practice=best_practice)
    return response 