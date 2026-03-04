from __future__ import annotations

import argparse

from kb_loader import load_kb_lines
from rag_store import build_vectorstore
from graph_app import build_graph


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb", default="simpsons_kb.pl")
    parser.add_argument("--query", required=True)
    args = parser.parse_args()

    kb_lines = load_kb_lines(args.kb)
    vectordb = build_vectorstore(kb_lines, persist_dir="chroma_db")

    app = build_graph(vectordb)

    result = app.invoke({"query": args.query})

    print("\n====== TASK 9 OUTPUT ======")
    print(f"Query: {result.get('query')}")
    print(f"Refine rounds: {result.get('refine_round')}")
    print(f"Relevance: {result.get('relevance')}")
    print(f"Relevance explanation: {result.get('relevance_explanation')}\n")

    print("---- Retrieved Context ----")
    for i, line in enumerate(result.get("retrieved", []), start=1):
        print(f"{i}. {line}")

    print("\n---- Final Answer ----")
    print(f"Answer (true/false): {result.get('final_answer')}")
    print("\n---- Inference Trace ----")
    print(result.get("inference_trace"))


if __name__ == "__main__":
    main()