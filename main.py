import os
import time
import streamlit as st
from groq import Groq

# ----------------- Page Configuration -----------------
st.set_page_config(
    page_title="AI Content Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------- High-End SaaS Custom CSS -----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global typography and background */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #0f172a;
    }
    
    .stApp {
        background-color: #f8fafc;
    }

    /* Remove Streamlit default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Minimalist Navbar */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 1.25rem;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 2rem;
    }
    .brand-logo {
        font-size: 1.25rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #0f172a;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .brand-badge {
        font-size: 0.75rem;
        font-weight: 600;
        background: #f1f5f9;
        color: #475569;
        padding: 0.2rem 0.55rem;
        border-radius: 9999px;
        border: 1px solid #e2e8f0;
    }

    /* Clean Card Containers */
    div[data-testid="stVerticalBlock"] > div:has(> div.card-wrapper) {
        background: #ffffff;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
        padding: 1.5rem;
    }

    .panel-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.25rem;
    }
    .panel-subtitle {
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 1.2rem;
    }

    /* Custom Streamlit Input Styles */
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
        background: #ffffff !important;
        color: #0f172a !important;
        font-size: 0.9rem !important;
        box-shadow: none !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 1px #3b82f6 !important;
    }

    /* Primary Button */
    div.stButton > button[kind="primary"] {
        background: #0f172a !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.65rem 1.25rem !important;
        transition: all 0.15s ease !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background: #1e293b !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15) !important;
    }

    /* Clean Output Box */
    .output-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        min-height: 420px;
        line-height: 1.65;
        font-size: 0.95rem;
        color: #1e293b;
    }

    /* Metric Badges */
    .stat-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.8rem;
        color: #64748b;
        background: #f1f5f9;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        margin-right: 0.5rem;
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- State Management -----------------
if "content" not in st.session_state:
    st.session_state.content = ""
if "generation_time" not in st.session_state:
    st.session_state.generation_time = 0.0

# ----------------- Top Header Navigation -----------------
st.markdown(
    """
    <div class="nav-bar">
        <div class="brand-logo">
            <span>⚡ ContentCraft</span>
            <span class="brand-badge">Lite Edition</span>
        </div>
        <div style="font-size: 0.85rem; color: #64748b; font-weight: 500;">
            Ultra-fast Groq Inference
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------- API Key & Model Configuration -----------------
groq_api_key = st.secrets.get("GROQ_API_KEY", "")

with st.sidebar:
    st.markdown("### ⚙️ Engine")
    if not groq_api_key:
        groq_api_key = st.text_input("Groq Key", type="password", placeholder="gsk_...")

    # Dynamic model fetch to prevent 404s
    models = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"]
    if groq_api_key:
        try:
            client_probe = Groq(api_key=groq_api_key)
            fetched = [
                m.id for m in client_probe.models.list().data 
                if not any(x in m.id for x in ["whisper", "guard", "vision"])
            ]
            if fetched:
                models = fetched
        except Exception:
            pass

    selected_model = st.selectbox("Model", models, index=0)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05)

# ----------------- Main Workspace -----------------
left_col, right_col = st.columns([1, 1.15], gap="large")

with left_col:
    st.markdown('<div class="card-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Create New Draft</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-subtitle">Select format, tune style, and generate conversion-ready copy.</div>', unsafe_allow_html=True)

    format_choice = st.pills(
        "Format",
        ["LinkedIn", "X Thread", "Newsletter", "Blog Post", "Video Script"],
        default="LinkedIn",
        label_visibility="collapsed",
    )

    c1, c2 = st.columns(2)
    with c1:
        tone_choice = st.selectbox(
            "Tone",
            ["Authoritative", "Conversational", "Punchy & Direct", "Educational", "Story-driven"],
        )
    with c2:
        audience_choice = st.text_input("Target Audience", placeholder="e.g., Tech founders, Devs")

    topic_prompt = st.text_area(
        "Key Notes or Outline",
        placeholder="Paste bullets, rough points, or raw thoughts...",
        height=180,
    )

    generate_btn = st.button("Generate Content ✦", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="panel-title">Editor Workspace</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-subtitle">Streamed copy ready to review, tweak, and export.</div>', unsafe_allow_html=True)

    if generate_btn:
        if not groq_api_key:
            st.error("Please add your Groq API key in the sidebar or secrets.")
        elif not topic_prompt.strip():
            st.warning("Please enter your notes or outline first.")
        else:
            system_msg = f"""
You are an expert copywriter. Write a high-converting, exceptionally engaging {format_choice}.
- Tone: {tone_choice}
- Target Audience: {audience_choice if audience_choice else 'General professionals'}
- Rule: Deliver polished copy immediately. No conversational preamble ('Here is your post:').
"""
            client = Groq(api_key=groq_api_key)
            output_holder = st.empty()
            accumulated = ""
            start_t = time.time()

            try:
                stream = client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": topic_prompt},
                    ],
                    temperature=temperature,
                    stream=True,
                )
                for chunk in stream:
                    delta = chunk.choices[0].delta.content or ""
                    accumulated += delta
                    output_holder.markdown(
                        f'<div class="output-box">{accumulated}▌</div>',
                        unsafe_allow_html=True,
                    )

                st.session_state.content = accumulated
                st.session_state.generation_time = round(time.time() - start_t, 2)
                output_holder.markdown(
                    f'<div class="output-box">{accumulated}</div>',
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.error(f"Generation error: {e}")

    elif st.session_state.content:
        # Display saved content in clean container
        st.markdown(
            f'<div class="output-box">{st.session_state.content}</div>',
            unsafe_allow_html=True,
        )

        # Meta & Quick Export Actions
        words = len(st.session_state.content.split())
        chars = len(st.session_state.content)
        
        st.markdown(
            f"""
            <div style="margin-top: 1rem; margin-bottom: 1rem;">
                <span class="stat-badge">📝 {words} words</span>
                <span class="stat-badge">🔤 {chars} chars</span>
                <span class="stat-badge">⚡ {st.session_state.generation_time}s</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        b1, b2 = st.columns(2)
        with b1:
            st.download_button(
                label="Copy / Download Markdown",
                data=st.session_state.content,
                file_name="content.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with b2:
            st.download_button(
                label="Download Plain Text",
                data=st.session_state.content,
                file_name="content.txt",
                mime="text/plain",
                use_container_width=True,
            )
    else:
        st.markdown(
            '<div class="output-box" style="display:flex; align-items:center; justify-content:center; color:#94a3b8;">'
            'Your generated copy will appear here live.'
            '</div>',
            unsafe_allow_html=True,
        )
