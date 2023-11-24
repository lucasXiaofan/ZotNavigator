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

import pinecone 
import openai
import uuid 
openai.api_key = "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"
pinecone.init(      
	api_key='4089180a-3431-4b18-bf07-c78fb17d8638',      
	environment='gcp-starter'      
)      
high_quality_index = pinecone.Index('highqualityinfo')

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
    embed_response = openai.Embedding.create(input=doc_text, engine="text-embedding-ada-002")
    embedding = embed_response['data'][0]['embedding']
    doc_id = str(uuid.uuid4())
    # Prepare the data for upserting into Pinecone
    data_to_upsert = [zip(doc_id, embedding, metadata)]

    # Upsert the data into Pinecone
    high_quality_index.upsert(vectors=data_to_upsert)

for item in read_and_chunk_txt_files(path):
    metadata = [{'title':item[0]}]
    pinecone_add(item[1],metadata = metadata)
    
    
def check_redundant(): 
    """_summary_ 
    prevent redundant text saved in database
    """
    pass

def retrieve_from_database(query):
    embed_response = openai.Embedding.create(input=query, engine="text-embedding-ada-002")
    embedding = embed_response['data'][0]['embedding']
    doc = high_quality_index.query(embedding,top_k=2)
    print(f'what is the type return from pinecone {type(doc)}, content: {doc}')
    return doc
    
