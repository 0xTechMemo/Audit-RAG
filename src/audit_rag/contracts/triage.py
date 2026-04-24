from __future__ import annotations

from pydantic import BaseModel, Field


class CandidateTriageOutput(BaseModel):
    query_type: str = "candidate_issue"
    skill_name: str = "contest-audit"
    stage_name: str = "candidate-triage"
    issue_text: str
    likely_root_cause: str | None = None
    broken_invariant: str | None = None
    attacker_profile: str = "unclear"
    matching_cases: list[str] = Field(default_factory=list)
    matching_patterns: list[str] = Field(default_factory=list)
    false_positive_risks: list[str] = Field(default_factory=list)
    probable_severity_range: str = "unclear"
    submission_blockers: list[str] = Field(default_factory=list)
    validation_gap: str | None = None
    next_validation_steps: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
