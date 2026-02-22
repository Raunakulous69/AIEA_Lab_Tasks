from data import zookeeper_rules
from lab1 import backchain_to_goal_tree
from production import AND, OR, NOT


def pretty(tree, indent=0):
    sp = "  " * indent
    if isinstance(tree, str):
        return sp + tree
    if isinstance(tree, NOT):
        return sp + "NOT\n" + pretty(tree.x, indent + 1)
    if isinstance(tree, AND):
        lines = [sp + "AND"]
        for t in tree:
            lines.append(pretty(t, indent + 1))
        return "\n".join(lines)
    if isinstance(tree, OR):
        lines = [sp + "OR"]
        for t in tree:
            lines.append(pretty(t, indent + 1))
        return "\n".join(lines)
    return sp + repr(tree)


def main():
    goal = "opus is a penguin"
    tree = backchain_to_goal_tree(zookeeper_rules, goal)
    print("GOAL:", goal)
    print("\nGOAL TREE:")
    print(pretty(tree))


if __name__ == "__main__":
    main()