from __future__ import annotations

from audit_rag.retrieval.query_context import QueryContext


def hybrid_search(query: str, context: QueryContext | None = None) -> dict:
    runtime = context or QueryContext()
    return {
        "query": query,
        "status": "todo",
        "message": "Hybrid retrieval not implemented yet.",
        "skill_name": runtime.skill_name,
        "stage_name": runtime.stage_name,
        "component_type": runtime.component_type,
    }
