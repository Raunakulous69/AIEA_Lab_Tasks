from kb_loader import load_kb_lines
from rag_store import build_vectorstore
from graph_app import build_graph


def run_smoke_tests():
    kb = load_kb_lines("simpsons_kb.pl")
    db = build_vectorstore(kb, persist_dir="chroma_db_test")
    app = build_graph(db)

    queries = [
        "Is homer the parent of bart?",
        "Does monty_burns own the springfield_nuclear_plant?",
        "Is lisa smart?",
        "Is bart kind?",  # likely false based on facts
        "Is ned friend of homer?",
    ]

    for q in queries:
        out = app.invoke({"query": q})
        print("\n=============================")
        print("Q:", q)
        print("Relevance:", out.get("relevance"), "| refine_round:", out.get("refine_round"))
        print("Answer:", out.get("final_answer"))
        print("Trace:", out.get("inference_trace"))


if __name__ == "__main__":
    run_smoke_tests()