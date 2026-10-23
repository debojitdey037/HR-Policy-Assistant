"""
HR Policy Assistant — Enso Group RAG Chatbot
Web Application built with Streamlit, LangChain, ChromaDB & Google Gemini.
Exact replica of the high-fidelity UI mockup.
"""

import sys
import textwrap
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
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def render_html(html_str: str):
    """Render HTML safely without markdown code-block triggers."""
    clean_html = "\n".join(line.strip() for line in html_str.splitlines() if line.strip())
    st.markdown(clean_html, unsafe_allow_html=True)


# Custom High-Fidelity CSS matching user's exact mockup
render_html(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Soft Pastel Blue Gradient Background */
    .stApp {
        background: radial-gradient(circle at 10% 12%, #E4EFF9 0%, #F5F8FC 45%, #EBF1F9 100%) !important;
        color: #1E293B !important;
    }

    /* Container constraints */
    .block-container {
        padding-top: 3.2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1220px !important;
    }

    /* Hide default Streamlit headers, menus, deploy button and footers */
    header[data-testid="stHeader"], 
    [data-testid="stToolbar"], 
    [data-testid="stAppDeployButton"], 
    #MainMenu, 
    footer {
        display: none !important;
        visibility: hidden !important;
    }

    /* LEFT COLUMN STYLING */
    .brand-wrap {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 2.5rem;
    }

    .enso-logo-title {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #0B2545;
        font-size: 1.85rem;
        font-weight: 700;
        line-height: 1;
        letter-spacing: -0.02em;
    }

    .enso-logo-subtitle {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.22em;
        color: #475569;
        margin-top: 3px;
    }

    .main-title {
        font-size: 3.1rem;
        font-weight: 800;
        line-height: 1.12;
        color: #0F2B48;
        letter-spacing: -0.035em;
        margin-bottom: 1.35rem;
    }

    .subtitle-desc {
        font-size: 1.05rem;
        line-height: 1.55;
        color: #475569;
        font-weight: 400;
        margin-bottom: 2.5rem;
        max-width: 360px;
    }

    .feature-item {
        display: flex;
        align-items: center;
        gap: 18px;
        margin-bottom: 1.6rem;
    }

    .feature-icon-box {
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    .feature-text {
        font-size: 0.96rem;
        font-weight: 600;
        color: #1E293B;
        line-height: 1.25;
    }

    /* RIGHT COLUMN STYLING (TARGET TOP-LEVEL COLUMN ONLY) */
    [data-testid="stHorizontalBlock"]:not([data-testid="stForm"] *) > [data-testid="stColumn"]:nth-of-type(2) {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 24px !important;
        box-shadow: 0 10px 30px rgba(15, 43, 72, 0.05), 0 2px 6px rgba(0, 0, 0, 0.02) !important;
        padding: 26px 32px 24px 32px !important;
        min-height: 560px !important;
    }

    /* RESET NESTED FORM COLUMNS */
    [data-testid="stForm"] [data-testid="stColumn"] {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        min-height: unset !important;
        padding: 0 !important;
    }

    .chat-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 18px;
        border-bottom: 1px solid #F1F5F9;
        margin-bottom: 22px;
        width: 100%;
    }

    .chat-header-title {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.18rem;
        font-weight: 700;
        color: #0F2B48;
    }

    .chat-header-status {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #475569;
    }

    .status-dot-green {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10B981;
        display: inline-block;
    }

    /* CHAT MESSAGES CONTAINER */
    .chat-messages-container {
        display: flex;
        flex-direction: column;
        gap: 20px;
        margin-bottom: 22px;
        width: 100%;
    }

    /* User Message Bubble */
    .user-msg-row {
        display: flex;
        justify-content: flex-end;
        align-items: flex-start;
        gap: 12px;
        width: 100%;
    }

    .user-bubble {
        background: #E0ECFF;
        color: #1E3A8A;
        border-radius: 16px 16px 4px 16px;
        padding: 13px 18px;
        font-size: 0.94rem;
        line-height: 1.48;
        font-weight: 500;
        max-width: 82%;
    }

    .avatar-user {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #DBEAFE;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    /* Bot Message Bubble */
    .bot-msg-row {
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        gap: 12px;
        width: 100%;
    }

    .avatar-bot {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #EFF6FF;
        border: 1px solid #DBEAFE;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    .bot-content-wrap {
        display: flex;
        flex-direction: column;
        gap: 10px;
        max-width: 88%;
    }

    .bot-answer-text {
        font-size: 0.96rem;
        line-height: 1.55;
        color: #1E293B;
        font-weight: 400;
    }

    /* Nested Reference Card */
    .reference-subcard {
        background: #F1F6FC;
        border: 1px solid #E2EBF6;
        border-radius: 14px;
        padding: 13px 16px;
    }

    .reference-title-line {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.84rem;
        font-weight: 700;
        color: #1E40AF;
        margin-bottom: 2px;
    }

    .reference-page-text {
        font-size: 0.86rem;
        color: #1E3A8A;
        font-weight: 500;
        margin-bottom: 8px;
    }

    .reference-divider {
        height: 1px;
        background-color: #E2E8F0;
        margin: 6px 0 8px 0;
    }

    .source-excerpt-heading {
        font-size: 0.82rem;
        font-weight: 700;
        color: #1E40AF;
        margin-bottom: 2px;
    }

    .source-excerpt-text {
        font-size: 0.85rem;
        font-style: italic;
        color: #334155;
        line-height: 1.45;
    }

    /* Strict Not Found Bubble */
    .not-found-bubble {
        background: #FEF2F2;
        border: 1px solid #FEE2E2;
        border-radius: 12px;
        padding: 12px 18px;
        font-size: 1.02rem;
        font-weight: 700;
        color: #991B1B;
    }

    /* Form and Inputs */
    div[data-testid="stForm"] {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin-top: 10px !important;
    }

    div[data-testid="stTextInput"] input {
        background: #FFFFFF !important;
        color: #1E293B !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
        height: 48px !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
    }

    /* Send Button */
    div[data-testid="stFormSubmitButton"] > button {
        background: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        height: 48px !important;
        padding: 0 20px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
    }

    div[data-testid="stFormSubmitButton"] > button p {
        color: #FFFFFF !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        margin: 0 !important;
    }

    div[data-testid="stFormSubmitButton"] > button:hover {
        background: #1D4ED8 !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35) !important;
    }

    .disclaimer-caption {
        font-size: 0.78rem;
        color: #94A3B8;
        display: flex;
        align-items: center;
        gap: 5px;
        margin-top: 8px;
    }

    /* SITE FOOTER */
    .site-footer {
        text-align: center;
        margin-top: 3.5rem;
        padding-top: 1.5rem;
        font-size: 0.95rem;
        font-weight: 500;
        color: #475569;
        letter-spacing: 0.01em;
    }

    .site-footer span.heart {
        color: #EF4444;
        display: inline-block;
        margin: 0 4px;
        font-size: 1.1rem;
    }
    </style>
    """,
)

# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "query": "How many days of Privilege Leave (PL) does a permanent employee get per year?",
            "answer": "Permanent employees are entitled to 12 days of Privilege Leave (PL) per year.",
            "reference": "Page 60 – Leave Policy (Section: Privilege Leave)",
            "excerpt": "Permanent employees are eligible for 12 days of Privilege Leave (PL) per year.",
            "is_found": True,
        }
    ]

# Layout Columns
left_col, right_col = st.columns([0.38, 0.62], gap="large")

# LEFT COLUMN: Branding & Features
with left_col:
    render_html(
        """
        <div class="brand-wrap">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <circle cx="24" cy="24" r="17" stroke="#0F2B48" stroke-width="7" stroke-dasharray="84 25" stroke-linecap="round"/>
                <circle cx="35" cy="13" r="3.5" fill="#3B82F6"/>
            </svg>
            <div>
                <div class="enso-logo-title">Enso</div>
                <div class="enso-logo-subtitle">GROUP</div>
            </div>
        </div>

        <div class="main-title">
            HR Policy<br>Assistant
        </div>

        <div class="subtitle-desc">
            Get quick answers to your HR policy questions from the Enso Group HR Manual.
        </div>

        <div class="feature-item">
            <div class="feature-icon-box">
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    <path d="m9 12 2 2 4-4"/>
                </svg>
            </div>
            <div class="feature-text">Accurate<br>Information</div>
        </div>

        <div class="feature-item">
            <div class="feature-icon-box">
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/>
                    <path d="M6 2v20"/>
                </svg>
            </div>
            <div class="feature-text">Direct from<br>HR Manual</div>
        </div>

        <div class="feature-item">
            <div class="feature-icon-box">
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
                </svg>
            </div>
            <div class="feature-text">Fast & Easy<br>Access</div>
        </div>
        """
    )

# RIGHT COLUMN: Chat Card
with right_col:
    # 1. Header
    render_html(
        """
        <div class="chat-header">
            <div class="chat-header-title">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0F2B48" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                    <circle cx="9" cy="10" r="1" fill="#0F2B48"/>
                    <circle cx="15" cy="10" r="1" fill="#0F2B48"/>
                </svg>
                <span>HR Policy Assistant</span>
            </div>
            <div class="chat-header-status">
                <span class="status-dot-green"></span>
                <span>Connected to HR Manual</span>
            </div>
        </div>
        """
    )

    # 2. Messages Display
    for item in st.session_state.chat_history:
        q = item.get("query", "")
        ans = item.get("answer", "")
        ref = item.get("reference", "")
        excerpt = item.get("excerpt", "")
        is_found = item.get("is_found", True)

        # User Message
        if q:
            render_html(
                f"""
                <div class="user-msg-row">
                    <div class="user-bubble">{q}</div>
                    <div class="avatar-user">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="#2563EB">
                            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                        </svg>
                    </div>
                </div>
                """
            )

        # Bot Message
        if not is_found or ans.strip().lower() == "not found":
            render_html(
                """
                <div class="bot-msg-row">
                    <div class="avatar-bot">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="11" width="18" height="10" rx="2"/>
                            <circle cx="12" cy="5" r="2"/>
                            <path d="M12 7v4"/>
                            <line x1="8" y1="16" x2="8.01" y2="16"/>
                            <line x1="16" y1="16" x2="16.01" y2="16"/>
                        </svg>
                    </div>
                    <div class="not-found-bubble">Not found</div>
                </div>
                """
            )
        else:
            excerpt_html = ""
            if excerpt:
                excerpt_html = f"""
                <div class="reference-divider"></div>
                <div class="source-excerpt-heading">Source Excerpt:</div>
                <div class="source-excerpt-text">&ldquo;{excerpt}&rdquo;</div>
                """

            render_html(
                f"""
                <div class="bot-msg-row">
                    <div class="avatar-bot">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="11" width="18" height="10" rx="2"/>
                            <circle cx="12" cy="5" r="2"/>
                            <path d="M12 7v4"/>
                            <line x1="8" y1="16" x2="8.01" y2="16"/>
                            <line x1="16" y1="16" x2="16.01" y2="16"/>
                        </svg>
                    </div>
                    <div class="bot-content-wrap">
                        <div class="bot-answer-text">{ans}</div>
                        <div class="reference-subcard">
                            <div class="reference-title-line">
                                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#1E40AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                    <polyline points="14 2 14 8 20 8"/>
                                </svg>
                                <span>Reference:</span>
                            </div>
                            <div class="reference-page-text">{ref}</div>
                            {excerpt_html}
                        </div>
                    </div>
                </div>
                """
            )

    # 3. Input Form
    with st.form("input_chat_form", clear_on_submit=True):
        input_col, send_col = st.columns([0.82, 0.18], gap="small")
        with input_col:
            user_input = st.text_input(
                "Type your question here...",
                placeholder="Type your question here...",
                label_visibility="collapsed",
            )
        with send_col:
            send_btn = st.form_submit_button("✈ Send", use_container_width=True)

    # 4. Disclaimer
    render_html(
        """
        <div class="disclaimer-caption">
            <span>ⓘ</span>
            <span>Answers are based only on the Enso Group HR Manual.</span>
        </div>
        """
    )

# SITE FOOTER
render_html(
    """
    <div class="site-footer">
        Made with <span class="heart">❤️</span> by Debojit
    </div>
    """
)

# Handle Submission
if send_btn and user_input and user_input.strip():
    with st.spinner(""):
        res = query_hr_assistant(user_input.strip())
        top_excerpt = ""
        if res.get("sources"):
            top_excerpt = res["sources"][0].get("content", "")[:220].strip()

        st.session_state.chat_history.append(
            {
                "query": user_input.strip(),
                "answer": res["answer"],
                "reference": res["reference"],
                "excerpt": top_excerpt,
                "is_found": res["is_found"],
            }
        )
        st.rerun()
