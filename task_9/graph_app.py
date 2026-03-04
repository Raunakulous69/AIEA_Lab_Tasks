from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, TypedDict

from langgraph.graph import StateGraph, END

from rag_store import retrieve_context
from llm_judge import judge_relevance, infer_true_false


class GraphState(TypedDict, total=False):
    query: str
    retrieved: List[str]
    relevance: bool
    relevance_explanation: str
    refine_round: int
    final_answer: bool
    inference_trace: str


def build_graph(vectordb) -> Any:
    graph = StateGraph(GraphState)

    def retrieve_node(state: GraphState) -> GraphState:
        query = state["query"]
        retrieved = retrieve_context(vectordb, query, k=6)
        return {
            **state,
            "retrieved": retrieved,
            "refine_round": state.get("refine_round", 0),
        }

    def judge_node(state: GraphState) -> GraphState:
        is_rel, expl = judge_relevance(state["query"], state.get("retrieved", []))
        return {**state, "relevance": is_rel, "relevance_explanation": expl}

    def refine_retrieve_node(state: GraphState) -> GraphState:
        """
        Self-refinement: do an additional retrieval with a slightly expanded query.
        """
        round_num = state.get("refine_round", 0) + 1
        base_q = state["query"]

        # Simple expansion prompt
        expanded_q = base_q + " facts rules relationships"

        retrieved = retrieve_context(vectordb, expanded_q, k=8)
        return {**state, "retrieved": retrieved, "refine_round": round_num}

    def infer_node(state: GraphState) -> GraphState:
        ans, trace = infer_true_false(state["query"], state.get("retrieved", []))
        return {**state, "final_answer": ans, "inference_trace": trace}

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("judge", judge_node)
    graph.add_node("refine_retrieve", refine_retrieve_node)
    graph.add_node("infer", infer_node)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "judge")

    # # Conditional: if relevance is false and refine_round < 1, refine; else infer
    # def should_refine(state: GraphState) -> str:
    #     if not state.get("relevance", False) and state.get("refine_round", 0) < 1:
    #         return "refine_retrieve"
    #     return "infer"


    def should_refine(state: GraphState) -> str:
    # Force exactly ONE refinement pass for demo purposes
        if state.get("refine_round", 0) < 1:
            return "refine_retrieve"
        return "infer"


    graph.add_conditional_edges(
        "judge",
        should_refine,
        {
            "refine_retrieve": "refine_retrieve",
            "infer": "infer",
        },
    )

    graph.add_edge("refine_retrieve", "judge")
    graph.add_edge("infer", END)

    return graph.compile()