import os
import time
import streamlit as st
from groq import Groq

# ----------------- Page Setup -----------------
st.set_page_config(
    page_title="Nexus | AI Content Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------- Modern SaaS Styling -----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Top Banner Styling */
    .hero-container {
        padding: 1.5rem 1.8rem;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid #334155;
        border-radius: 14px;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    .hero-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.35rem;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        font-weight: 400;
        margin: 0;
    }

    /* Output Card */
    .output-container {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
    }

    /* Button Polish */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- Session State Initialization -----------------
if "generated_content" not in st.session_state:
    st.session_state.generated_content = ""
if "generation_time" not in st.session_state:
    st.session_state.generation_time = 0.0
if "last_params" not in st.session_state:
    st.session_state.last_params = {}

# ----------------- Hero Banner -----------------
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">⚡ Nexus AI Content Studio</div>
        <p class="hero-subtitle">Ultra-fast inference platform engineered to craft high-conversion copy, technical breakdowns, and multi-channel campaigns.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------- Sidebar / Engine Controls -----------------
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")

    api_key_source = st.secrets.get("GROQ_API_KEY", "")
    if not api_key_source:
        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="Grab your API key at https://console.groq.com/keys",
        )
    else:
        groq_api_key = api_key_source
        st.success("API Key loaded from environment", icon="🔒")

    st.markdown("---")

    model_option = st.selectbox(
        "Base Architecture",
        ("llama-3.3-70b-versatile", "llama-3.1-8b-instant"),
        index=0,
        help="Use 70B for nuanced writing; 8B for raw speed.",
    )

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        temperature = st.slider("Temperature", 0.0, 1.2, 0.65, 0.05)
    with col_s2:
        max_tokens = st.slider("Max Tokens", 256, 4096, 1500, 128)

    st.markdown("---")
    st.caption("Nexus Content Assistant v2.0 • Powered by Llama 3 & Groq LPUs")

# ----------------- Workspace Layout -----------------
left_col, right_col = st.columns([1.1, 1.2], gap="large")

with left_col:
    st.markdown("#### 🎯 Creative Brief")

    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            content_type = st.selectbox(
                "Format",
                (
                    "LinkedIn Thought Leadership",
                    "X (Twitter) Thread",
                    "Technical Blog Article",
                    "Executive Newsletter",
                    "Short-form Video Script",
                    "Product Launch Email",
                ),
            )
        with col2:
            tone = st.selectbox(
                "Tone & Style",
                (
                    "Authoritative & Insightful",
                    "Punchy & Direct",
                    "Conversational & Relatable",
                    "Analytical & Educational",
                    "Compelling & Persuasive",
                ),
            )

        audience = st.text_input(
            "Target Audience",
            placeholder="e.g., Early-stage founders, Data Engineers, B2B Marketers",
        )

        keywords = st.text_input(
            "Keywords / Anchors (Optional)",
            placeholder="e.g., Latency, Open-source LLMs, ROI",
        )

        topic = st.text_area(
            "Topic & Raw Context",
            placeholder="Paste your rough bullet points, data findings, or the premise of your piece...",
            height=180,
        )

        generate_btn = st.button("Generate Draft 🚀", type="primary", use_container_width=True)

# ----------------- Processing & Output -----------------
with right_col:
    st.markdown("#### 📄 Output Workspace")

    if generate_btn:
        if not groq_api_key:
            st.error("Missing API key. Supply one via sidebar or Streamlit Secrets.")
        elif not topic.strip():
            st.warning("Please provide context or raw notes before generating.")
        else:
            client = Groq(api_key=groq_api_key)

            system_instruction = f"""
You are an elite copywriter, content strategist, and domain expert.
Craft a world-class {content_type} geared towards {audience if audience else "an executive professional audience"}.

Guidelines:
1. Tone: {tone}.
2. Integrated Keywords/Phrases: {keywords if keywords else "None"}.
3. Formatting: Use strong hooks, clean typographic spacing, bold headers, and structured bullets.
4. Output standard: Production-ready copy only. No conversational meta-commentary (do not say "Here is your post:").
"""

            response_box = st.empty()
            accumulator = ""
            start_time = time.time()

            try:
                with st.spinner("Compiling copy with Groq..."):
                    stream = client.chat.completions.create(
                        model=model_option,
                        messages=[
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": topic},
                        ],
                        temperature=temperature,
                        max_tokens=max_tokens,
                        stream=True,
                    )

                    for chunk in stream:
                        text_delta = chunk.choices[0].delta.content or ""
                        accumulator += text_delta
                        response_box.markdown(accumulator + "▌")

                    response_box.markdown(accumulator)

                # Persist state
                st.session_state.generated_content = accumulator
                st.session_state.generation_time = round(time.time() - start_time, 2)
                st.session_state.last_params = {
                    "format": content_type,
                    "tone": tone,
                    "model": model_option,
                }
                st.rerun()

            except Exception as err:
                st.error(f"Inference Failure: {err}")

    # Display persisted content tabs if available
    if st.session_state.generated_content:
        tab_preview, tab_raw = st.tabs(["Formatted Preview", "Markdown Raw"])

        with tab_preview:
            with st.container(border=True):
                st.markdown(st.session_state.generated_content)

        with tab_raw:
            st.text_area(
                "Raw Markdown",
                st.session_state.generated_content,
                height=300,
                label_visibility="collapsed",
            )

        # Content Metrics Bar
        word_count = len(st.session_state.generated_content.split())
        char_count = len(st.session_state.generated_content)

        m1, m2, m3 = st.columns(3)
        m1.metric("Words", f"{word_count:,}")
        m2.metric("Characters", f"{char_count:,}")
        m3.metric("Latency", f"{st.session_state.generation_time}s")

        # Utility Download Actions
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button(
                label="📥 Download .MD",
                data=st.session_state.generated_content,
                file_name="draft.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with col_dl2:
            st.download_button(
                label="📄 Download .TXT",
                data=st.session_state.generated_content,
                file_name="draft.txt",
                mime="text/plain",
                use_container_width=True,
            )
    else:
        st.info("Your generated output will appear here with live streaming, analytics, and download options.")