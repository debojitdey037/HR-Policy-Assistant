"""
HR Policy Assistant — Enso Group RAG Chatbot
Web Application built with Streamlit, LangChain, ChromaDB & Google Gemini.
Supports both Light Mode (exact replica of high-fidelity mockup) and Dark Mode.
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
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize Session State
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

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


def render_html(html_str: str):
    """Render HTML safely without markdown code-block triggers."""
    clean_html = "\n".join(line.strip() for line in html_str.splitlines() if line.strip())
    st.markdown(clean_html, unsafe_allow_html=True)


is_dark = st.session_state.dark_mode

# Theme variables
if is_dark:
    app_bg = "radial-gradient(circle at 10% 12%, #0F172A 0%, #070B14 45%, #0B1120 100%)"
    text_main = "#F8FAFC"
    card_bg = "#111A2E"
    card_border = "#1E293B"
    card_shadow = "0 15px 35px rgba(0, 0, 0, 0.5), 0 0 25px rgba(59, 130, 246, 0.08)"
    header_border = "#1E293B"
    title_color = "#F8FAFC"
    subtitle_color = "#94A3B8"
    enso_title = "#F8FAFC"
    enso_sub = "#64748B"
    enso_stroke = "#F8FAFC"
    enso_dot = "#38BDF8"
    feature_icon = "#38BDF8"
    feature_text = "#E2E8F0"
    user_bubble_bg = "#1E3A8A"
    user_bubble_text = "#DBEAFE"
    user_avatar_bg = "#1E293B"
    user_avatar_icon = "#60A5FA"
    bot_avatar_bg = "#1E293B"
    bot_avatar_border = "#334155"
    bot_avatar_icon = "#60A5FA"
    bot_text = "#F1F5F9"
    ref_subcard_bg = "#0B132B"
    ref_subcard_border = "#1E2D4A"
    ref_title = "#60A5FA"
    ref_page = "#93C5FD"
    ref_divider = "#1E293B"
    excerpt_heading = "#60A5FA"
    excerpt_text = "#CBD5E1"
    not_found_bg = "#450A0A"
    not_found_border = "#7F1D1D"
    not_found_text = "#FCA5A5"
    input_bg = "#0F172A"
    input_border = "#334155"
    input_text = "#F8FAFC"
    disclaimer_color = "#64748B"
    footer_color = "#94A3B8"
    toggle_bg = "#1E293B"
    toggle_border = "#334155"
    toggle_color = "#F8FAFC"
else:
    app_bg = "radial-gradient(circle at 10% 12%, #E4EFF9 0%, #F5F8FC 45%, #EBF1F9 100%)"
    text_main = "#1E293B"
    card_bg = "#FFFFFF"
    card_border = "#E2E8F0"
    card_shadow = "0 10px 30px rgba(15, 43, 72, 0.05), 0 2px 6px rgba(0, 0, 0, 0.02)"
    header_border = "#F1F5F9"
    title_color = "#0F2B48"
    subtitle_color = "#475569"
    enso_title = "#0B2545"
    enso_sub = "#475569"
    enso_stroke = "#0F2B48"
    enso_dot = "#3B82F6"
    feature_icon = "#2563EB"
    feature_text = "#1E293B"
    user_bubble_bg = "#E0ECFF"
    user_bubble_text = "#1E3A8A"
    user_avatar_bg = "#DBEAFE"
    user_avatar_icon = "#2563EB"
    bot_avatar_bg = "#EFF6FF"
    bot_avatar_border = "#DBEAFE"
    bot_avatar_icon = "#2563EB"
    bot_text = "#1E293B"
    ref_subcard_bg = "#F1F6FC"
    ref_subcard_border = "#E2EBF6"
    ref_title = "#1E40AF"
    ref_page = "#1E3A8A"
    ref_divider = "#E2E8F0"
    excerpt_heading = "#1E40AF"
    excerpt_text = "#334155"
    not_found_bg = "#FEF2F2"
    not_found_border = "#FEE2E2"
    not_found_text = "#991B1B"
    input_bg = "#FFFFFF"
    input_border = "#E2E8F0"
    input_text = "#1E293B"
    disclaimer_color = "#94A3B8"
    footer_color = "#475569"
    toggle_bg = "#FFFFFF"
    toggle_border = "#CBD5E1"
    toggle_color = "#0F2B48"

# Dynamic Styling
render_html(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

    .stApp {{
        background: {app_bg} !important;
        color: {text_main} !important;
    }}

    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1220px !important;
    }}

    header[data-testid="stHeader"], 
    [data-testid="stToolbar"], 
    [data-testid="stAppDeployButton"], 
    #MainMenu, 
    footer {{
        display: none !important;
        visibility: hidden !important;
    }}

    /* Floating Theme Switch in Top-Right Corner */
    div[data-testid="stElementContainer"]:has(button[data-testid="stBaseButton-secondary"]) {{
        position: fixed !important;
        top: 24px !important;
        right: 32px !important;
        z-index: 999999 !important;
        width: auto !important;
    }}

    button[data-testid="stBaseButton-secondary"] {{
        background: {toggle_bg} !important;
        border: 1px solid {toggle_border} !important;
        color: {toggle_color} !important;
        border-radius: 20px !important;
        padding: 8px 18px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12) !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }}

    button[data-testid="stBaseButton-secondary"] p {{
        color: {toggle_color} !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        margin: 0 !important;
    }}

    button[data-testid="stBaseButton-secondary"]:hover {{
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.18) !important;
    }}

    /* LEFT COLUMN */
    .brand-wrap {{
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 2.5rem;
    }}

    .enso-logo-title {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: {enso_title};
        font-size: 1.85rem;
        font-weight: 700;
        line-height: 1;
        letter-spacing: -0.02em;
    }}

    .enso-logo-subtitle {{
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.22em;
        color: {enso_sub};
        margin-top: 3px;
    }}

    .main-title {{
        font-size: 3.1rem;
        font-weight: 800;
        line-height: 1.12;
        color: {title_color};
        letter-spacing: -0.035em;
        margin-bottom: 1.35rem;
    }}

    .subtitle-desc {{
        font-size: 1.05rem;
        line-height: 1.55;
        color: {subtitle_color};
        font-weight: 400;
        margin-bottom: 2.5rem;
        max-width: 360px;
    }}

    .feature-item {{
        display: flex;
        align-items: center;
        gap: 18px;
        margin-bottom: 1.6rem;
    }}

    .feature-icon-box {{
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}

    .feature-text {{
        font-size: 0.96rem;
        font-weight: 600;
        color: {feature_text};
        line-height: 1.25;
    }}

    /* RIGHT COLUMN CHAT CARD */
    [data-testid="stHorizontalBlock"]:not([data-testid="stForm"] *) > [data-testid="stColumn"]:nth-of-type(2) {{
        background: {card_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 24px !important;
        box-shadow: {card_shadow} !important;
        padding: 26px 32px 24px 32px !important;
        min-height: 560px !important;
    }}

    [data-testid="stForm"] [data-testid="stColumn"] {{
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        min-height: unset !important;
        padding: 0 !important;
    }}

    .chat-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 18px;
        border-bottom: 1px solid {header_border};
        margin-bottom: 22px;
        width: 100%;
    }}

    .chat-header-title {{
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.18rem;
        font-weight: 700;
        color: {title_color};
    }}

    .chat-header-status {{
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.85rem;
        font-weight: 500;
        color: {subtitle_color};
    }}

    .status-dot-green {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10B981;
        display: inline-block;
    }}

    .chat-messages-container {{
        display: flex;
        flex-direction: column;
        gap: 20px;
        margin-bottom: 22px;
        width: 100%;
    }}

    .user-msg-row {{
        display: flex;
        justify-content: flex-end;
        align-items: flex-start;
        gap: 12px;
        width: 100%;
    }}

    .user-bubble {{
        background: {user_bubble_bg};
        color: {user_bubble_text};
        border-radius: 16px 16px 4px 16px;
        padding: 13px 18px;
        font-size: 0.94rem;
        line-height: 1.48;
        font-weight: 500;
        max-width: 82%;
    }}

    .avatar-user {{
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: {user_avatar_bg};
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}

    .bot-msg-row {{
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        gap: 12px;
        width: 100%;
    }}

    .avatar-bot {{
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: {bot_avatar_bg};
        border: 1px solid {bot_avatar_border};
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}

    .bot-content-wrap {{
        display: flex;
        flex-direction: column;
        gap: 10px;
        max-width: 88%;
    }}

    .bot-answer-text {{
        font-size: 0.96rem;
        line-height: 1.55;
        color: {bot_text};
        font-weight: 400;
    }}

    .reference-subcard {{
        background: {ref_subcard_bg};
        border: 1px solid {ref_subcard_border};
        border-radius: 14px;
        padding: 13px 16px;
    }}

    .reference-title-line {{
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.84rem;
        font-weight: 700;
        color: {ref_title};
        margin-bottom: 2px;
    }}

    .reference-page-text {{
        font-size: 0.86rem;
        color: {ref_page};
        font-weight: 500;
        margin-bottom: 8px;
    }}

    .reference-divider {{
        height: 1px;
        background-color: {ref_divider};
        margin: 6px 0 8px 0;
    }}

    .source-excerpt-heading {{
        font-size: 0.82rem;
        font-weight: 700;
        color: {excerpt_heading};
        margin-bottom: 2px;
    }}

    .source-excerpt-text {{
        font-size: 0.85rem;
        font-style: italic;
        color: {excerpt_text};
        line-height: 1.45;
    }}

    .not-found-bubble {{
        background: {not_found_bg};
        border: 1px solid {not_found_border};
        border-radius: 12px;
        padding: 12px 18px;
        font-size: 1.02rem;
        font-weight: 700;
        color: {not_found_text};
    }}

    div[data-testid="stForm"] {{
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin-top: 10px !important;
    }}

    div[data-testid="stTextInput"] input {{
        background: {input_bg} !important;
        color: {input_text} !important;
        border: 1.5px solid {input_border} !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
        height: 48px !important;
    }}

    div[data-testid="stTextInput"] input:focus {{
        border-color: #2563EB !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
    }}

    div[data-testid="stFormSubmitButton"] > button {{
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
    }}

    div[data-testid="stFormSubmitButton"] > button p {{
        color: #FFFFFF !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        margin: 0 !important;
    }}

    div[data-testid="stFormSubmitButton"] > button:hover {{
        background: #1D4ED8 !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35) !important;
    }}

    .disclaimer-caption {{
        font-size: 0.78rem;
        color: {disclaimer_color};
        display: flex;
        align-items: center;
        gap: 5px;
        margin-top: 8px;
    }}

    .site-footer {{
        text-align: center;
        margin-top: 3.5rem;
        padding-top: 1.5rem;
        font-size: 0.95rem;
        font-weight: 500;
        color: {footer_color};
        letter-spacing: 0.01em;
    }}

    .site-footer span.heart {{
        color: #EF4444;
        display: inline-block;
        margin: 0 4px;
        font-size: 1.1rem;
    }}
    </style>
    """
)

# Floating Theme Switch
btn_label = "☀️ Light Mode" if is_dark else "🌙 Dark Mode"
if st.button(btn_label, key="theme_toggle_btn"):
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()

# Layout Columns
left_col, right_col = st.columns([0.38, 0.62], gap="large")

# LEFT COLUMN: Branding & Features
with left_col:
    render_html(
        f"""
        <div class="brand-wrap">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <circle cx="24" cy="24" r="17" stroke="{enso_stroke}" stroke-width="7" stroke-dasharray="84 25" stroke-linecap="round"/>
                <circle cx="35" cy="13" r="3.5" fill="{enso_dot}"/>
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
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="{feature_icon}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    <path d="m9 12 2 2 4-4"/>
                </svg>
            </div>
            <div class="feature-text">Accurate<br>Information</div>
        </div>

        <div class="feature-item">
            <div class="feature-icon-box">
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="{feature_icon}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/>
                    <path d="M6 2v20"/>
                </svg>
            </div>
            <div class="feature-text">Direct from<br>HR Manual</div>
        </div>

        <div class="feature-item">
            <div class="feature-icon-box">
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="{feature_icon}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
        f"""
        <div class="chat-header">
            <div class="chat-header-title">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{title_color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                    <circle cx="9" cy="10" r="1" fill="{title_color}"/>
                    <circle cx="15" cy="10" r="1" fill="{title_color}"/>
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
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="{user_avatar_icon}">
                            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                        </svg>
                    </div>
                </div>
                """
            )

        # Bot Message
        if not is_found or ans.strip().lower() == "not found":
            render_html(
                f"""
                <div class="bot-msg-row">
                    <div class="avatar-bot">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{bot_avatar_icon}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{bot_avatar_icon}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
                                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="{ref_title}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
