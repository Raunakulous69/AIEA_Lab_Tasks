from __future__ import annotations

from pathlib import Path


def load_kb_lines(kb_path: str) -> list[str]:
    """
    Loads a .pl knowledge base and returns meaningful lines as text docs for RAG.
    Keeps facts/rules and ignores blank lines and pure comments.
    """
    path = Path(kb_path)
    if not path.exists():
        raise FileNotFoundError(f"KB file not found: {kb_path}")

    docs: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("%"):
            continue
        # Keep Prolog statements ending in '.'
        if line.endswith("."):
            docs.append(line)
    return docs