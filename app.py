"""
Streamlit Web Application: HR Policy Assistant — RAG Chatbot.

Provides a clean, responsive, and intuitive web UI for employees and evaluators
to query the Enso Group HR Policy Manual with exact source citations and strict
hallucination controls.
"""

import sys
from pathlib import Path
import streamlit as st

# Setup paths
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import config
from rag_pipeline import query_hr_assistant

# Page Configuration
st.set_page_config(
    page_title="HR Policy Assistant — Enso Group",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    /* Main container styling */
    .main-header {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #1E293B;
        margin-bottom: 0.25rem;
    }
    .sub-header {
        color: #64748B;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .answer-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.25rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .not-found-badge {
        display: inline-block;
        background-color: #FEE2E2;
        color: #991B1B;
        font-weight: 600;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.95rem;
    }
    .found-badge {
        display: inline-block;
        background-color: #DCFCE7;
        color: #166534;
        font-weight: 600;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.95rem;
    }
    .reference-box {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        padding: 0.75rem 1rem;
        border-radius: 4px;
        margin-top: 0.75rem;
    }
    .excerpt-box {
        font-family: monospace;
        font-size: 0.88rem;
        background: #F1F5F9;
        border-radius: 6px;
        padding: 0.75rem;
        white-space: pre-wrap;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Session State
if "history" not in st.session_state:
    st.session_state.history = []
if "current_response" not in st.session_state:
    st.session_state.current_response = None
if "input_question" not in st.session_state:
    st.session_state.input_question = ""


def set_question(sample_q: str):
    """Callback for sample question buttons."""
    st.session_state.input_question = sample_q
    st.session_state.query_input_field = sample_q


def clear_query():
    """Reset question and response state."""
    st.session_state.input_question = ""
    st.session_state.query_input_field = ""
    st.session_state.current_response = None


# Sidebar
with st.sidebar:
    st.title("📋 Project Information")
    st.markdown("### HR Policy Assistant")
    st.caption("College Midterm Project — RAG Chatbot")

    st.markdown("---")
    st.markdown("#### 🛠️ Technology Stack")
    st.markdown(
        """
        - **LLM Engine:** Google Gemini (`gemini-3.5-flash`)
        - **Embeddings:** Gemini (`models/gemini-embedding-001`)
        - **Framework:** LangChain (LCEL Runnable Pipeline)
        - **Vector Database:** ChromaDB (Persistent)
        - **PDF Parser:** PyMuPDF (`fitz`)
        - **Interface:** Streamlit
        - **Environment:** python-dotenv
        """
    )

    st.markdown("---")
    st.markdown("#### 📄 Document Status")
    if config.PDF_PATH.exists():
        st.success(f"✅ Document loaded: `{config.PDF_PATH.name}` (79 pages)")
    else:
        st.error("❌ `hr_manual.pdf` is missing from `data/`")

    st.markdown("#### 🔑 API Key Status")
    if config.validate_api_key():
        st.success("✅ Gemini API Key configured securely")
    else:
        st.error("❌ Gemini API Key missing or placeholder in `.env`")

    st.markdown("#### 🗄️ Vector Store")
    if config.CHROMA_DIR.exists() and any(config.CHROMA_DIR.iterdir()):
        st.success("✅ ChromaDB collection ready")
    else:
        st.warning("⚠️ ChromaDB not yet built. Run `python ingest.py`")

    st.markdown("---")
    st.markdown(
        """
        **Grounding Rule:** If an answer cannot be supported by the official manual, the assistant responds with exactly `Not found`.
        """
    )


# Main Content Area
st.markdown("<h1 class='main-header'>🏢 HR Policy Assistant</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='sub-header'>Ask questions about company leaves, probation, benefits, and workplace guidelines based on the <b>Enso Group HR Policy Manual</b>.</p>",
    unsafe_allow_html=True,
)

# Prerequisites Validation Banner
if not config.validate_api_key():
    st.error(
        "⚠️ **Missing API Key:** Please set your valid `GEMINI_API_KEY` in the `.env` file before querying the assistant."
    )
    st.stop()

if not config.PDF_PATH.exists():
    st.error(
        "⚠️ **Missing Document:** `hr_manual.pdf` was not found in the `data/` directory. Please add the PDF to proceed."
    )
    st.stop()

if not config.CHROMA_DIR.exists():
    st.warning(
        "⚠️ **Database Required:** Vector database is not initialized. Please run `python ingest.py` in your terminal."
    )
    st.stop()

# Sample Questions (LMS Demo Buttons)
st.markdown("##### 💡 Try LMS Evaluation Questions:")
col1, col2, col3 = st.columns(3)
with col1:
    st.button(
        "1. Privilege Leave Days",
        on_click=set_question,
        args=("How many days of Privilege Leave (PL) does a permanent employee get per year?",),
        use_container_width=True,
    )
    st.button(
        "2. Probation Period",
        on_click=set_question,
        args=("What is the probation period for employees up to Senior Manager?",),
        use_container_width=True,
    )
with col2:
    st.button(
        "3. Health-Insurance Premium",
        on_click=set_question,
        args=("What is the company's health-insurance premium amount?",),
        use_container_width=True,
    )
    st.button(
        "4. India GST Rate",
        on_click=set_question,
        args=("What is the current GST rate in India?",),
        use_container_width=True,
    )
with col3:
    st.button(
        "5. Maternity Leave Days",
        on_click=set_question,
        args=("How many days of maternity leave are given?",),
        use_container_width=True,
    )

st.markdown("")

# User Question Form
with st.form("qa_form", clear_on_submit=False):
    user_query = st.text_input(
        "Enter your HR policy question:",
        value=st.session_state.input_question,
        placeholder="e.g., How many days of Privilege Leave (PL) does a permanent employee get per year?",
        key="query_input_field",
    )
    btn_col1, btn_col2, _ = st.columns([1.5, 1.2, 5])
    with btn_col1:
        submit_btn = st.form_submit_button("🔍 Ask Question", use_container_width=True, type="primary")
    with btn_col2:
        clear_btn = st.form_submit_button("🗑️ Clear", use_container_width=True, on_click=clear_query)

if submit_btn and user_query.strip():
    with st.spinner("Searching HR manual and generating grounded response..."):
        response = query_hr_assistant(user_query.strip())
        st.session_state.current_response = response
        # Record in history
        st.session_state.history.append(response)

# Display Current Response
if st.session_state.current_response:
    resp = st.session_state.current_response
    st.markdown("---")
    st.markdown("### 💬 Result")

    if not resp["is_found"]:
        # Strict 'Not found' Display
        st.markdown(
            f"""
            <div class='answer-card'>
                <span class='not-found-badge'>Grounding Check: Absent from Manual</span>
                <h3 style='margin-top: 0.75rem; color: #1E293B;'>{resp['answer']}</h3>
                <p style='color: #64748B; font-size: 0.95rem; margin-top: 0.5rem;'>
                    No supporting evidence exists in the Enso Group HR Policy Manual for this question.
                    External knowledge and speculation are strictly disabled.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Verified Answer Display
        st.markdown(
            f"""
            <div class='answer-card'>
                <span class='found-badge'>Verified from HR Manual</span>
                <h4 style='margin-top: 0.75rem; color: #0F172A;'>Answer:</h4>
                <p style='font-size: 1.05rem; line-height: 1.6; color: #1E293B;'>{resp['answer']}</p>
                <div class='reference-box'>
                    <b>Reference:</b> {resp['reference']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Source Citations and Excerpts Section
        if resp.get("sources"):
            with st.expander("📚 View Supporting Document Evidence & Page Excerpts", expanded=True):
                for idx, src in enumerate(resp["sources"][:3]):
                    page_num = src.get("page", "Unknown")
                    section_title = src.get("section", "HR Manual")
                    content = src.get("content", "").strip()
                    st.markdown(f"**Source #{idx + 1}: Page {page_num} — `{section_title}`**")
                    st.markdown(f"<div class='excerpt-box'>{content}</div>", unsafe_allow_html=True)
                    st.markdown("")

# Footer
st.markdown("---")
st.markdown(
    "<center><small style='color: #94A3B8;'>HR Policy Assistant • Built with LangChain, ChromaDB & Google Gemini • College Midterm Project</small></center>",
    unsafe_allow_html=True,
)
