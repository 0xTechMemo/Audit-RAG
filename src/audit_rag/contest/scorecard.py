from __future__ import annotations

from typing import Any

from audit_rag.contest.lead_ledger import LeadRecord, save_triage_result, update_lead
from audit_rag.retrieval.issue_triage import triage_issue
from audit_rag.retrieval.query_context import QueryContext

BLOCKER_KEYWORDS = {
    "duplicate": ["duplicate", "known", "public", "v12", "same root cause"],
    "trusted_or_config": ["admin", "owner", "governance", "operator", "trusted", "config", "misconfiguration"],
    "user_mistake": ["user mistake", "unsupported", "stray", "dust", "wrong token", "mistaken transfer"],
    "no_impact": ["event", "temporary", "delay", "rounding dust", "no loss"],
}


def _bucket_text(text: str, words: list[str]) -> bool:
    lowered = text.lower()
    return any(word in lowered for word in words)


def _similarity_bucket(matches: list[str]) -> str:
    if len(matches) >= 2:
        return "exact-or-strong"
    if len(matches) == 1:
        return "adjacent"
    return "weak-or-none"


def _impact_shape(text: str) -> list[str]:
    lowered = text.lower()
    shapes: list[str] = []
    mapping = {
        "stuck-funds": ["stuck", "blocked", "cannot withdraw", "cannot redeem", "unavailable"],
        "direct-loss": ["steal", "theft", "loss", "drain", "compromise"],
        "bad-debt": ["bad debt", "insolvent", "underwater"],
        "accounting-mismatch": ["accounting", "debt", "principal", "index", "shares", "balance"],
        "dos": ["dos", "denial", "revert", "blocked"],
        "auth-bypass": ["auth", "authorization", "permission", "bypass", "require_auth"],
    }
    for shape, words in mapping.items():
        if any(word in lowered for word in words):
            shapes.append(shape)
    return shapes or ["unclear"]


def _suppression_signals(text: str, triage: dict[str, Any]) -> list[str]:
    combined = " ".join(
        [text]
        + triage.get("submission_blockers", [])
        + triage.get("false_positive_risks", [])
        + triage.get("next_validation_steps", [])
    )
    signals: list[str] = []
    for name, words in BLOCKER_KEYWORDS.items():
        if _bucket_text(combined, words):
            signals.append(name)
    if triage.get("false_positive_risks"):
        signals.append("false-positive-caution-present")
    if not triage.get("matching_cases"):
        signals.append("no-close-hm-history")
    return sorted(set(signals))


def build_scorecard(lead: LeadRecord, context: QueryContext | None = None) -> dict[str, Any]:
    runtime = context or QueryContext(component_type=lead.component)
    triage = triage_issue(lead.text, runtime)
    suppression = _suppression_signals(lead.text, triage)
    matching_cases = triage.get("matching_cases", [])
    matching_patterns = triage.get("matching_patterns", [])
    scorecard = {
        "lead_id": lead.id,
        "contest_slug": lead.contest_slug,
        "title": lead.title,
        "status_before": lead.status,
        "root_cause_similarity": _similarity_bucket(matching_cases),
        "pattern_similarity": _similarity_bucket(matching_patterns),
        "impact_shape": _impact_shape(lead.text),
        "probable_severity_range": triage.get("probable_severity_range", "unclear"),
        "matching_cases": matching_cases,
        "matching_patterns": matching_patterns,
        "false_positive_risks": triage.get("false_positive_risks", []),
        "suppression_signals": suppression,
        "submission_blockers": triage.get("submission_blockers", []),
        "validation_recipe": {
            "goal": "用当前目标仓库证明 reachability、权限边界、状态变化和影响，而不是只证明历史相似",
            "steps": triage.get("next_validation_steps", []),
            "minimum_assertions": [
                "当前代码路径可由有效攻击者或普通用户触发",
                "关键状态变量或资产余额出现可观测错误变化",
                "影响不是仅由 trusted-role misconfiguration、用户误操作或 unsupported token 触发",
                "若作为 HM，PoC 或状态推演能支撑 C4 severity",
            ],
        },
        "report_framing": {
            "recommended_title_shape": "[M-xx] <broken invariant> causes <concrete impact>",
            "root_cause_focus": "只链接直接造成漏洞的当前仓库代码行；历史 RAG 来源仅作内部校准",
            "avoid_claims": [
                "不要把历史相似案例当作当前漏洞证明",
                "不要扩大到 PoC 未证明的入口、资产或状态维度",
                "不要在 final submission 中写 audit-rag / V12 diligence 过程说明，除非用户要求",
            ],
        },
        "raw_triage": triage,
    }
    return {"status": "ok", "kind": "lead-triage-scorecard", "scorecard": scorecard}


def triage_and_persist(lead: LeadRecord, context: QueryContext | None = None) -> dict[str, Any]:
    result = build_scorecard(lead, context)
    path = save_triage_result(lead.contest_slug, lead.id, result)
    scorecard = result["scorecard"]
    updated = update_lead(
        lead.contest_slug,
        lead.id,
        {
            "status": "investigating" if lead.status == "new" else lead.status,
            "related_rag_cases": scorecard["matching_cases"],
            "related_rag_patterns": scorecard["matching_patterns"],
            "false_positive_risk": "; ".join(scorecard["false_positive_risks"][:3]) or None,
            "current_blocker": "; ".join(scorecard["submission_blockers"][:3]) or None,
            "rag_triage_path": str(path),
            "severity_guess": scorecard["probable_severity_range"],
        },
    )
    result["triage_path"] = str(path)
    result["updated_lead"] = updated.model_dump()
    return result


def suppress_check(lead: LeadRecord, context: QueryContext | None = None) -> dict[str, Any]:
    result = build_scorecard(lead, context)
    scorecard = result["scorecard"]
    signals = scorecard["suppression_signals"]
    if "duplicate" in signals:
        recommendation = "suppress-or-duplicate-review"
    elif any(signal in signals for signal in ["trusted_or_config", "user_mistake", "no_impact"]):
        recommendation = "downgrade-to-qa-or-abandon"
    elif "false-positive-caution-present" in signals:
        recommendation = "needs-negative-case-review"
    else:
        recommendation = "continue-validation"
    return {
        "status": "ok",
        "kind": "suppression-check",
        "lead_id": lead.id,
        "contest_slug": lead.contest_slug,
        "recommendation": recommendation,
        "suppression_signals": signals,
        "false_positive_risks": scorecard["false_positive_risks"],
        "submission_blockers": scorecard["submission_blockers"],
        "matching_cases": scorecard["matching_cases"],
        "matching_patterns": scorecard["matching_patterns"],
        "revival_conditions": [
            "找到与 known/V12 不同的 root cause 或受影响函数",
            "用当前代码 PoC 证明非 privileged、非配置错误、非用户误操作路径",
            "证明影响达到 C4 Medium/High，而不是 QA/Low 或临时延迟",
        ],
    }
