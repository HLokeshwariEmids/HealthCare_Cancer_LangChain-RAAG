import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_chunks(path, max_chunks=50):
    with pdfplumber.open(path) as pdf:
        raw_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(raw_text)
    return chunks[:max_chunks]
