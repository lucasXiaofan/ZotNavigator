def memory_manager(queue,query):
     
    while len(queue) > 10: 
        queue.pop(0)
    queue.append(query)
    return ", ".join(queue)

# maybe we can use to account to set up two different database 
# 1 for high quality dataset
# 2 for conversation memory 
import os
path = r"C:\Users\LangZheZR\Documents\GitHub\UniGPT\new_mvp\fake_database"
def read_and_chunk_txt_files(directory):
    result = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                content = file.read()
                words = content.split()
                result.append((filename,' '.join(words)))
    return result

from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
import uuid 
import os
import dotenv
dotenv.load_dotenv()
client = OpenAI(api_key = os.getenv('OPENAI_API'))

pc  = Pinecone(      
	api_key='4089180a-3431-4b18-bf07-c78fb17d8638'   
)

high_quality_index = pc.Index('zotn')
# def pinecone_add(doc, embedding, type_data= 'high_quality_data'):
#     # TODO: see if I can implement ids and metadatas
#     if type_data == 'high_quality_data':
#         high_quality_index.upsert(vectors = doc )
        
#     elif type_data == 'chat_history':
#         pass 
def pinecone_add(doc_text, metadata=None):
    """
    Add a new document to the Pinecone index after encoding it with OpenAI's embedding.
    
    :param index: The Pinecone index object.
    :param doc_id: A unique identifier for the document.
    :param doc_text: The text of the document to add.
    :param metadata: Optional metadata associated with the document.
    """
    # Create the embedding for the document text
    embed_response = client.embeddings.create(input=doc_text, model="text-embedding-3-large")
    embedding = embed_response.data[0].embedding
    doc_id = str(uuid.uuid4())
    # Prepare the data for upserting into Pinecone
    data_to_upsert = [(doc_id, embedding, metadata)]

    # Upsert the data into Pinecone
    high_quality_index.upsert(vectors=data_to_upsert)

# for item in read_and_chunk_txt_files(path):
#     metadata = [{'title':item[0]}]
#     pinecone_add(item[1],metadata = metadata)
    
    
def check_redundant(): 
    """_summary_ 
    prevent redundant text saved in database
    """
    pass

def retrieve_from_database(query):
    embed_response = client.embeddings.create(input=query, model="text-embedding-3-large")
    embedding = embed_response.data[0].embedding
    doc = high_quality_index.query(vector=embedding,top_k=1,include_metadata=True)
    print('doc from retrieve_from_database: ',doc)
    return [r['metadata']['text'] for r in doc['matches']]


def check_relevance(query, available_datasets):
    client = OpenAI(api_key=os.getenv('DEEPSEEKER_API'), base_url="https://api.deepseek.com")
    # datasets_summary = ", ".join(available_datasets)
    datasets_summary = 'requirements for UCI ics relevant majors: software engineering, computer science, data science, game design'
    
    system_prompt = f"""
    You are an AI assistant tasked with determining if a query is relevant to a set of available resources.
    
    Available resources: {datasets_summary}
    
    If the user's query is relevant to any of the available resources, respond with 'True'.
    If the query is not relevant to any of the resources, respond with 'False'.
    
    Your response should be ONLY 'True' or 'False', with no additional text.
    """
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        stream=False
    )
    print('response from check_relevance: ',response.choices[0].message.content)
    result = response.choices[0].message.content.strip().lower()
    
    return result == 'true'


def parse_and_add_departments(json_file_path):
    with open(json_file_path, 'r') as file:
        departments = json.load(file)

    for department in departments:
        department_name = department['department_name']
        requirements = department['requirements']

        # Format the text
        text = f"Department: {department_name}\n\nRequirements:\n"
        for key, value in requirements.items():
            text += f"{key}:\n{value}\n\n"

        # Prepare metadata
        metadata = {"text": text}

        # Add to Pinecone
        pinecone_add(doc_text=text, metadata=metadata)
        print(f"Added {department_name} to Pinecone")


    
if __name__ == '__main__':

    import json


# Usage
    # json_file_path = "new_mvp/fake_database/departments_requirements.json"
    # parse_and_add_departments(json_file_path)
    # print(retrieve_from_database('requirement for software engineering'))
    client = OpenAI(api_key = os.getenv('OPENAI_API'))
    embed_response = client.embeddings.create(input='requirement for software engineering', model="text-embedding-3-large")
    embedding = embed_response.data[0].embedding
    print(f'len of embedding 1: {len(embedding)}')
    embed_response = client.embeddings.create(input="In some cases, studying a city may provide a distorted view of a nation, particularly in developing or underdeveloped countries. These nations often pour their resources into a single core city to create an image of prosperity, designed to attract domestic talent and foreign investment. This focus can lead to impressive growth in the city, while the rest of the country remains underdeveloped. For instance, Ulaanbaatar, the capital of Mongolia, holds nearly 50% of the country’s population, with 74% of its residents being young and middle-aged. Most of the country's foreign businesses, primarily from China, Russia, South Korea, and Japan, are concentrated in Ulaanbaatar, and the city accounts for more than half of Mongolia’s industrial output. This focus on the capital may give outsiders the impression that Mongolia is highly industrialized, though in reality, much of the country remains economically undeveloped.", model="text-embedding-3-large")
    embedding = embed_response.data[0].embedding
    print(f'len of embedding 2: {len(embedding)}')


