import os
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
import json, re, csv
from datetime import datetime
from typing import Optional
import google.generativeai as genai

class GeminiEmbeddings(Embeddings):
    def __init__(self, model_name="models/embedding-001", api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("❗ GEMINI_API_KEY is not set in environment or passed explicitly.")
        
        genai.configure(api_key=self.api_key)
        self.model_name = model_name

    def embed_documents(self, texts):
        return [
            genai.embed_content(
                model=self.model_name,
                content=t,
                task_type="retrieval_document"
            )["embedding"]
            for t in texts
        ]

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
        temperature=0.3
    )
    return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_db.as_retriever())

def evaluate_response(question, answer, role):
    role_metrics = {
        "Medical Specialist (Doctor)": ["Correctness", "Specificity", "Fluency"],
        "Public Health Analyst": ["Correctness", "Relevance", "Coherence"],
        "Health-Conscious Patient": ["Fluency", "Coherence", "Confidence"],
        "Medical Research Intern": ["Correctness", "Specificity", "Relevance"]
    }
    default_metrics = ["Correctness", "Relevance", "Fluency"]
    metrics = role_metrics.get(role, default_metrics)
    metric_list = ", ".join(metrics)

    prompt = f"""Evaluate this answer for role **{role}**:
Provide scores (0 to 1) for: {metric_list} + hallucination_score.
Return valid JSON only:
{{
{chr(10).join([f'  "{m}": 0.8,' for m in metrics])}  
  "hallucination_score": 0.1
}}

Q: {question}
A: {answer}
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        raw = response.text.strip()

        # Extract JSON
        raw = re.sub(r"```json|```", "", raw).strip()
        match = re.search(r"{.*}", raw, re.DOTALL)
        if match:
            raw = match.group(0)

        result = json.loads(raw)
        halluc = result.pop("hallucination_score", 0)
        confidence = round((sum(result.values()) / len(result)) * (1 - halluc), 2)

        result["Confidence Score"] = confidence
        result["Hallucination"] = halluc

        log_to_csv(role, question, answer, result)
        return result

    except Exception as e:
        print("❌ Eval Error:", e)
        return None

def log_to_csv(role, question, answer, metrics_dict):
    os.makedirs("logs", exist_ok=True)
    filename = "logs/evaluation_log.csv"
    fields = ["timestamp", "role", "question", "answer"] + list(metrics_dict.keys())
    row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), role, question, answer] + [metrics_dict.get(k, 0) for k in metrics_dict]

    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(fields)
        writer.writerow(row)
