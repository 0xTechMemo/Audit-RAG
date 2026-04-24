from __future__ import annotations

from audit_rag.contracts.triage import CandidateTriageOutput
from audit_rag.indexing.hybrid_search import hybrid_search
from audit_rag.retrieval.query_context import QueryContext


def triage_issue(text: str, context: QueryContext | None = None) -> dict:
    runtime = context or QueryContext()
    search_result = hybrid_search(text, runtime)
    result = CandidateTriageOutput(
        issue_text=text,
        skill_name=runtime.skill_name,
        stage_name=runtime.stage_name,
        probable_severity_range="unclear",
        submission_blockers=[
            "需要接入真实样本数据和 source-backed 聚合逻辑",
        ],
        false_positive_risks=(
            ["需要单独检查 privileged misconfiguration 和 unsupported-by-design 风险"]
            if runtime.require_false_positive_check
            else []
        ),
        validation_gap="尚未接入真实 case / pattern / validation recipe 数据",
        next_validation_steps=[
            "补充手工样本数据",
            "实现最小 lexical retrieval",
            "分离正向匹配与 caution 通道",
        ],
        sources=["local://skill-aware-triage-placeholder"],
        notes=[search_result["message"]],
    )
    return result.model_dump()
