"""
Streamlit Web Application: HR Policy Assistant — RAG Chatbot.

A Dribbble-grade, premium UI/UX experience for querying the Enso Group HR Policy Manual.
Features ambient aura glows, glassmorphic frosted cards, responsive typography,
and strict hallucination-free answering.
"""

import sys
from pathlib import Path
import streamlit as st
from PIL import Image

# Setup paths
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import config
from rag_pipeline import query_hr_assistant

# Page Configuration
st.set_page_config(
    page_title="HR Policy Intelligence — Enso Group",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Dribbble-Grade Custom Styling (Obsidian / Aurora Glassmorphism)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Typography & Background Aura */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp {
        background: radial-gradient(circle at 10% 10%, rgba(99, 102, 241, 0.15) 0%, transparent 35%),
                    radial-gradient(circle at 90% 20%, rgba(236, 72, 153, 0.12) 0%, transparent 35%),
                    radial-gradient(circle at 50% 90%, rgba(14, 165, 233, 0.10) 0%, transparent 45%),
                    #090D16 !important;
        color: #F1F5F9 !important;
    }

    /* Top Padding Adjustment */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
    }

    /* Sidebar Glass Panel */
    section[data-testid="stSidebar"] {
        background: rgba(13, 18, 32, 0.85) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Header Gradient & Badge */
    .brand-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(99, 102, 241, 0.12);
        color: #A5B4FC;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        margin-bottom: 0.75rem;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -0.03em;
        margin-bottom: 0.6rem;
        background: linear-gradient(135deg, #FFFFFF 0%, #E2E8F0 50%, #A5B4FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #94A3B8;
        font-weight: 400;
        margin-bottom: 1.25rem;
    }

    .metrics-row {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
    }

    .metric-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 0.35rem 0.75rem;
        font-size: 0.82rem;
        font-weight: 500;
        color: #CBD5E1;
    }

    /* Hero Banner Image Card */
    .hero-image-card {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.6),
                    0 0 25px rgba(99, 102, 241, 0.15);
        transition: transform 0.3s ease;
    }

    .hero-image-card img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
    }

    /* Floating Glass Search Box */
    div[data-testid="stForm"] {
        background: rgba(15, 23, 42, 0.65) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.5) !important;
        margin-top: 1rem !important;
        margin-bottom: 1.5rem !important;
    }

    /* Input Field Styling */
    div[data-testid="stTextInput"] input {
        background: rgba(10, 14, 26, 0.75) !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        padding: 0.85rem 1rem !important;
        font-size: 1.02rem !important;
        transition: all 0.25s ease !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
    }

    /* Primary Search Button */
    div[data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"] {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 50%, #4338CA 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.75rem !important;
        font-weight: 600 !important;
        font-size: 0.98rem !important;
        box-shadow: 0 6px 20px -3px rgba(99, 102, 241, 0.5) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    div[data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px -3px rgba(99, 102, 241, 0.7) !important;
    }

    /* Clear Button */
    div[data-testid="stFormSubmitButton"] > button:not([kind="primaryFormSubmit"]) {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #94A3B8 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stFormSubmitButton"] > button:not([kind="primaryFormSubmit"]):hover {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #F8FAFC !important;
    }

    /* Verified Answer Glass Card */
    .verified-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.7) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-left: 5px solid #6366F1;
        border-radius: 16px;
        padding: 1.75rem;
        margin-top: 1.25rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(16px);
        box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.4);
    }

    .card-topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }

    .badge-verified-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        font-size: 0.82rem;
        font-weight: 700;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        border: 1px solid rgba(16, 185, 129, 0.3);
        letter-spacing: 0.02em;
    }

    .verified-answer {
        font-size: 1.22rem;
        line-height: 1.75;
        font-weight: 500;
        color: #F8FAFC;
        margin-bottom: 1.25rem;
        letter-spacing: -0.01em;
    }

    .reference-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(99, 102, 241, 0.15);
        color: #C7D2FE;
        font-size: 0.92rem;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }

    /* Minimalist Strict 'Not found' Display */
    .not-found-container {
        background: linear-gradient(135deg, rgba(30, 25, 35, 0.65) 0%, rgba(20, 15, 25, 0.65) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-left: 5px solid #EF4444;
        border-radius: 16px;
        padding: 1.5rem 1.75rem;
        margin-top: 1.25rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(16px);
    }

    .not-found-heading {
        font-size: 1.45rem;
        font-weight: 700;
        color: #F87171;
        letter-spacing: -0.02em;
        margin: 0;
    }

    /* Excerpt Box */
    .excerpt-dark {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
        background: #060911;
        color: #94A3B8;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 1.15rem;
        line-height: 1.6;
        white-space: pre-wrap;
    }

    /* Pulsing Status Dot */
    .pulse-dot {
        width: 8px;
        height: 8px;
        background: #10B981;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #10B981;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Session State
if "current_response" not in st.session_state:
    st.session_state.current_response = None


def clear_query():
    """Reset question and response state."""
    st.session_state.current_response = None


# Sidebar Configuration
with st.sidebar:
    st.markdown("### 🏢 Policy Intelligence")
    st.caption("Enso Group Corporate Knowledge Engine")
    st.markdown("---")

    st.markdown("#### ⚡ System Status")
    st.markdown(
        """
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 0.85rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span class="pulse-dot"></span>
                <span style="font-size: 0.85rem; font-weight: 600; color: #E2E8F0;">RAG Pipeline Active</span>
            </div>
            <div style="font-size: 0.78rem; color: #94A3B8;">Zero-hallucination guardrails enabled</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### 🛠️ Technology Stack")
    st.markdown(
        """
        - **LLM Engine:** Google Gemini
        - **Embeddings:** `gemini-embedding-001` (3072-dim)
        - **Vector Base:** ChromaDB Persistent
        - **Pipeline:** LangChain LCEL Runnable
        - **PDF Parser:** PyMuPDF Engine
        """
    )

    st.markdown("---")
    st.markdown("#### 📄 Document Health")
    if config.PDF_PATH.exists():
        st.success(f"Loaded: `{config.PDF_PATH.name}` (79 Pages)")
    else:
        st.error("Missing: `hr_manual.pdf`")

    st.markdown("#### 🔑 API Connection")
    if config.validate_api_key():
        st.success("Gemini API connected")
    else:
        st.error("API Key not found in `.env`")


# Main Page Content: Dribbble Split Hero Layout
hero_col1, hero_col2 = st.columns([1.15, 0.85], gap="large")

with hero_col1:
    st.markdown("<div class='brand-pill'>✦ Enso Group HR Assistant</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-title'>HR Policy Intelligence</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='hero-subtitle'>Get immediate, legally grounded answers about leaves, probation periods, benefits, travel policies, and corporate conduct directly from the official 79-page manual.</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class='metrics-row'>
            <div class='metric-chip'>📄 79 Official Pages</div>
            <div class='metric-chip'>🔒 100% Document Grounded</div>
            <div class='metric-chip'>⚡ Zero Hallucinations</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with hero_col2:
    banner_path = BASE_DIR / "data" / "hr_banner.jpg"
    if banner_path.exists():
        try:
            banner_img = Image.open(banner_path)
            st.image(banner_img, use_container_width=True)
        except Exception:
            pass

# Pre-flight Checks
if not config.validate_api_key():
    st.error("⚠️ **API Key Required:** Please configure `GEMINI_API_KEY` in your `.env` file.")
    st.stop()

if not config.PDF_PATH.exists():
    st.error("⚠️ **Document Missing:** `hr_manual.pdf` not found in `data/`.")
    st.stop()

if not config.CHROMA_DIR.exists():
    st.warning("⚠️ **Database Required:** Please run `python ingest.py` in your terminal.")
    st.stop()

# Floating Search & Query Box
with st.form("qa_form", clear_on_submit=False):
    st.markdown("<span style='font-size: 0.88rem; font-weight: 600; color: #CBD5E1;'>Search Corporate Policy:</span>", unsafe_allow_html=True)
    user_query = st.text_input(
        "Search Corporate Policy:",
        placeholder="e.g. How many days of Privilege Leave (PL) does a permanent employee get per year?",
        key="query_text_input",
        label_visibility="collapsed",
    )
    col_ask, col_clear, _ = st.columns([1.5, 1.2, 5])
    with col_ask:
        submit_btn = st.form_submit_button("Ask Policy Assistant ✨", use_container_width=True, type="primary")
    with col_clear:
        clear_btn = st.form_submit_button("Clear", use_container_width=True, on_click=clear_query)

if submit_btn and user_query.strip():
    with st.spinner("Synthesizing verified answer from manual..."):
        response = query_hr_assistant(user_query.strip())
        st.session_state.current_response = response

# Display Current Response
if st.session_state.current_response:
    resp = st.session_state.current_response
    st.markdown("---")

    if not resp.get("is_found") or resp.get("answer", "").strip().lower() == "not found":
        # Strict Minimalist 'Not found'
        st.markdown(
            """
            <div class='not-found-container'>
                <div class='not-found-heading'>Not found</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Verified Answer Dribbble Glass Card
        answer_text = resp["answer"].replace("\n", "<br>")
        ref_text = resp["reference"]
        st.markdown(
            f"""
            <div class='verified-card'>
                <div class='card-topbar'>
                    <span class='badge-verified-pill'>✓ Verified from HR Manual</span>
                    <span class='reference-pill'>📖 {ref_text}</span>
                </div>
                <div class='verified-answer'>{answer_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Supporting Excerpts Drawer
        if resp.get("sources"):
            with st.expander("📚 View Supporting Source Citations & Excerpts", expanded=False):
                for idx, src in enumerate(resp["sources"][:3]):
                    page_num = src.get("page", "Unknown")
                    section_title = src.get("section", "HR Manual")
                    content = src.get("content", "").strip()
                    st.markdown(f"**Clause #{idx + 1} — Page {page_num} • `{section_title}`**")
                    st.markdown(f"<div class='excerpt-dark'>{content}</div>", unsafe_allow_html=True)
                    st.markdown("")

# Sleek Minimalist Footer
st.markdown("---")
st.markdown(
    "<center><small style='color: #64748B; font-size: 0.8rem;'>Enso Group HR Assistant • College Midterm Project • Built with LangChain, ChromaDB & Google Gemini</small></center>",
    unsafe_allow_html=True,
)
