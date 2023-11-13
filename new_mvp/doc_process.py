from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

# return embedding of the document
def embed_doc(file, openai_key): 
    embedding = OpenAIEmbeddings(openai_api_key= openai_key)
    
    if file[0] == 'txt':
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        chunks = text_splitter.create_documents([file[1]])
    elif file[0] == 'pdf':
        text = ""
        for page in file[1].pages:
            text+= page.extract_text()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 100,
            length_function = len
        )
        # texts = text_splitter.split_text(text=text)
        chunks = text_splitter.create_documents([text])
    return FAISS.from_documents(chunks, embedding)
    