# PDF-Constrained Conversational Agent

A production-grade AI agent that answers questions strictly from an uploaded PDF — with page citations and clean refusals for out-of-scope queries.


## Architecture

```
User → Streamlit UI → Agent Core → Gemini 2.5 Flash
                    ↓
              PDF Extractor (tools/)
              Citation Builder (tools/)
              Conversation Memory (memory/)
              Structured Logger (utils/)
```

**Key design decisions:**
- **No vector DB** — Gemini's 1M token context window fits entire PDFs directly. Simpler = more reliable.
- **Tools pattern** — PDF extraction and citation parsing are isolated tools, not embedded in agent logic.
- **Memory module** — Conversation history managed separately for clean multi-turn dialogue.
- **Prompt-first refusal** — The system prompt strictly instructs the model to refuse out-of-scope queries, not post-process filter them.

## Setup

```bash
# 1. Clone and enter the project
git clone <your-repo>
cd pdf-agent

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
cp .env.example .env
# Edit .env and paste your Gemini API key

# 5. Run the app
streamlit run app.py
```

## Testing

Use the sample queries in `tests/valid_queries.txt` and `tests/invalid_queries.txt`.

Upload any PDF via the sidebar, then test both valid and invalid queries to verify:
- Valid queries return cited answers with [Page X] references
- Invalid queries are refused cleanly

## Deployment (Streamlit Cloud)

1. Push this repo to GitHub (make sure `.env` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. In **Secrets**, add: `GEMINI_API_KEY = "your_key_here"`
5. Deploy — get a live URL to share with recruiters

## Bonus

The agent supports non-English PDFs. Gemini 1.5 Flash handles multilingual documents natively. Queries in Hindi, French, or any supported language will be answered in the same language as the query.
