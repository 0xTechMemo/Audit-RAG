from __future__ import annotations

import typer
from audit_rag.ingestion.pipelines.ingest_reports import run_ingest
from audit_rag.quality.data_quality import validate_normalized_data
from audit_rag.retrieval.issue_triage import triage_issue
from audit_rag.retrieval.query_context import QueryContext
from audit_rag.services.output_formatter import to_pretty_json

app = typer.Typer(help="audit-rag CLI")


@app.command()
def ingest(source_dir: str) -> None:
    """Ingest raw report sources."""
    run_ingest(source_dir)


@app.command("triage-issue")
def triage_issue_cmd(
    text: str,
    skill_name: str = typer.Option("contest-audit", help="Workflow/skill name for retrieval context."),
    stage_name: str = typer.Option("candidate-triage", help="Audit stage name."),
    component_type: str | None = typer.Option(None, help="Optional component family, e.g. cross-domain-bridge."),
    audit_goal: str = typer.Option(
        "judge whether this lead is submission-worthy",
        help="What the triage should optimize for.",
    ),
    desired_output_schema: str = typer.Option(
        "candidate-triage-v1",
        help="Desired output contract/schema name.",
    ),
    require_false_positive_check: bool = typer.Option(
        True,
        "--false-positive-check/--no-false-positive-check",
        help="Whether to retrieve false-positive/downgrade caution matches.",
    ),
) -> None:
    """Triage a candidate issue statement."""
    context = QueryContext(
        skill_name=skill_name,
        stage_name=stage_name,
        component_type=component_type,
        audit_goal=audit_goal,
        desired_output_schema=desired_output_schema,
        require_false_positive_check=require_false_positive_check,
    )
    result = triage_issue(text, context)
    print(to_pretty_json(result))


@app.command("validate-data")
def validate_data_cmd() -> None:
    """Validate normalized RAG data schemas and quality gates."""
    result = validate_normalized_data()
    print(to_pretty_json(result))
    if result["status"] != "ok":
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
