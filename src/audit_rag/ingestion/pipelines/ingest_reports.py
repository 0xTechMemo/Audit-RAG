from __future__ import annotations

from pathlib import Path


def run_ingest(source_dir: str | Path) -> None:
    source_path = Path(source_dir)
    print(f"[TODO] ingest reports from {source_path}")
