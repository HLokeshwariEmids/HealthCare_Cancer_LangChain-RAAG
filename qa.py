import os
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiEmbeddings(Embeddings):
    def __init__(self, model_name="models/embedding-001", api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model_name = model_name

    def embed_documents(self, texts):
        embeddings = []
        for i in range(0, len(texts), 5):
            batch = texts[i:i+5]
            for t in batch:
                emb = genai.embed_content(
                    model=self.model_name,
                    content=t,
                    task_type="retrieval_document"
                )["embedding"]
                embeddings.append(emb)
        return embeddings

    def embed_query(self, text):
        return genai.embed_content(
            model=self.model_name,
            content=text,
            task_type="retrieval_query"
        )["embedding"]

def build_vector_db(chunks):
    embeddings = GeminiEmbeddings()
    return FAISS.from_texts(chunks, embeddings)

def get_qa_chain(vector_db):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        google_api_key=os.environ["GEMINI_API_KEY"],
        temperature=0.3,
    )
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 3})
    )
