from __future__ import annotations

import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SKILL_DOCS = {
    "c4-contest-auditor/SKILL.md": Path.home()
    / ".hermes/skills/software-development/c4-contest-auditor/SKILL.md",
    "c4-contest-auditor/references/c4-intake-notes.md": Path.home()
    / ".hermes/skills/software-development/c4-contest-auditor/references/c4-intake-notes.md",
    "audit-rag-bootstrap/SKILL.md": Path.home()
    / ".hermes/skills/software-development/audit-rag-bootstrap/SKILL.md",
}


def main() -> None:
    for relative_path, source_path in SKILL_DOCS.items():
        if not source_path.exists():
            raise FileNotFoundError(f"Missing skill markdown: {source_path}")
        target_path = REPO_ROOT / "docs" / "skills" / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        print(f"synced {source_path} -> {target_path}")


if __name__ == "__main__":
    main()
