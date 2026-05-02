<!-- prettier-ignore -->
# PDF-Constrained Conversational Agent

[![Status](https://img.shields.io/badge/status-active-brightgreen)](https://github.com)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/streamlit-%E2%9C%93-orange?logo=streamlit)](https://streamlit.io)
[![Dependabot](https://img.shields.io/badge/dependencies-up--to--date-brightgreen)](https://github.com)

>A compact, production-ready conversational agent that answers user questions strictly from an uploaded PDF — with explicit page citations and safe refusals for out-of-scope queries.

## Table of contents

- [Features](#features)
- [Quickstart](#quickstart)
- [Usage](#usage)
- [Testing](#testing)
- [Development](#development)
- [Contributing](#contributing)

## Features

- Answers drawn only from the uploaded PDF with inline page citations.
- Clean, prompt-driven refusals to out-of-scope questions.
- No external vector DB required — designed to use large context models.
- Modular tools: PDF extraction, citation builder, and memory are separated for clarity.

## Quickstart

Clone, create a virtual environment, install deps, and run:

```bash
git clone <your-repo>
cd pdf_agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

See [app.py](app.py) for the Streamlit entry point and [requirements.txt](requirements.txt) for dependencies.

## Usage

1. Open the app (Streamlit will print a local URL).
2. Upload a PDF in the sidebar.
3. Ask natural-language questions — answers include page citations like "[Page 4]".
4. Try edge cases from [tests/invalid_queries.txt](tests/invalid_queries.txt) to confirm refusal behavior.

## Testing

- Sample valid/invalid queries: [tests/valid_queries.txt](tests/valid_queries.txt) and [tests/invalid_queries.txt](tests/invalid_queries.txt).
- To run unit tests (if present):

```bash
pytest -q
```

## Development

- Core agent logic: `agent/core.py`
- Prompts: `agent/prompts.py`
- Tools: `tools/pdf_extractor.py`, `tools/citation_builder.py`
- Memory: `memory/conversation.py`

Use the `.venv` environment shown above for development flows.

## Contributing

Contributions are welcome. Open an issue or send a PR describing the change and any required environment variables.

---
