
import re
from io import BytesIO

from langchain.docstore.document import Document
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader

from PyPDF2 import PdfFileReader, PdfFileWriter,PdfReader
# import fitz this cause problem for streamlit idkw


# !!!! not using mb5 from original file. 
# check what is return from streamlit file uploader:
# https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader
def simplePDFloader(file): # not file_path, lol
    return ('pdf', PdfReader(file))

def simpleTextLoader(file):
    return ('txt',[file.read().decode()])

def read_file(file: BytesIO):
#     """Reads an uploaded file and returns a File object"""
    # if file.name.lower().endswith(".docx"):
#         return DocxFile.from_bytes(file)
    if file.name.lower().endswith(".pdf"):
        return  simplePDFloader(file)
    elif file.name.lower().endswith(".txt"):
        return simpleTextLoader(file)
    else:
        raise NotImplementedError(f"File type {file.name.split('.')[-1]} not supported")
