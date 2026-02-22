from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union
import re

Bindings = Dict[str, str]

VAR_RE = re.compile(r"\(\?([a-zA-Z_]\w*)\)")  # matches (?x), (?animal), etc.


class AND(list):
    """AND([a,b,c]) means all subgoals must be true."""
    def __repr__(self):
        return f"AND({list.__repr__(self)})"


class OR(list):
    """OR([a,b,c]) means any subgoal can be true."""
    def __repr__(self):
        return f"OR({list.__repr__(self)})"


class NOT:
    """NOT(x) means x must be false (used in some forward-chaining tasks)."""
    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return f"NOT({self.x!r})"


PASS = "PASS"
FAIL = "FAIL"


@dataclass(frozen=True)
class Rule:
    antecedent: Any
    consequent: Any


def IF(antecedent, consequent):
    # Convenience: IF(A, THEN(B)) also allowed
    if isinstance(consequent, tuple) and len(consequent) == 2 and consequent[0] == "THEN":
        consequent = consequent[1]
    return Rule(antecedent=antecedent, consequent=consequent)


def THEN(consequent):
    return ("THEN", consequent)


def variables(statement: str) -> Set[str]:
    """Return set of variable names found in a pattern, like {'x','y'} for '(?x) loves (?y)'."""
    return set(VAR_RE.findall(statement))


def _tokenize_pattern(pat: str) -> List[str]:
    # Split by whitespace; MIT format depends on word positions.
    # Example: "(?x) is a penguin" -> ["(?x)","is","a","penguin"]
    return pat.strip().split()


def match(pattern: str, datum: str) -> Optional[Bindings]:
    """
    Unify a single pattern string against a single datum string.
    Variables are of the form (?x).
    Returns dict bindings if match succeeds, else None.
    """
    p_tokens = _tokenize_pattern(pattern)
    d_tokens = _tokenize_pattern(datum)
    if len(p_tokens) != len(d_tokens):
        return None

    binds: Bindings = {}
    for p, d in zip(p_tokens, d_tokens):
        m = VAR_RE.fullmatch(p)
        if m:
            var = m.group(1)
            if var in binds and binds[var] != d:
                return None
            binds[var] = d
        else:
            if p != d:
                return None
    return binds


def populate(template: Any, bindings: Bindings) -> Any:
    """
    Substitute bindings into a template.
    Works for: strings, AND/OR structures, NOT, lists.
    """
    if isinstance(template, str):
        def repl(m):
            var = m.group(1)
            return bindings.get(var, f"(?{var})")
        return VAR_RE.sub(repl, template)

    if isinstance(template, AND):
        return AND([populate(x, bindings) for x in template])
    if isinstance(template, OR):
        return OR([populate(x, bindings) for x in template])
    if isinstance(template, NOT):
        return NOT(populate(template.x, bindings))
    if isinstance(template, list):
        return [populate(x, bindings) for x in template]

    return template


def simplify(expr: Any) -> Any:
    """
    Flatten nested AND/OR, remove duplicates, collapse singletons.
    Keeps strings as-is.
    """
    if isinstance(expr, str):
        return expr

    if isinstance(expr, NOT):
        return NOT(simplify(expr.x))

    if isinstance(expr, AND):
        items: List[Any] = []
        for x in expr:
            sx = simplify(x)
            if isinstance(sx, AND):
                items.extend(list(sx))
            else:
                items.append(sx)

        # remove duplicates while preserving order
        seen = set()
        deduped = []
        for it in items:
            key = repr(it)
            if key not in seen:
                seen.add(key)
                deduped.append(it)

        if len(deduped) == 1:
            return deduped[0]
        return AND(deduped)

    if isinstance(expr, OR):
        items: List[Any] = []
        for x in expr:
            sx = simplify(x)
            if isinstance(sx, OR):
                items.extend(list(sx))
            else:
                items.append(sx)

        seen = set()
        deduped = []
        for it in items:
            key = repr(it)
            if key not in seen:
                seen.add(key)
                deduped.append(it)

        if len(deduped) == 1:
            return deduped[0]
        return OR(deduped)

    return expr