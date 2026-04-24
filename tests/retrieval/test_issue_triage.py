from audit_rag.retrieval.issue_triage import triage_issue


def test_triage_issue_returns_skill_aware_shape() -> None:
    result = triage_issue("reward debt may update too late")
    assert result["query_type"] == "candidate_issue"
    assert result["skill_name"] == "contest-audit"
    assert result["stage_name"] == "candidate-triage"
    assert "false_positive_risks" in result
    assert "submission_blockers" in result
    assert "sources" in result
