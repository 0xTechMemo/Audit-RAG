from __future__ import annotations

from audit_rag.contracts.triage import CandidateTriageOutput
from audit_rag.indexing.hybrid_search import hybrid_search
from audit_rag.retrieval.query_context import QueryContext


def _severity_range(top_match: dict | None) -> str:
    if not top_match:
        return "unclear"
    severity = top_match.get("severity")
    if severity in {"high", "medium"}:
        return severity
    return "unclear"


def triage_issue(text: str, context: QueryContext | None = None) -> dict:
    runtime = context or QueryContext()
    search_result = hybrid_search(text, runtime)
    positive_matches = search_result.get("positive_matches", [])
    caution_matches = search_result.get("caution_matches", [])
    case_matches = [m for m in positive_matches if m.get("document_type") == "case_report"]
    pattern_matches = [m for m in positive_matches if m.get("document_type") == "vulnerability_pattern"]
    top_case = case_matches[0] if case_matches else None

    false_positive_risks = [
        match.get("why_not_valid") or match.get("downgrade_reason") or match.get("title")
        for match in caution_matches[:3]
    ]
    false_positive_risks = [risk for risk in false_positive_risks if risk]

    submission_blockers = [
        "需要用当前目标仓库代码验证 reachability、权限边界和资产影响，不能只依赖历史相似案例",
    ]
    if not top_case:
        submission_blockers.append("本地 RAG 没有召回足够相似的 High/Medium 历史案例")
    if false_positive_risks:
        submission_blockers.append("需要排除 caution/false-positive 通道召回的降级条件")

    sources = [match["source"] for match in positive_matches[:5] if match.get("source")]
    sources.extend(match["source"] for match in caution_matches[:3] if match.get("source"))

    result = CandidateTriageOutput(
        issue_text=text,
        skill_name=runtime.skill_name,
        stage_name=runtime.stage_name,
        likely_root_cause=top_case.get("root_cause") if top_case else None,
        broken_invariant=(top_case.get("broken_invariants") or [None])[0] if top_case else None,
        attacker_profile="需要基于当前代码确认；历史相似案例仅提供候选攻击画像",
        matching_cases=[match["id"] for match in case_matches[:5] if match.get("id")],
        matching_patterns=[match["id"] for match in pattern_matches[:5] if match.get("id")],
        probable_severity_range=_severity_range(top_case),
        submission_blockers=submission_blockers,
        false_positive_risks=false_positive_risks,
        validation_gap="尚未把当前目标仓库的具体代码路径、PoC 和数值影响接入验证链路",
        next_validation_steps=[
            "定位当前目标仓库中与 top matched case 对应的函数和状态变量",
            "检查历史 root_cause 是否在当前代码中真实存在，而不是仅标题相似",
            "用最小 PoC 或状态转移推演证明影响与权限/时序条件",
            "对照 false_positive_risks 排除 privileged-only、unsupported-by-design、dust-loss 等降级路径",
        ],
        sources=sources,
        notes=[search_result["message"]],
    )
    return result.model_dump()
