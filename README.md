# ✦ Nexus AI | Content Studio

A minimalist, high-performance content creation copilot powered by **Groq LPUs** and **Streamlit**. 

Nexus AI transforms rough notes and bullet points into production-ready copy across multiple formats with real-time streaming and zero conversational filler.

🔗 **Live Deployment:** [mesum-project.streamlit.app](https://mesum-project.streamlit.app/)

---

## What It Does

Nexus AI provides a structured, side-by-side workspace designed for fast writing workflows:

* **Format Selection via Pills:** Instantly switch between `LinkedIn`, `X Thread`, `Newsletter`, `Blog Post`, and `Video Script`.
* **Style & Audience Controls:** Set targeted tones (`Authoritative & Insightful`, `Conversational`, `Punchy & Direct`, `Educational`, `Story-driven`) and custom target demographics.
* **Keyword Anchoring:** Inject critical keywords and hashtags naturally into the generated piece.
* **Live Streaming Output:** Ultra-low latency draft generation directly from Groq's high-speed inference engine.
* **Output Workspace:** Built-in live tracking for word count, character count, and latency, plus one-click `.md` and `.txt` export options.

---

## App Interface

| Section | Purpose |
|---|---|
| **Create Content (Left)** | Set content format, tone, target audience, keywords, and raw notes. |
| **Output Workspace (Right)** | Real-time streamed copy with performance stats and download buttons. |
| **Engine Settings (Sidebar)** | Manage your Groq API key and select active model architectures (`groq/compound-mini`, `llama3-70b-8192`, `llama3-8b-8192`, `mixtral-8x7b-32768`). |

---

## Tech Stack

* **Frontend:** Streamlit
* **Styling:** Custom CSS (Plus Jakarta Sans, light theme, custom card wrappers)
* **Inference API:** Groq Python SDK
* **Hosting:** Streamlit Community Cloud

---

## Project Structure

```text
├── app.py              # Main application logic and UI styling
├── requirements.txt    # Python dependencies (streamlit, groq)
├── .streamlit/
│   ├── config.toml     # UI theme settings (forces light mode)
│   └── secrets.toml    # (Optional) Local Groq API key storage
└── README.md           # Project documentation
