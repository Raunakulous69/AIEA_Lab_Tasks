
# Task 9 - LangGraph Migration (AIEA Lab)

This project migrates a Task 8-style LangChain + KB retrieval workflow into **LangGraph**.

## Features
- Prolog-style KB (`simpsons_kb.pl`) used as a source for RAG retrieval
- LangGraph pipeline:
  1) retrieve context (RAG)
  2) judge relevance
  3) self-refine with additional retrieval if relevance is low
  4) output final true/false + inference trace

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
