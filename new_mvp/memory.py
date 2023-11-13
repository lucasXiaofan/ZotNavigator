from langchain.vectorstores import pinecone
import pinecone     
import openai
import uuid 
openai.api_key = "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"
pinecone.init(      
	api_key='4089180a-3431-4b18-bf07-c78fb17d8638',      
	environment='gcp-starter'      
)      
high_quality_index = pinecone.Index('highqualityinfo')

def memory_manager(queue,query):
     
    while len(queue) > 10: 
        queue.pop(0)
    queue.append(query)
    return ", ".join(queue)

def pinecone_add(doc_text, title=None):
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
    if title != None: 
        metadata = [{
            'title': title
        }]
    # Prepare the data for upserting into Pinecone
    data_to_upsert = list(zip(doc_id, embedding, metadata))
    # Upsert the data into Pinecone
    high_quality_index.upsert(vectors=data_to_upsert)