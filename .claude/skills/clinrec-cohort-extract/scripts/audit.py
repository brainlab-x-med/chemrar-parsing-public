"""
audit.py — structured audit logging for the extraction pipeline.

The qgrep.sh wrapper only captures shell commands. The heavy lifting of Phase 2
(reading regimen blocks, building rows, resolving citations) happens in Python /
Read and would otherwise leave no trace. Import this module from build/extraction
code so every cohort and regimen — with its grounding — lands in the same
`output-cohort/<doc_id>.extraction.log`.

Usage:
    import sys; sys.path.insert(0, ".claude/skills/clinrec-cohort-extract/scripts")
    import audit
    audit.event("574_1", "phase2-start", "reading §3.2–3.4 + Приложение Б")
    audit.read_block("574_1", "574_1.md", 525, 660, "§3.3.5 Препараты и режимы")
    for r in rows: audit.regimen("574_1", r)
    audit.event("574_1", "phase2-done", f"{len(rows)} regimens")
"""

from __future__ import annotations

import datetime
import pathlib
from typing import Any


def _append(doc_id: str, line: str, out_dir: str) -> None:
    p = pathlib.Path(out_dir) / f"{doc_id}.extraction.log"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def _ts() -> str:
    return datetime.datetime.now().strftime("%F %T")


def event(doc_id: str, kind: str, msg: str, out_dir: str = "output-cohort") -> None:
    """Free-form pipeline event (start/done/decision)."""
    _append(doc_id, f"[{_ts()}] {kind} :: {msg}", out_dir)


def read_block(doc_id: str, md_file: str, start: int, end: int, what: str,
               out_dir: str = "output-cohort") -> None:
    """Record that a span of markdown was read for extraction."""
    _append(doc_id, f"[{_ts()}] read :: {md_file} L{start}-{end} :: {what}", out_dir)


def cohort(doc_id: str, c: dict[str, Any], out_dir: str = "output-cohort") -> None:
    src = c.get("source", {})
    msg = (f"{c.get('cohort_id','?')}"
           f"{' <-'+c['parent'] if c.get('parent') else ''} | "
           f"{c.get('stage')} | {c.get('clinical_situation')} | "
           f"ecog={c.get('ecog')} bio={c.get('biomarkers')} | "
           f"sec={src.get('section')}")
    _append(doc_id, f"[{_ts()}] cohort :: {msg}", out_dir)


def regimen(doc_id: str, row: dict[str, Any], out_dir: str = "output-cohort") -> None:
    src = row.get("source", {})
    tr = row.get("treatment", {})
    drugs = ", ".join(d.get("inn", "?") for d in row.get("drugs", []))
    cite = "yes" if src.get("citation") else "no"
    msg = (f"{row.get('cohort_id','?')} | {tr.get('line_stage')} | "
           f"{tr.get('regimen_name')} | sec={src.get('section')} "
           f"refs={src.get('references')} cite={cite} "
           f"| drugs[{len(row.get('drugs', []))}]={drugs}")
    _append(doc_id, f"[{_ts()}] regimen :: {msg}", out_dir)
