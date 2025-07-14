import os
import streamlit as st
from dotenv import load_dotenv
from ingest import extract_chunks
from qa import build_vector_db, get_qa_chain, evaluate_response
from prompts import get_prompt
from roles import USER_ROLES
import time
import base64
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# ---------------- Guardrails Safe Import ----------------
try:
    from guardrails_config import response_guard
    GUARDRAILS_ENABLED = True
except ImportError:
    GUARDRAILS_ENABLED = False
    class DummyGuard:
        def validate(self, val):
            return {"pass": True, "validated_output": val}
    response_guard = DummyGuard()

# ---------------- Load API Key ----------------
load_dotenv()
<<<<<<< HEAD
# Load API key from secrets or fallback to .env
api_key = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")


=======
api_key = os.getenv("GEMINI_API_KEY")
>>>>>>> f30291c (🔧 Update app.py with Guardrails, admin mode, metrics logging, and hallucination checks)

st.set_page_config(page_title="Cancer Report RAG", layout="wide")

# ---------------- UI Theme ----------------
st.markdown("""
    <style>
    .stApp { background-color: #F2F6FC; }
    .title { font-size: 40px; color: #0a1f44; font-weight: 700; margin-bottom: 20px; }
    .answer-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
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
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🧠 Cancer Report Q&A Assistant (Gemini + RAG)</div>", unsafe_allow_html=True)
st.sidebar.title("⚙️ App Options")
st.sidebar.markdown("Upload a Cancer Report PDF to begin.")

<<<<<<< HEAD
# Check for Gemini API key
# Inject into env for langchain + Gemini access
if api_key:
    os.environ["GEMINI_API_KEY"] = api_key
else:
    st.set_page_config(page_title="🧠 Cancer Report RAG", layout="wide")
    st.error("❗ Gemini API key not found. Please set it in .env (for local) or Secrets (Streamlit Cloud).")
=======
# Admin mode
ADMIN_MODE = st.sidebar.checkbox("🔐 Admin Mode")
CONF_THRESHOLD = st.sidebar.slider("Confidence Threshold (%)", 0, 100, 50) if ADMIN_MODE else 50

# ---------------- Check API Key ----------------
if not api_key:
    st.error("❗ Gemini API key not found in .env.")
>>>>>>> f30291c (🔧 Update app.py with Guardrails, admin mode, metrics logging, and hallucination checks)
    st.stop()
else:
    os.environ["GEMINI_API_KEY"] = api_key

<<<<<<< HEAD

st.markdown("## 📤Upload a Cancer Report PDF")
pdf_file = st.file_uploader("Choose your Cancer Facts PDF", type="pdf")
=======
# ---------------- Upload PDF ----------------
st.markdown("## 📤 Upload a Cancer Report PDF")
pdf_file = st.file_uploader("Choose a Cancer Facts PDF", type="pdf")
>>>>>>> f30291c (🔧 Update app.py with Guardrails, admin mode, metrics logging, and hallucination checks)

if pdf_file:
    if "chunks" not in st.session_state:
        with open("temp.pdf", "wb") as f:
            f.write(pdf_file.getbuffer())

        with st.spinner("📚 Processing PDF..."):
            chunks = extract_chunks("temp.pdf", max_chunks=50)
            vector_db = build_vector_db(chunks)
            qa_chain = get_qa_chain(vector_db)
            st.session_state.chunks = chunks
            st.session_state.vector_db = vector_db
            st.session_state.qa_chain = qa_chain

        st.success("✅ Document processed. Ask your question below!")
        st.balloons()

# ---------------- Q&A Section ----------------
if "qa_chain" in st.session_state:
    st.markdown("## 🧪 Step 2: Select Role & Ask Question")
    role_options = list(USER_ROLES.keys()) + ["Add a new role"]
    selected = st.selectbox("👤 Choose a role or add one", role_options)

    if selected == "Add a new role":
        new_role = st.text_input("Enter new role name")
        new_prompt = st.text_area("Enter prompt template for the role")
        if st.button("➕ Save Role"):
            if new_role and new_prompt:
                USER_ROLES[new_role] = new_prompt
                st.success(f"✅ Role '{new_role}' added.")
    else:
        question = st.text_input("❓ Ask a question about the report")
        if st.button("Ask Question"):
            if not question.strip():
                st.warning("Please enter a valid question.")
            elif any(word in question.lower() for word in ["kill", "suicide", "die", "murder"]):
                st.error("🚫 Your question contains sensitive keywords. Please rephrase respectfully.")
            else:
                final_prompt = get_prompt(selected, question)

                with st.spinner("🤖 Generating answer..."):
                    start_time = time.time()
                    answer = st.session_state.qa_chain.run(final_prompt)
                    duration = round(time.time() - start_time, 2)

                # Guardrails validation
                validated = response_guard.validate({"response": answer})
                if GUARDRAILS_ENABLED and not validated["pass"]:
                    st.error("⚠️ Response failed safety checks.")
                    st.stop()
                else:
                    answer = validated.get("validated_output", {}).get("response", answer)

                st.markdown(f"<div class='answer-box'><b>{selected} says:</b><br><br>{answer}</div>", unsafe_allow_html=True)
                st.success(f"✅ Answered in {duration} seconds")
                st.markdown(f"<small><i>🔁 Generated by Gemini 1.5 Flash | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i></small>", unsafe_allow_html=True)

                # ---------------- Evaluation ----------------
                metrics_dict = evaluate_response(question, answer, selected)
                if metrics_dict:
                    confidence = metrics_dict.get("Confidence Score", 0) * 100
                    if confidence < CONF_THRESHOLD:
                        st.warning(f"⚠️ Confidence Score is below threshold ({round(confidence, 2)}%). Consider revising the question.")

                    st.subheader("📊 Role-Based Evaluation Metrics")
                    labels = list(metrics_dict.keys())
                    values = [round(metrics_dict[k] * 5, 2) for k in labels if k not in ["Confidence Score", "Hallucination"]]

                    for k in labels:
                        if k not in ["Confidence Score", "Hallucination"]:
                            st.write(f"**{k}:** {round(metrics_dict[k] * 5, 2)} / 5")

                    st.write(f"🛡️ **Final Confidence Score:** `{round(confidence, 2)}%`")
                    if "Hallucination" in metrics_dict:
                        st.write(f"❗ **Hallucination Likelihood:** `{round(metrics_dict['Hallucination'] * 100, 2)}%`")

                    fig, ax = plt.subplots()
                    ax.bar([k for k in labels if k not in ["Confidence Score", "Hallucination"]],
                           values, color=plt.cm.Paired.colors[:len(values)])
                    ax.set_ylim(0, 5)
                    ax.set_ylabel("Score (out of 5)")
                    ax.set_title(f"{selected} – Evaluation")
                    st.pyplot(fig)
                else:
                    st.warning("⚠️ Could not evaluate response metrics.")

                # ---------------- Flagging & Feedback ----------------
                with st.expander("📣 Submit Feedback (Optional)"):
                    feedback = st.text_area("📝 Your feedback")
                    rating = st.slider("⭐ Helpfulness Rating", 1, 5, 3)
                    if st.button("Submit Feedback"):
                        st.success("✅ Thank you for your feedback!")

                with st.expander("🚩 Flag this Response"):
                    if st.button("Flag as Inappropriate or Incorrect"):
                        os.makedirs("logs", exist_ok=True)
                        with open("logs/flagged_responses.csv", "a", encoding="utf-8") as f:
                            f.write(f'"{question}","{answer}","{selected}","{confidence}"\n')
                        st.success("✅ Flag submitted to moderators.")

                with st.expander("📂 View Retrieved Chunks"):
                    docs = st.session_state.qa_chain.retriever.get_relevant_documents(question)
                    for i, doc in enumerate(docs):
                        st.markdown(f"<div class='answer-box'><b>Chunk {i+1}:</b><br>{doc.page_content[:300]}...</div>", unsafe_allow_html=True)

# ---------------- Download Chunks ----------------
if "chunks" in st.session_state:
    st.markdown("## 📥 Download Extracted Chunks")
    if st.button("Download Chunks"):
        joined_chunks = "\n\n".join(st.session_state.chunks)
        b64 = base64.b64encode(joined_chunks.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="chunks.txt">📄 Download chunks.txt</a>'
        st.markdown(href, unsafe_allow_html=True)

# ---------------- Footer ----------------
st.markdown("""
<div class='footer'>
    💡 Built with ❤️ using Gemini 1.5, LangChain & Streamlit | Project by Lokeshwari
</div>
""", unsafe_allow_html=True)
