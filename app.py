import os
import streamlit as st
from dotenv import load_dotenv
from ingest import extract_chunks
from qa import build_vector_db, get_qa_chain
from prompts import get_prompt
from roles import USER_ROLES
import time
import base64

load_dotenv()
# Load API key from secrets or fallback to .env
api_key = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")



st.set_page_config(page_title="🧠 Cancer Report RAG", layout="wide")

# Inject custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #F2F6FC;
    }
    .title {
        font-size: 40px;
        color: #0a1f44;
        font-weight: 700;
        margin-bottom: 20px;
    }
    .answer-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    .sidebar-title {
        font-size: 18px;
        font-weight: 600;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #ddeeff;
        color: #333;
        text-align: center;
        padding: 10px;
    }
    .download-link {
        text-decoration: none;
        font-weight: bold;
        color: #004080;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🧠 Cancer Report Q&A Assistant (Gemini + RAG)</div>", unsafe_allow_html=True)

st.sidebar.title("⚙️ App Options")
st.sidebar.markdown("Please upload a public cancer report PDF (e.g., ACS 2025) to get started.")

# Check for Gemini API key
# Inject into env for langchain + Gemini access
if api_key:
    os.environ["GEMINI_API_KEY"] = api_key
else:
    st.set_page_config(page_title="🧠 Cancer Report RAG", layout="wide")
    st.error("❗ Gemini API key not found. Please set it in .env (for local) or Secrets (Streamlit Cloud).")
    st.stop()


st.markdown("## 📤Upload a Cancer Report PDF")
pdf_file = st.file_uploader("Choose your Cancer Facts PDF", type="pdf")

if pdf_file:
    if "chunks" not in st.session_state:
        with open("temp.pdf", "wb") as f:
            f.write(pdf_file.getbuffer())

        with st.spinner("📚 Processing PDF into chunks and creating embeddings..."):
            chunks = extract_chunks("temp.pdf", max_chunks=50)
            vector_db = build_vector_db(chunks)
            qa_chain = get_qa_chain(vector_db)

            st.session_state.chunks = chunks
            st.session_state.vector_db = vector_db
            st.session_state.qa_chain = qa_chain

        st.success("✅ Document processed! Now you can ask questions below.")
        st.balloons()

if "qa_chain" in st.session_state:
    st.markdown("## 🧪Select or Add Role, Then Ask a Question")

    role_options = list(USER_ROLES.keys()) + ["Add a new role"]
    selected = st.selectbox("👤 Choose a role or create one", role_options)

    if selected == "Add a new role":
        new_role = st.text_input("Enter new role name")
        new_prompt = st.text_area("Enter prompt template for the role")
        if st.button("➕ Save Role"):
            if new_role and new_prompt:
                USER_ROLES[new_role] = new_prompt
                st.success(f"✅ Role '{new_role}' added! Now you can select it and ask a question.")
    else:
        question = st.text_input("❓ What would you like to know based on this report?")

        if st.button("Ask Question"):
            if not question.strip():
                st.warning("Please enter a valid question.")
            else:
                final_prompt = get_prompt(selected, question)
                with st.spinner("🤖 Generating intelligent response..."):
                    start_time = time.time()
                    answer = st.session_state.qa_chain.run(final_prompt)
                    duration = round(time.time() - start_time, 2)

                st.markdown(f"<div class='answer-box'><b>{selected} says:</b><br><br>{answer}</div>", unsafe_allow_html=True)
                st.success(f"✅ Answered in {duration} seconds")

                with st.expander("📂 View Top Retrieved Chunks"):
                    docs = st.session_state.qa_chain.retriever.get_relevant_documents(question)
                    for i, doc in enumerate(docs):
                        st.markdown(f"<div class='answer-box'><b>Chunk {i+1}:</b><br>{doc.page_content[:300]}...</div>", unsafe_allow_html=True)

                with st.expander("📣 Submit Feedback"):
                    feedback = st.text_area("📝 Your feedback on the answer")
                    rating = st.slider("⭐ Helpfulness Rating", 1, 5, 3)
                    if st.button("Submit Feedback"):
                        with open("feedback_log.txt", "a") as fb:
                            fb.write(f"\nRole: {selected}\nQuestion: {question}\nRating: {rating}\nFeedback: {feedback}\n---\n")
                        st.success("✅ Feedback submitted. Thank you!")

if "chunks" in st.session_state:
    st.markdown("## 📥Download Extracted Chunks(If Needed)")
    if st.button("Download Chunks"):
        joined_chunks = "\n\n".join(st.session_state.chunks)
        b64 = base64.b64encode(joined_chunks.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="chunks.txt">📄 Click here to download chunks</a>'
        st.markdown(href, unsafe_allow_html=True)

st.markdown("""
<div class='footer'>
    💡 Built using Gemini 2.5, LangChain & Streamlit | CopyRights @Lokeshwari Reserved 2025
</div>
""", unsafe_allow_html=True)
