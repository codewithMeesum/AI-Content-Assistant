import os
import time
import streamlit as st
from groq import Groq

# ----------------- Page Setup -----------------
st.set_page_config(
    page_title="Nexus | AI Content Studio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------- Clean SaaS UI / UX Styling -----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }
    
    .stApp {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }

    .block-container {
        max-width: 1240px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
    }

    /* Fixed Clean Navigation Bar */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 0 1.25rem 0;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #e2e8f0;
    }
    .brand-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        letter-spacing: -0.02em;
    }
    .badge-pill {
        background: #e2e8f0;
        color: #475569;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 0.2rem 0.55rem;
        border-radius: 9999px;
    }

    /* Contrast-Safe Labels & Inputs */
    label p {
        font-weight: 600 !important;
        color: #334155 !important;
        font-size: 0.85rem !important;
        margin-bottom: 0.35rem !important;
    }

    .stTextInput input, 
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        font-size: 0.92rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
    }

    .stTextInput input::placeholder, 
    .stTextArea textarea::placeholder {
        color: #94a3b8 !important;
    }

    .stTextInput input:focus, 
    .stTextArea textarea:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
    }

    /* Selectbox styling */
    div[data-baseweb="select"] {
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        color: #0f172a !important;
        border-radius: 8px !important;
    }

    /* Pill Selection Restyle */
    div[data-testid="stPills"] button {
        border-radius: 20px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 0.35rem 0.85rem !important;
    }

    /* Primary CTA Button */
    div.stButton > button[kind="primary"] {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        border: none !important;
        padding: 0.65rem 1rem !important;
        transition: all 0.15s ease-in-out !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #1e293b !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.15) !important;
    }

    /* Output Workspace Canvas */
    .editor-canvas {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        min-height: 480px;
        line-height: 1.7;
        font-size: 0.95rem;
        color: #1e293b;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    
    .editor-placeholder {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 480px;
        color: #94a3b8;
        border: 1.5px dashed #cbd5e1;
        border-radius: 12px;
        background: #f8fafc;
        text-align: center;
        padding: 2rem;
    }

    /* Stat Badges */
    .stat-badge {
        display: inline-flex;
        align-items: center;
        font-size: 0.78rem;
        font-weight: 600;
        color: #475569;
        background: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 0.25rem 0.55rem;
        margin-right: 0.4rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- Session State -----------------
if "content" not in st.session_state:
    st.session_state.content = ""
if "latency" not in st.session_state:
    st.session_state.latency = 0.0

# ----------------- Top Navigation -----------------
st.markdown(
    """
    <div class="app-header">
        <div class="brand-title">
            <span>✦ Nexus AI</span>
            <span class="badge-pill">Content Studio</span>
        </div>
        <div style="font-size: 0.85rem; color: #64748b; font-weight: 500;">
            Ultra-fast Groq Inference
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------- Sidebar Configuration -----------------
groq_api_key = st.secrets.get("GROQ_API_KEY", "")

with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    if not groq_api_key:
        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="Enter your key from console.groq.com",
        )
    else:
        st.success("API Key loaded securely", icon="🔒")

    # Whitelist verified text models to prevent audio/voice terms-acceptance crashes
    TEXT_MODELS = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
    ]

    selected_model = st.selectbox(
        "Active Model",
        TEXT_MODELS,
        index=0,
        help="llama-3.3-70b gives the highest quality copy; 8b provides near-zero latency.",
    )

    temperature = st.slider("Creativity (Temp)", 0.0, 1.0, 0.7, 0.05)

# ----------------- Two-Column Workspace -----------------
col_editor, col_preview = st.columns([1.05, 1.15], gap="large")

with col_editor:
    with st.container(border=True):
        st.markdown("##### 📝 Create Content")
        st.caption("Configure format, tone, and provide rough context.")

        format_type = st.pills(
            "Format",
            ["LinkedIn", "X Thread", "Newsletter", "Blog Post", "Video Script"],
            default="LinkedIn",
        )

        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            tone = st.selectbox(
                "Tone & Style",
                [
                    "Authoritative & Insightful",
                    "Conversational",
                    "Punchy & Direct",
                    "Educational",
                    "Story-driven",
                ],
            )
        with sub_c2:
            audience = st.text_input(
                "Target Audience",
                placeholder="e.g. Founders, Tech leads, Students",
            )

        keywords = st.text_input(
            "Keywords / Anchors (Optional)",
            placeholder="e.g. AI tools, productivity, speed",
        )

        topic = st.text_area(
            "Topic & Raw Notes",
            placeholder="Paste rough notes, outline, or thesis...",
            height=180,
        )

        generate_clicked = st.button("Generate Content ✦", type="primary", use_container_width=True)

with col_preview:
    st.markdown("##### 📄 Output Workspace")
    st.caption("Review, edit, and export your generated copy.")

    output_area = st.empty()

    if generate_clicked:
        if not groq_api_key:
            st.error("Missing Groq API Key. Add it to secrets or sidebar.")
        elif not topic.strip():
            st.warning("Please provide context or raw notes before generating.")
        else:
            client = Groq(api_key=groq_api_key)
            system_prompt = f"""
You are an expert copywriter and content strategist. Write a clean, high-performing {format_type}.
- Tone: {tone}
- Target Audience: {audience if audience else "General professional"}
- Key Anchors: {keywords if keywords else "None specified"}

Rules:
1. Deliver production-ready copy with clear structural scaffolding, hooks, and clean spacing.
2. Under no circumstances should you include introductory meta-commentary (e.g., 'Here is your post:'). Jump straight into the draft.
"""
            accumulated = ""
            start_time = time.time()

            try:
                stream = client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": topic},
                    ],
                    temperature=temperature,
                    stream=True,
                )

                for chunk in stream:
                    delta = chunk.choices[0].delta.content or ""
                    accumulated += delta
                    output_area.markdown(
                        f'<div class="editor-canvas">{accumulated}▌</div>',
                        unsafe_allow_html=True,
                    )

                st.session_state.content = accumulated
                st.session_state.latency = round(time.time() - start_time, 2)
                output_area.markdown(
                    f'<div class="editor-canvas">{accumulated}</div>',
                    unsafe_allow_html=True,
                )

            except Exception as e:
                st.error(f"Inference error: {e}")

    elif st.session_state.content:
        output_area.markdown(
            f'<div class="editor-canvas">{st.session_state.content}</div>',
            unsafe_allow_html=True,
        )

        words = len(st.session_state.content.split())
        chars = len(st.session_state.content)

        st.markdown(
            f"""
            <div style="margin-top: 0.85rem; margin-bottom: 0.85rem;">
                <span class="stat-badge">📝 {words} words</span>
                <span class="stat-badge">🔤 {chars} chars</span>
                <span class="stat-badge">⚡ {st.session_state.latency}s</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            st.download_button(
                label="📥 Download Markdown",
                data=st.session_state.content,
                file_name="draft.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with btn_col2:
            st.download_button(
                label="📄 Download Plain Text",
                data=st.session_state.content,
                file_name="draft.txt",
                mime="text/plain",
                use_container_width=True,
            )
    else:
        output_area.markdown(
            """
            <div class="editor-placeholder">
                <span style="font-size: 1.8rem; margin-bottom: 0.5rem;">✦</span>
                <div style="font-weight: 600; font-size: 0.95rem; color: #64748b;">Ready for Creation</div>
                <div style="font-size: 0.82rem; color: #94a3b8; margin-top: 0.2rem;">Configure your prompt on the left and hit generate.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
