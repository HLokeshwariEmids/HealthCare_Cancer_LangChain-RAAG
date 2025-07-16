 🧠 Cancer Report Q&A Assistant (Gemini + LangChain + RAG + Guardrails)
 
This is a Role-Aware Retrieval-Augmented Generation (RAG) Q&A assistant that allows doctors, analysts, patients, and researchers to interact intelligently with the 2025 Cancer Facts & Figures PDF. 

Powered by Google Gemini 1.5 Flash, LangChain, and Streamlit, it generates role-specific answers, enforces safety via Guardrails (Pydantic), and evaluates the LLM’s performance using structured metrics.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

 🚀 Key Features

| Feature                               | Description                                                                               |
| ------------------------------------- | ----------------------------------------------------------------------------------------- |
| 📄 **PDF Upload + Chunking**          | Upload any health report in PDF and auto-split it into semantic chunks using `pdfplumber` |
| 🧠 **Gemini Embeddings + LLM**        | Uses `gemini-1.5-flash-latest` for both embeddings and answer generation                  |
| 🗂️ **FAISS Vector DB**               | Stores text embeddings for fast and meaningful retrieval                                  |
| 👥 **Role-Based Prompting**           | Answers are customized for different user roles like Doctor, Analyst, Patient, Intern     |
| 🧩 **Add New Roles**                  | Add your own roles and custom prompts dynamically at runtime                              |
| 🧪 **Evaluation with Metrics**        | Automatically scores answers for **correctness, coherence, hallucination**                |
| 🛡️ **Guardrails (Pydantic + Regex)** | Ensures no hallucinated or unsafe medical content is displayed                            |
| 🔐 **Admin Mode**                     | Set confidence thresholds and flag low-confidence responses                               |
| 🪪 **Flag Inappropriate Answers**     | Flag responses for manual review and audit via CSV logs                                   |
| 🧠 **Show Retrieved Chunks**          | Display top relevant chunks from the document for transparency                            |
| 💬 **User Feedback**                  | Rate and comment on responses to improve the system over time                             |
| 📥 **Download Extracted Chunks**      | Export processed chunks into `.txt` for offline reading                                   |
| 🎨 **Beautiful UI**                   | Built using Streamlit with responsive layout, expander sections, and custom styles        |


---

 🧩 Supported Roles (Customizable)

🩺 Medical Specialist (Doctor)

🧑‍⚕️ Health-Conscious Patient

🧬 Public Health Analyst

🧑‍🔬 Medical Research Intern

👩‍⚕️ Nurse

🧑‍💻 Healthcare Receptionist

➕ Add your own! via runtime interface

---

 🛠️ Technologies Used

| Tool/Library              | Role                                    |
| ------------------------- | --------------------------------------- |
| **LangChain**             | Prompt templates, RetrievalQA, chaining |
| **Gemini 1.5 Flash API**  | Answer generation + document embeddings |
| **Guardrails + Pydantic** | Structured safety enforcement           |
| **FAISS**                 | Fast semantic similarity search         |
| **pdfplumber**            | PDF parsing and chunk extraction        |
| **Streamlit**             | Clean, interactive user interface       |
| **Python 3.10+**          | Backend logic                           |

---

🧪 How It Works – End-to-End Flow

1.📤 Upload PDF
User uploads a cancer facts report (PDF)

2.📚 Chunking
Text is extracted and split into overlapping chunks

3.🔐 Embedding
Each chunk is embedded using Gemini's embedding model

4.📦 Storage
Embeddings are saved into a FAISS vector database

5.👤 Role Selection
User picks a persona like Doctor, Patient, Analyst

6.📝 Question Asking
Role-specific prompts are crafted dynamically

7.🔍 Retrieval
Relevant chunks are retrieved from FAISS

8.🤖 Gemini LLM Answering
Gemini 1.5 Flash generates a response based on context

9.🛡️ Guardrails Validation
Pydantic + regex ensure no unsafe or vague language

10.📊 Evaluation
Correctness, Fluency, Relevance, Hallucination & Confidence are scored

11.✅ Answer Displayed
User sees the final answer, metrics, and related chunks

12.🗣️ Feedback + Flagging
Feedback and moderation logs are stored in CSVs

---
Workflow Flowchart:

<img width="1730" height="3840" alt="Untitled diagram _ Mermaid Chart-2025-07-16-100158" src="https://github.com/user-attachments/assets/9079ba91-f9eb-4b7d-9201-09990a7c152a" />



