from __future__ import annotations

import json

from typer.testing import CliRunner

from audit_rag.cli.main import app


runner = CliRunner()


def test_triage_issue_cli_passes_query_context_options() -> None:
    result = runner.invoke(
        app,
        [
            "triage-issue",
            "async CoreWriter sendAsset clears accounting before external settlement",
            "--skill-name",
            "c4-contest-auditor",
            "--stage-name",
            "candidate-triage",
            "--component-type",
            "cross-domain-bridge",
            "--audit-goal",
            "find similar bugs and downgrade risks",
            "--desired-output-schema",
            "candidate-triage-v1",
            "--no-false-positive-check",
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["skill_name"] == "c4-contest-auditor"
    assert payload["stage_name"] == "candidate-triage"
    assert payload["notes"]
    assert "0 caution matches" in payload["notes"][0]
