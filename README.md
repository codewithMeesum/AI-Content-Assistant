<div align="center">

# ⚡ Nexus AI Content Studio
### High-Performance Content Engine Powered by Groq LPUs & Streamlit

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mesum-project.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Groq API](https://img.shields.io/badge/Inference-Groq%20LPU-orange.svg)](https://groq.com/)

[**Explore Live App ↗**](https://mesum-project.streamlit.app/) • [**Report Bug**](https://github.com/your-username/ai-content-assistant/issues) • [**Request Feature**](https://github.com/your-username/ai-content-assistant/issues)

</div>

---

## 📌 Overview

**Nexus AI Content Studio** is an ultra-low-latency AI content copilot built for creators, growth marketers, and founders. Leveraging Groq's high-speed inference engine, Nexus compiles conversion-driven copy, technical deep dives, and viral social threads with zero conversational bloat.

The UI is intentionally engineered to mirror modern minimalist SaaS benchmarks like Linear and Notion: clean typography, interactive format pills, live streaming output, and one-click exports.

---

## ✨ Key Capabilities

* **⚡ Ultra-Low Latency Inference:** Streams completed drafts in seconds using Groq LPUs.
* **🎯 Dynamic Content Formats:** Tailored generation for LinkedIn, X Threads, Technical Blogs, Newsletters, and Video Scripts.
* **🎨 Precision Style & Tone Control:** Granular style levers from authoritative domain leadership to punchy, conversational copy.
* **📊 Real-time Output Analytics:** Tracks total word count, character count, and inference latency on every run.
* **📥 Instant Multi-Format Export:** Export generated drafts directly to `.md` (Markdown) or `.txt` (Plain Text).
* **🔒 Enterprise-Safe Key Management:** Seamlessly switches between Streamlit Secrets management and manual user-provided keys.

---

## 🛠️ Tech Stack

| Layer | Tool / Library |
|---|---|
| **Frontend & UI** | Streamlit, Custom SaaS CSS (Inter/Plus Jakarta Sans) |
| **Inference Engine** | Groq Python SDK |
| **Active Models** | `groq/compound-mini`, `llama3-70b-8192`, `llama3-8b-8192`, `mixtral-8x7b-32768` |
| **Deployment** | Streamlit Community Cloud |

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone [https://github.com/your-username/ai-content-assistant.git](https://github.com/your-username/ai-content-assistant.git)
cd ai-content-assistant
