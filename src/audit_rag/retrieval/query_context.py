from __future__ import annotations

from pydantic import BaseModel


class QueryContext(BaseModel):
    skill_name: str = "contest-audit"
    stage_name: str = "candidate-triage"
    component_type: str | None = None
    ecosystem: str | None = None
    language: str | None = None
    runtime: str | None = None
    strict_runtime: bool = False
    audit_goal: str = "judge whether this lead is submission-worthy"
    require_false_positive_check: bool = True
    desired_output_schema: str = "candidate-triage-v1"
