 🧠 Cancer Report Q&A Assistant (Gemini + LangChain + RAG)

This project is a **Role-Aware Retrieval-Augmented Generation (RAG) Chatbot** that enables healthcare professionals, patients, researchers, and analysts to interact with the **2025 ACS Cancer Facts & Figures** PDF in a personalized and intelligent manner using **Gemini 1.5 Flash API**, **LangChain**, and **Streamlit**.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

 🚀 Features

- 🔍 **PDF Upload and Chunking**: Upload any public health report in PDF format, extract and split it into manageable text chunks.
- 🧠 **Gemini Embeddings + LLM**: Uses Google Gemini 1.5 Flash for both document embeddings and natural language answering.
- 🗂️ **Vector Database (FAISS)**: Stores embedded text chunks for efficient semantic search and retrieval.
- 👥 **Role-Based Prompting**: Customizes answers based on the user's role (Doctor, Patient, Nurse, Analyst, etc.).
- ➕ **Dynamic Role Editor**: Add new user roles with specific prompt templates at runtime.
- ❓ **Question Answering Interface**: Ask role-specific questions about the uploaded cancer report.
- 📊 **Top Document Chunks Display**: See the most relevant parts of the document retrieved for your question.
- ✍️ **User Feedback & Rating**: Give feedback and rate responses for future improvement.
- 📥 **Chunk Download Option**: Download extracted text chunks for offline reference.
- 🎨 **Stylish Streamlit UI**: Beautiful interface with background colors, sidebar, balloon success, and sectioned layout.

---

 🧩 Supported Roles

These roles personalize the prompt and tone of the LLM:

- 🩺 Medical Specialist (Doctor)
- 🧑‍⚕️ Health-Conscious Patient
- 🧬 Public Health Analyst
- 🧑‍🔬 Medical Research Intern
- 👩‍💼 Nurse
- 🧑‍💻 Healthcare Receptionist
- ➕ Add your own roles at runtime via the UI!

---

 🛠️ Technologies Used

- **LangChain**: Prompt engineering, document chunking, and retrieval chaining
- **Gemini 1.5 Flash API**: Google LLM for QA and document embedding
- **FAISS**: Vector similarity search engine for document chunks
- **pdfplumber**: PDF text extraction
- **Streamlit**: Interactive web UI for users
- **Python 3.10+**

---

🧪 How It Works

1. 📄 User uploads a PDF report.
2. ✂️ PDF is split into overlapping text chunks.
3. 🧠 Chunks are embedded via Gemini Embeddings API.
4. 📦 Embeddings are stored in FAISS.
5. 👤 User selects a role and asks a question.
6. 🧾 System constructs a custom prompt based on the role.
7. 🔍 Relevant chunks are retrieved using vector similarity.
8. 🤖 Gemini LLM generates an intelligent role-specific answer.
9. ✅ User sees the answer, retrieved chunks, and can submit feedback.

---
Workflow Flowchart:

![Uploading Untitled diagram _ Mermaid Chart-2025-07-16-094256.png…]()

