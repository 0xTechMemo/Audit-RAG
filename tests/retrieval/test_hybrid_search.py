from audit_rag.indexing.hybrid_search import hybrid_search
from audit_rag.retrieval.query_context import QueryContext


def test_hybrid_search_returns_ranked_case_reports_for_restriction_bypass() -> None:
    result = hybrid_search(
        "ERC4626 withdraw lets a FULL_RESTRICTED owner bypass restrictions through an approved caller",
        QueryContext(component_type="staking"),
    )

    assert result["status"] == "ok"
    assert result["query"]
    assert result["positive_matches"]
    top = result["positive_matches"][0]
    assert top["id"] == "c4-2023-10-ethena-m-01"
    assert top["document_type"] == "case_report"
    assert top["score"] > 0
    assert "auth-bypass" in top["root_cause"]


def test_hybrid_search_separates_false_positive_caution_channel() -> None:
    result = hybrid_search(
        "native collateral minting is unavailable but redemption still works",
        QueryContext(require_false_positive_check=True),
    )

    assert result["status"] == "ok"
    assert result["caution_matches"]
    assert result["caution_matches"][0]["document_type"] == "false_positive_case"
    assert "why_not_valid" in result["caution_matches"][0]
