# chemrar-pdf-parsing

Cohort-first extraction of drug regimens from Russian oncology clinical
recommendations (клинические рекомендации), per BRA-92.

The extraction is done by a Claude Code skill. It first builds the cohort tree
(`МКБ → гистология → стадия/ECOG/биомаркеры → линия → тип терапии`) and then
attaches drug regimens to it. One output row is one regimen for one cohort.

## Layout

- `.claude/skills/clinrec-cohort-extract/` — the skill.
  - `SKILL.md` — the procedure and the output JSON schema.
  - `scripts/html_to_markdown.py` — Phase 1, HTML → Markdown with image
    transcription.
  - `scripts/audit.py` — writes the per-document provenance log.
  - `scripts/log_tool_call.py` — optional hook for a raw tool-call log.
- `src/clinrec/` — the LLM client and settings that Phase 1 uses
  (`core/settings.py`, `core/logging.py`, `extraction/client.py`).
- `scripts/download_htmls.py` — fetches clinrec HTML from a configurable API.
- `cohort_builds/` — the stored Phase 2 results of the 2026-08-24 run, one
  script per document. These are not parsers; see
  [`cohort_builds/README.md`](cohort_builds/README.md).
- `format.md` — the output field list agreed with the medical expert.

## Setup

```bash
uv sync
```

Phase 1 transcribes images with `google/gemini-3.1-flash-lite` through
OpenRouter. Put the key in `.env` at the repository root:

```
OPENROUTER_API_KEY=...
```

## Usage

**0. Download HTML.** The CSV needs an `id` column with document ids. Set the
API URL as a template with an `{id}` placeholder, either in `CLINREC_API_URL` or
with `--api-url`:

```bash
export CLINREC_API_URL="https://example.org/api?id={id}"
uv run python scripts/download_htmls.py --csv document_ids.csv --out api-cached
```

The API must return JSON of the form
`{"name": ..., "obj": {"sections": [{"title": ..., "content": "<html>"}]}}`.
The script joins the sections into one HTML file per document.

**1. Phase 1, HTML → Markdown.**

```bash
uv run python .claude/skills/clinrec-cohort-extract/scripts/html_to_markdown.py api-cached/584_2.html --out-dir output-cohort
```

This writes `output-cohort/584_2.md` and caches image transcriptions in
`output-cohort/584_2.images/`, so re-runs do not call the model again.

**2. Phase 2, extraction.** In Claude Code, open this repository and ask, for
example, "извлеки когорты из 584_2", or run `/clinrec-cohort-extract`. The agent
writes:

- `output-cohort/<doc_id>.cohorts.json` — the cohort tree;
- `output-cohort/<doc_id>.regimens.json` — the regimens;
- `output-cohort/<doc_id>.extraction.log` — where each cohort and regimen came
  from.

`api-cached/` and `output-*/` are not stored in git.
