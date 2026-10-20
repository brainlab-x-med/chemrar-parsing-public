# Agentic cohort-first extraction (BRA-92)

The procedure is described in the skill
`.claude/skills/clinrec-cohort-extract/SKILL.md`. The output JSON schema is in
the "Output schema" section there. `format.md` is the field list agreed with the
medical expert; the skill schema is built from it.

## Pipeline

0. **HTML.** `scripts/download_htmls.py` fetches documents from the API set in
   `CLINREC_API_URL` (or `--api-url`) into `api-cached/<doc_id>.html`. It needs
   a CSV with an `id` column of document ids.
1. **Phase 1, HTML → Markdown.** Run
   `.claude/skills/clinrec-cohort-extract/scripts/html_to_markdown.py`.
   - Headings and **bold** are kept, because cohort markers are often bold.
   - Tables become Markdown, tagged with `<!-- section N.N -->`.
   - Embedded images (tables, Приложение Б flowcharts) are transcribed by a
     vision model (`google/gemini-3.1-flash-lite` via OpenRouter, needs
     `OPENROUTER_API_KEY` in `.env`). Transcriptions are cached in
     `output-cohort/<doc_id>.images/`.
   - Output: `output-cohort/<doc_id>.md`. The script also starts a fresh
     `<doc_id>.extraction.log`.
2. **Phase 2, agentic extraction.** The agent works over the Markdown with `grep`.
   - **Pass A:** cohort skeleton (disease, histology, stage, line), written to
     `<doc_id>.cohorts.json`.
   - **Pass B:** one row per drug regimen × cohort, linked by `cohort_id`.
   - **Pass C:** enrichment with ECOG, biomarkers, УУР/УДД and source
     (section, references, citation from the bibliography).
   - **Refine loop:** targeted greps fill empty must-have fields, up to ~8 rounds.
   - Output: `<doc_id>.regimens.json`, plus provenance in
     `<doc_id>.extraction.log` via `audit.py`.

## This directory

The build scripts are **not parsers**. They hold the agent's Phase 2 result as
Python literals. While producing the 2026-08-24 snapshot, the agent ran the
skill on each document, read the Markdown with `grep`, and then wrote a
`build_<doc_id>.py` that emits what it had extracted. The skill does not ask for
this step, so it was not done for every document (see below).

What a build script contains:

- cohorts, regimens, drugs, doses, stages, УУР/УДД and section numbers, all
  written out by hand by the agent;
- calls to `audit.py` that write provenance to `<doc_id>.extraction.log`.
  `audit.read_block(...)` only records which lines the agent read. It does not
  read them.

What a build script reads from `output-cohort/<doc_id>.md`:

- 35 of the 50 scripts read nothing from it;
- 15 scripts parse only the bibliography (`load_bib`). They turn the reference
  ids they store into citation text (`cite_first`). Ten of them use
  `extract_lib.py`; five carry their own copy of `load_bib`.

What follows from this:

- Running a build script does not re-extract anything. It writes out the stored
  result again.
- If a clinrec is updated, its build script still emits the old data. To pick
  up the new version, run the skill again.
- To fix an extraction error, edit the literal in the build script, or re-run
  the skill.

`extract_lib.py` holds the shared helpers: bibliography parsing (`load_bib`,
`cite_first`), INN cleanup, row builders, `write_doc`, and `validate`, which
reports fill rates of must-have fields.

Rebuild one document from the repository root:

```bash
python cohort_builds/build_584_2.py
```

The 15 scripts that read the bibliography need the Phase 1 output
`output-cohort/<doc_id>.md`. The other 35 run without it.

## Snapshot of 2026-08-24

The snapshot covers 66 documents, 535 cohorts and 1 727 regimens. The outputs
(`output-cohort/`) are not stored in git.

All 50 builds reproduce that snapshot byte for byte. Because the data is stored
as literals, this checks that the scripts run and that the paths to `audit.py`
resolve. It does not check extraction quality; that needs a comparison against
the documents themselves.

16 documents have no build script in the snapshot: 100_2, 116_2, 129_3, 12_3,
130_2, 131_2, 132_2, 134_2, 136_2, 137_2, 30_5, 379_4, 475_3, 515_3, 535_2,
574_1. For these the agent wrote the JSON directly. 475_3, 515_3 and 574_1 are
the pilot documents. Re-extracting any of the 16 means running the skill again.
