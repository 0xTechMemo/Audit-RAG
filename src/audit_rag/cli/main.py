from __future__ import annotations

import typer
from audit_rag.ingestion.pipelines.ingest_reports import run_ingest
from audit_rag.quality.data_quality import validate_normalized_data
from audit_rag.retrieval.issue_triage import triage_issue
from audit_rag.services.output_formatter import to_pretty_json

app = typer.Typer(help="audit-rag CLI")


@app.command()
def ingest(source_dir: str) -> None:
    """Ingest raw report sources."""
    run_ingest(source_dir)


@app.command("triage-issue")
def triage_issue_cmd(text: str) -> None:
    """Triage a candidate issue statement."""
    result = triage_issue(text)
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
