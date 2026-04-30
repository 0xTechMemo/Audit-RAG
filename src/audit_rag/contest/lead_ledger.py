from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

_REPO_ROOT = Path(__file__).resolve().parents[3]
_PROVISIONAL_DIR = _REPO_ROOT / "data" / "provisional" / "contests"

LEAD_STATUSES = {
    "new",
    "investigating",
    "needs-poc",
    "poc-passed",
    "duplicate",
    "false-positive",
    "qa-low",
    "submission-ready",
    "suppressed",
    "abandoned",
}


class LeadRecord(BaseModel):
    id: str
    contest_slug: str
    title: str
    text: str
    status: str = "new"
    component: str | None = None
    files: list[str] = Field(default_factory=list)
    functions: list[str] = Field(default_factory=list)
    severity_guess: str = "unclear"
    current_blocker: str | None = None
    duplicate_check: str | None = None
    false_positive_risk: str | None = None
    validation_command: str | None = None
    poc_path: str | None = None
    related_rag_cases: list[str] = Field(default_factory=list)
    related_rag_patterns: list[str] = Field(default_factory=list)
    rag_triage_path: str | None = None
    final_decision: str | None = None
    created_at: str
    updated_at: str


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return slug[:80] or "lead"


def contest_dir(contest_slug: str) -> Path:
    return _PROVISIONAL_DIR / contest_slug


def ledger_path(contest_slug: str) -> Path:
    return contest_dir(contest_slug) / "lead-ledger.jsonl"


def rag_triage_dir(contest_slug: str) -> Path:
    return contest_dir(contest_slug) / "rag-triage"


def load_leads(contest_slug: str) -> list[LeadRecord]:
    path = ledger_path(contest_slug)
    if not path.exists():
        return []
    leads: list[LeadRecord] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        leads.append(LeadRecord.model_validate(json.loads(line)))
    return leads


def save_leads(contest_slug: str, leads: list[LeadRecord]) -> Path:
    path = ledger_path(contest_slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(
        json.dumps(lead.model_dump(), ensure_ascii=False, sort_keys=True) for lead in leads
    )
    if content:
        content += "\n"
    path.write_text(content, encoding="utf-8")
    return path


def _next_id(existing: list[LeadRecord], title: str) -> str:
    base = slugify(title)
    existing_ids = {lead.id for lead in existing}
    if base not in existing_ids:
        return base
    index = 2
    while f"{base}-{index}" in existing_ids:
        index += 1
    return f"{base}-{index}"


def add_lead(
    contest_slug: str,
    title: str,
    text: str | None = None,
    component: str | None = None,
    files: list[str] | None = None,
    functions: list[str] | None = None,
    severity_guess: str = "unclear",
    status: str = "new",
) -> dict[str, Any]:
    if status not in LEAD_STATUSES:
        raise ValueError(f"unsupported lead status: {status}")
    leads = load_leads(contest_slug)
    timestamp = now_iso()
    lead = LeadRecord(
        id=_next_id(leads, title),
        contest_slug=contest_slug,
        title=title,
        text=text or title,
        status=status,
        component=component,
        files=files or [],
        functions=functions or [],
        severity_guess=severity_guess,
        created_at=timestamp,
        updated_at=timestamp,
    )
    leads.append(lead)
    path = save_leads(contest_slug, leads)
    return {"status": "ok", "action": "add-lead", "ledger_path": str(path), "lead": lead.model_dump()}


def update_lead(contest_slug: str, lead_id: str, updates: dict[str, Any]) -> LeadRecord:
    leads = load_leads(contest_slug)
    for index, lead in enumerate(leads):
        if lead.id != lead_id:
            continue
        data = lead.model_dump()
        data.update({key: value for key, value in updates.items() if value is not None})
        if data.get("status") not in LEAD_STATUSES:
            raise ValueError(f"unsupported lead status: {data.get('status')}")
        data["updated_at"] = now_iso()
        updated = LeadRecord.model_validate(data)
        leads[index] = updated
        save_leads(contest_slug, leads)
        return updated
    raise KeyError(f"lead not found: {lead_id}")


def get_lead(contest_slug: str, lead_id: str) -> LeadRecord:
    for lead in load_leads(contest_slug):
        if lead.id == lead_id:
            return lead
    raise KeyError(f"lead not found: {lead_id}")


def list_leads(contest_slug: str, status: str | None = None) -> dict[str, Any]:
    leads = load_leads(contest_slug)
    if status:
        leads = [lead for lead in leads if lead.status == status]
    return {
        "status": "ok",
        "contest_slug": contest_slug,
        "ledger_path": str(ledger_path(contest_slug)),
        "count": len(leads),
        "leads": [lead.model_dump() for lead in leads],
    }


def save_triage_result(contest_slug: str, lead_id: str, result: dict[str, Any]) -> Path:
    directory = rag_triage_dir(contest_slug)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{lead_id}.json"
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return path
