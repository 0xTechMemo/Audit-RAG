from audit_rag.contest import lead_ledger
from audit_rag.contest.lead_ledger import add_lead, get_lead, list_leads
from audit_rag.contest.scorecard import suppress_check, triage_and_persist


def test_add_and_list_leads(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(lead_ledger, "_PROVISIONAL_DIR", tmp_path)

    result = add_lead(
        contest_slug="demo-contest",
        title="Bridge accounting clears retry state before async settlement",
        text="bridge accounting clears retry state before async settlement and funds are stuck",
        component="cross-domain-bridge",
        files=["src/Bridge.sol"],
        functions=["bridgePrincipalFromL1"],
        severity_guess="medium",
    )

    assert result["status"] == "ok"
    lead_id = result["lead"]["id"]
    listed = list_leads("demo-contest")
    assert listed["count"] == 1
    assert listed["leads"][0]["id"] == lead_id
    assert get_lead("demo-contest", lead_id).component == "cross-domain-bridge"


def test_triage_lead_persists_scorecard(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(lead_ledger, "_PROVISIONAL_DIR", tmp_path)

    added = add_lead(
        contest_slug="demo-contest",
        title="ERC4626 restricted owner bypasses withdrawal restrictions",
        text="A FULL_RESTRICTED staker can approve another account and use ERC4626 withdraw to bypass owner restrictions",
        component="staking",
    )
    lead = get_lead("demo-contest", added["lead"]["id"])

    result = triage_and_persist(lead)

    assert result["status"] == "ok"
    assert result["scorecard"]["matching_cases"]
    assert result["triage_path"].endswith(f"{lead.id}.json")
    updated = get_lead("demo-contest", lead.id)
    assert updated.rag_triage_path == result["triage_path"]
    assert updated.related_rag_cases


def test_suppress_check_returns_recommendation(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(lead_ledger, "_PROVISIONAL_DIR", tmp_path)

    added = add_lead(
        contest_slug="demo-contest",
        title="Owner misconfiguration causes unsupported token issue",
        text="owner admin misconfiguration uses unsupported token and causes only user mistake impact",
    )
    lead = get_lead("demo-contest", added["lead"]["id"])

    result = suppress_check(lead)

    assert result["status"] == "ok"
    assert result["kind"] == "suppression-check"
    assert result["recommendation"] in {
        "suppress-or-duplicate-review",
        "downgrade-to-qa-or-abandon",
        "needs-negative-case-review",
        "continue-validation",
    }
    assert result["suppression_signals"]
