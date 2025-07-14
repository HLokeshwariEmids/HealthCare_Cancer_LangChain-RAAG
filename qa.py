import os
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
import json
from datetime import datetime
import csv
import re

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class GeminiEmbeddings(Embeddings):
    def __init__(self, model_name="models/embedding-001", api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model_name = model_name

    def embed_documents(self, texts):
        return [genai.embed_content(model=self.model_name, content=t, task_type="retrieval_document")["embedding"] for t in texts]

    def embed_query(self, text):
        return genai.embed_content(model=self.model_name, content=text, task_type="retrieval_query")["embedding"]

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

    eval_prompt = f"""
Evaluate the following LLM-generated answer for the user role: **{role}**.
Provide a score between 0 and 1 for each of the following metrics: {metric_list}.
Also evaluate the hallucination_score (0=accurate, 1=hallucinated).

Return ONLY a JSON object like:
{{
{chr(10).join([f'  "{m}": 0.8,' for m in metrics])}  
  "hallucination_score": 0.1
}}

Question: {question}
Answer: {answer}
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(eval_prompt)
        raw_text = response.text.strip()

        # -------- Clean Gemini Response for JSON --------
        if "```json" in raw_text:
            raw_text = re.findall(r"```json(.*?)```", raw_text, re.DOTALL)
            if raw_text:
                raw_text = raw_text[0].strip()
        elif "```" in raw_text:
            raw_text = re.findall(r"```(.*?)```", raw_text, re.DOTALL)
            if raw_text:
                raw_text = raw_text[0].strip()

        match = re.search(r"{.*}", raw_text, re.DOTALL)
        if match:
            raw_text = match.group(0)

        result = json.loads(raw_text)

        # -------- Compute Confidence Score --------
        hallucination_score = result.get("hallucination_score", 0)
        del result["hallucination_score"]

        weighted_sum = sum(result.values()) / len(result)
        confidence = round(weighted_sum * (1 - hallucination_score), 2)

        result["Confidence Score"] = confidence
        result["Hallucination"] = hallucination_score

        log_to_csv(role, question, answer, result)
        return result

    except Exception as e:
        print("❌ Evaluation Error:", e)
        return None

def log_to_csv(role, question, answer, metrics_dict):
    filename = "logs/evaluation_log.csv"
    os.makedirs("logs", exist_ok=True)

    fields = ["timestamp", "role", "question", "answer"] + list(metrics_dict.keys())
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        role,
        question,
        answer
    ] + [metrics_dict.get(k, 0) for k in metrics_dict]

    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(fields)
        writer.writerow(row)
