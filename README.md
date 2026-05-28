# 🚀 LinkedIn Post Generator (Codebasics Project)

An AI-powered tool that generates personalized, high-engaging LinkedIn posts based on historical performance data. Utilizing a **Few-Shot Learning** approach, the system extracts structural attributes (line count, language, and topics) from your past successful posts, unifies your content tags, and guides a Large Language Model (LLM) to replicate your distinct writing style.

---

## 🛠️ Tech Stack & Architecture

* **Frontend Framework:** Streamlit (Dynamic, responsive UI dashboard)
* **LLM Orchestration:** LangChain Core & LangChain Groq
* **Inference Provider:** Groq Cloud API (Ultra-fast execution)
* **Foundation Model:** `llama-3.3-70b-versatile`
* **Data Analysis:** Pandas (Data structuring, analytics, and categorical filtering)

---

##  Project Structure

```text
telegram post generator/
│
├── data/
│   ├── raw_posts.json          # Unprocessed historical LinkedIn posts
│   └── processed_posts.json    # Sanitized and LLM-enriched data with clean tags
│
├── app.py                      # Main Streamlit UI dashboard
├── preprocess.py               # Data ingestion, regex sanitization, & tag unification pipeline
├── few_shot.py                 # File I/O handler, vector-mimic logic, and analytics
├── post_generator.py           # Few-shot dynamic prompt builder and Groq API connector
├── llm_helper.py               # Centralized LLM engine initialization
├── .env                        # Local environment credentials (Secret API Keys)
└── README.md                   # Project documentation
