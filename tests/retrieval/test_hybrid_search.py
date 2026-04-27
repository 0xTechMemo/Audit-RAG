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


def test_strict_runtime_keeps_evm_query_out_of_known_soroban_records() -> None:
    result = hybrid_search(
        "ERC4626 donation manipulates share price and causes minShares deposit denial of service",
        QueryContext(ecosystem="evm", language="solidity", runtime="evm", strict_runtime=True),
    )

    assert result["strict_runtime"] is True
    assert result["ecosystem"] == "evm"
    ids = [item["id"] for item in result["positive_matches"]]
    assert "erc4626-share-inflation-donation-pattern" in ids
    assert not any("blend-v2" in item_id for item_id in ids)


def test_strict_runtime_prioritizes_stellar_soroban_records() -> None:
    result = hybrid_search(
        "Soroban Rust duplicate reserve Vec entries overprice bad debt auction",
        QueryContext(ecosystem="stellar", language="rust-soroban", runtime="soroban", strict_runtime=True),
    )

    assert result["strict_runtime"] is True
    ids = [item["id"] for item in result["positive_matches"]]
    assert ids[:2] == [
        "c4-2025-02-blend-v2-m-04",
        "soroban-duplicate-asset-list-pricing-pattern",
    ]
    assert all("solidity" not in item["runtime_metadata"]["languages"] for item in result["positive_matches"])
