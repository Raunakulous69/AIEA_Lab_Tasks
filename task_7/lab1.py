from __future__ import annotations
from typing import Any, Dict, List, Optional, Set, Tuple

from production import AND, OR, NOT, Rule, match, populate, simplify


def _as_list(x):
    return x if isinstance(x, list) else [x]


def backchain_to_goal_tree(rules: List[Rule], hypothesis: str) -> Any:
    """
    Takes a hypothesis (string) and a list of rules (Rule objects),
    returning an AND/OR tree of subgoals needed to prove the hypothesis.

    Leaves are strings. Internal nodes are AND(...) or OR(...).
    """
    memo: Dict[str, Any] = {}
    visiting: Set[str] = set()

    def bc(goal: str) -> Any:
        # memoization
        if goal in memo:
            return memo[goal]
        # cycle guard
        if goal in visiting:
            return goal

        visiting.add(goal)

        # Always include the goal itself as a valid leaf in the OR tree
        options: List[Any] = [goal]

        for rule in rules:
            consequents = _as_list(rule.consequent)

            for cons in consequents:
                if not isinstance(cons, str):
                    continue

                bindings = match(cons, goal)
                if bindings is None:
                    continue

                ant = populate(rule.antecedent, bindings)

                # Recursively backchain the antecedent
                if isinstance(ant, str):
                    options.append(bc(ant))

                elif isinstance(ant, AND):
                    options.append(AND([bc(x) if isinstance(x, str) else x for x in ant]))

                elif isinstance(ant, OR):
                    options.append(OR([bc(x) if isinstance(x, str) else x for x in ant]))

                elif isinstance(ant, NOT):
                    # Keep NOT as-is (still a leaf-like constraint)
                    # In some assignments you might want to backchain inside NOT,
                    # but most Task 7 backward-chainers keep it as a leaf.
                    options.append(ant)

                else:
                    options.append(ant)

        tree = simplify(OR(options))
        memo[goal] = tree
        visiting.remove(goal)
        return tree

    return bc(hypothesis)