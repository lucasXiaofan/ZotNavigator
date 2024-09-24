from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
import os
import dotenv
dotenv.load_dotenv()

# return embedding of the document
def embed_doc(file): 
    embedding = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API'))
    
    if file[0] == 'txt':
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.create_documents([file[1]])
    elif file[0] == 'pdf':
        text = ""
        for page in file[1].pages:
            text += page.extract_text()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 100,
            length_function = len
        )
        chunks = text_splitter.create_documents([text])
    return FAISS.from_documents(chunks, embedding)

def retrieve_doc(query, db, k=1):
    embedding = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API'))
    query_embedding = embedding.embed_query(query)
    docs = db.similarity_search_by_vector(query_embedding, k=k)
    return [doc.page_content for doc in docs]