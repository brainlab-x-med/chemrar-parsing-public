#!/usr/bin/env python3
"""
log_tool_call.py — PostToolUse hook target. Mirrors every tool call into a
raw log file.

Claude Code passes the hook payload as JSON on stdin (tool_name, tool_input,
tool_response, cwd, session_id, ...). This appends one compact line per call to
output-cohort/raw_tool_calls.log.

NOTE: a PostToolUse hook fires for *every* tool in the session — skill edits,
exploration, everything — not just the extraction pipeline. Keep this separate
from <doc_id>.extraction.log (which stays clean, pipeline-only).

Wire it up in .claude/settings.local.json (see SKILL.md, "Raw tool-call log").
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Resolve against the repo root so the hook works from any cwd.
LOG = Path(__file__).resolve().parents[4] / "output-cohort" / "raw_tool_calls.log"


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return  # never break the tool flow

    tool = payload.get("tool_name", "?")
    inp = payload.get("tool_input", {}) or {}
    arg = (
        inp.get("command")
        or inp.get("file_path")
        or inp.get("description")
        or inp.get("skill")
        or inp.get("query")
        or ""
    )
    arg = " ".join(str(arg).split())[:160]

    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.now():%F %T}] {tool} :: {arg}\n")


if __name__ == "__main__":
    main()
