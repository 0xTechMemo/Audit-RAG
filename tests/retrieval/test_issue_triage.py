from audit_rag.retrieval.issue_triage import triage_issue


def test_triage_issue_returns_skill_aware_shape() -> None:
    result = triage_issue("reward debt may update too late")
    assert result["query_type"] == "candidate_issue"
    assert result["skill_name"] == "contest-audit"
    assert result["stage_name"] == "candidate-triage"
    assert "false_positive_risks" in result
    assert "submission_blockers" in result
    assert "sources" in result


def test_triage_issue_uses_real_retrieval_matches() -> None:
    result = triage_issue(
        "A FULL_RESTRICTED staker can approve another account and use ERC4626 withdraw to bypass owner restrictions"
    )

    assert result["matching_cases"]
    assert result["matching_cases"][0] == "c4-2023-10-ethena-m-01"
    assert result["likely_root_cause"] == (
        "auth-bypass via missing owner check in ERC4626 _withdraw, allowing approval-based withdrawal to bypass FULL_RESTRICTED enforcement"
    )
    assert result["broken_invariant"]
    assert result["probable_severity_range"] == "medium"
    assert "local://case_reports/c4-2023-10-ethena-m-01" in result["sources"]
    assert not any("placeholder" in source for source in result["sources"])
