from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class SourceTrace(BaseModel):
    source_url: str | None = None
    source_name: str | None = None
    note: str | None = None


class CaseReport(BaseModel):
    id: str
    source_type: str
    protocol_name: str
    finding_title: str
    summary: str
    root_cause: str
    severity: str
    tags: list[str] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)


class StageContext(BaseModel):
    skill_name: str = "contest-audit"
    stage_name: str = "candidate-triage"
    component_type: str | None = None
    audit_goal: str = "judge whether this lead is submission-worthy"
    require_false_positive_check: bool = True
    desired_output_schema: str = "candidate-triage-v1"
