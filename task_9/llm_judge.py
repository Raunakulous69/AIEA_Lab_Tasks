from __future__ import annotations

import re
from typing import Tuple


def judge_relevance(query: str, retrieved: list[str]) -> Tuple[bool, str]:
    """
    Lightweight relevance check:
    - If query tokens overlap enough with retrieved facts, mark relevant.
    Returns (is_relevant, explanation).
    """
    q = query.lower()
    q_tokens = set(re.findall(r"[a-z_]+", q))
    if not q_tokens:
        return False, "Query had no valid tokens."

    joined = " ".join(retrieved).lower()
    hit = sum(1 for t in q_tokens if t in joined)

    # Tune threshold as needed
    if hit >= max(2, len(q_tokens) // 4):
        return True, f"Relevant: token hits={hit} for tokens={sorted(list(q_tokens))[:10]}"
    return False, f"Not relevant enough: token hits={hit} for tokens={sorted(list(q_tokens))[:10]}"


def infer_true_false(query: str, retrieved: list[str]) -> Tuple[bool, str]:
    """
    Very simple inference for demo:
    If retrieved contains direct evidence lines that match patterns implied by query,
    return True; else False.

    This is NOT full Prolog execution—it's a minimal 'logical inference trace' style.
    """
    q = query.lower()
    ctx = [r.lower() for r in retrieved]

    # Example supported query forms:
    # "Is homer the parent of bart?"
    # "Is lisa smart?"
    # "Does burns own the nuclear plant?"
    patterns = [
        ("parent", r"parent\(([^,]+),\s*([^)]+)\)\.", "parent"),
        ("spouse", r"spouse\(([^,]+),\s*([^)]+)\)\.", "spouse"),
        ("friend", r"friend\(([^,]+),\s*([^)]+)\)\.", "friend"),
        ("owns", r"owns\(([^,]+),\s*([^)]+)\)\.", "owns"),
        ("works_at", r"works_at\(([^,]+),\s*([^)]+)\)\.", "works_at"),
        ("smart", r"smart\(([^)]+)\)\.", "smart"),
        ("kind", r"kind\(([^)]+)\)\.", "kind"),
        ("mischievous", r"mischievous\(([^)]+)\)\.", "mischievous"),
    ]

    trace_lines = []
    for label, regex, keyword in patterns:
        if keyword in q:
            for line in ctx:
                m = re.match(regex, line.strip())
                if m:
                    trace_lines.append(f"Matched fact: {line.strip()}")
                    return True, "\n".join(trace_lines)

            trace_lines.append(f"No matching fact found for keyword '{keyword}'.")
            return False, "\n".join(trace_lines)

    # fallback
    return False, "Query pattern not recognized by demo inferencer. (Still shows retrieval + relevance loop.)"