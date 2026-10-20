---
name: clinrec-cohort-extract
description: Agentically extract medication-treatment cohorts from a Russian oncology clinical-recommendation HTML doc (BRA-92, cohort-first). Use when asked to parse a clinrec / клинреки / клинические рекомендации HTML file into structured drug-regimen JSON, or to extract cohorts/режимы/схемы терапии from a doc in api-cached/. Triggers: "parse clinrec", "extract cohorts", "извлечь когорты/режимы", a doc id like 475_3 / 574_1 / 515_3.
---

# Clinrec cohort-first extraction (BRA-92)

Extract every **medication** treatment regimen from a Russian oncology clinical
recommendation, each tied to its patient cohort. Non-drug modalities alone (pure
surgery, pure RT with no drug) are **not** rows — but ХЛТ (chemoradiation) and
targeted/immuno are.

Approach is **cohort-first** (per BRA-92): build the cohort tree
`ICD/disease -> histology -> indications (stage + ECOG/biomarkers) -> line/stage -> therapy type -> regimen`,
then attach drug regimens to it. Work **agentically with `grep`**: query the
markdown, refine, fill fields, stop when must-have coverage stops improving.

## Inputs & outputs

- Input: an HTML file in `api-cached/<doc_id>.html` (e.g. `api-cached/475_3.html`).
- Working dir: `output-cohort/` (create if missing).
- Outputs (both under `output-cohort/`):
  - `<doc_id>.md` — Phase-1 markdown (images transcribed).
  - `<doc_id>.cohorts.json` — **Pass 2a** cohort skeleton (the cohort tree, no drugs).
  - `<doc_id>.regimens.json` — **final** result: JSON **array** of medication-regimen objects (schema below).
  - `<doc_id>.extraction.log` — clean per-doc extraction trail (Phase-1 + per-cohort/per-regimen provenance), written only by the pipeline scripts.

## Phase 1 — HTML → Markdown (images transcribed by LLM)

Images carry the tables/flowcharts (esp. **Приложение Б**), so they must be
transcribed, not dropped. Run:

```bash
uv run python .claude/skills/clinrec-cohort-extract/scripts/html_to_markdown.py \
    api-cached/<doc_id>.html --out-dir output-cohort
```

Produces `output-cohort/<doc_id>.md` with:
- headings, paragraphs, lists, `<strong>` → `**bold**` (cohort markers are bold);
- HTML tables → Markdown tables, tagged `<!-- section N.N -->`;
- each embedded image → `<!-- image K (section N) transcription start --> … end -->`
  (data-URI images transcribed via vision model; `file:///` images can't be read — skipped with a marker).

Image transcriptions are cached in `output-cohort/<doc_id>.images/` — reruns are free.
Skim the `.md` once to learn the doc's structure before extracting.

## Phase 2 — Agentic extraction (grep-driven loop)

Read `<doc_id>.md`. Then iterate. **Do not** try to one-shot it; **do not** loop forever (hard cap ~8 grep-refine rounds, or stop earlier when a round adds no new must-have fields).

**Pipeline log — the audit of *what was extracted and from where*.**
`output-cohort/<doc_id>.extraction.log` is the clean, per-doc extraction trail.
It is written **only by the pipeline scripts**, never by ad-hoc agent commands,
so it never fills with skill-editing / exploration noise:

- Phase 1 (`html_to_markdown.py`) **starts the log fresh** (one `phase1` line).
- Phase 2 emits provenance via `audit.py` — import it from your build/assembly step:
  ```python
  import sys; sys.path.insert(0, ".claude/skills/clinrec-cohort-extract/scripts")
  import audit
  audit.event(doc_id, "phase2-start", "...")
  audit.read_block(doc_id, f"{doc_id}.md", 674, 857, "§3.2–3.3 regimen blocks")
  for c in cohorts: audit.cohort(doc_id, c)
  for r in regimens: audit.regimen(doc_id, r)   # one line per regimen: cohort_id | line | name | sec | refs | cite | drugs
  audit.event(doc_id, "phase2-done", f"{len(regimens)} regimens")
  ```

The result is a deterministic, data-centric log: every cohort and every regimen
with its source section, reference ids, and whether the citation resolved —
reproducible by re-running the pipeline, independent of the agent's session
transcript (which separately records raw tool calls but is noisy and not shipped).
Your own exploration `grep`s are *not* part of this log — keep them out of it.

**Raw tool-call log (optional).** The raw log is the debug counterpart to the
clean log. It keeps one line per tool call made in the session, including the
exploration `grep`s. It is written by a Claude Code `PostToolUse` hook to
`output-cohort/raw_tool_calls.log`. The log is off by default.

To turn it on, add the hook below to `.claude/settings.local.json`. That file is
personal and not committed. If the file already has keys, merge `hooks` into
them rather than replacing the file.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/skills/clinrec-cohort-extract/scripts/log_tool_call.py\""
          }
        ]
      }
    ]
  }
}
```

The hook fires for every tool in every session in this project, not only for
extraction runs. Turn it on for debugging, then remove it. To restrict it, set
`matcher` to `"Bash|Read"` to log only greps and reads. Each line looks like
`[2026-08-24 23:41:02] Bash :: grep -niE "ECOG\s*[0-9]" output-cohort/574_1.md`.
The hook never fails a tool call. Bad input is ignored.

**The output rows are medications, not cohorts.** One row = one drug regimen
(scheme) attached to one cohort. The cohort tree built in Pass A is only the
*context* each medication regimen hangs off. A doc with 6 cohorts × ~3 regimens
each ≈ 18 rows. Pass A is cheap scaffolding; **Pass B (medications) is the bulk
of the work and where most fields live.**

### 2a — Pass A: cohort skeleton (scaffold, do first, keep short)

Build the cohort tree, nothing about drugs yet.

- **disease.name + disease.icd10**: `<h1>`/title + МКБ section. `grep -niE "C[0-9]{2}|МКБ" <doc_id>.md`
- **disease.histology_type**: anchor on the generic morphology cue (`гистолог|морфолог|тип опухоли`) and let it carry non-epithelial tumors too; the named types are just common examples, not the full set. `grep -niE "гистолог|морфолог|тип опухоли|плоскоклеточн|аденокарцином|мелкоклеточн|карцином|лимфом|сарком|меланом|герминоген|нейроэндокрин|глиом" <doc_id>.md`
- **cohorts** (stage + indications): section 3 (Лечение) headings, **Приложение Б** (transcribed images/tables), inline-bold.
  `grep -niE "стади|T[0-4][a-z]?N[0-3]|\b(I|II|III|IV)[ABC]?\b|резектабельн|метастатич|рецидив|адъювант|неоадъювант|линия" <doc_id>.md`
  (Roman-numeral alternation catches all stages I–IV — not only the advanced IV; early-stage cohorts (e.g. adjuvant for stage II) would otherwise be missed.)

Cohort layout varies by doc — don't assume one place. Check both and use whichever the doc populates:
- **Приложение Б** (transcribed flowchart/tables) — cohorts live here and point into §3 for the regimen; may span several Приложение Б tables, and the appendix can add extra stage conditions beyond TNM (e.g. resectability).
- **§3 (Лечение)** directly — stages/cohorts written inline under subsection headings, no appendix needed.
Observed examples: appendix-driven (574_1); multi-table appendix + resectability (515_3); §3-only, no appendix (475_3). Treat these as the range of layouts to expect, not a fixed map.

Result of Pass A: a short list of cohorts `{cohort_id, disease, stage, resectability, clinical_situation, ecog?, biomarkers?, treatment_stages, source}`.
**Write this skeleton to `output-cohort/<doc_id>.cohorts.json`** (array) before Pass B — it is the cohort tree the regimens attach to. Sub-cohorts (HER2+, ECOG strata, PD-L1/MSI) carry a `parent` id.

### 2b — Pass B: medication regimens (the core — re-read §3 Лечение and attach)

This is the second BRA-92 read. Go through **section 3 (Лечение)** and every
regimen table (Markdown tables + transcribed images), and for **each drug
scheme** emit one row, attaching it to the matching Pass-A cohort via
**`cohort_id`** (the id from `<doc_id>.cohorts.json` — pick the most specific
sub-cohort: HER2+/ECOG-stratum/PD-L1 over the parent). Make sure **every**
medication scheme in the doc becomes a row — sweep §3 subsections and all tables,
don't stop at the first.

Per row, extract:
- **treatment.regimen_name** — scheme name as written. Don't rely on a fixed drug/scheme whitelist (it won't generalise across nozologies); anchor on **structure + generic cues**: a regimen name sits next to its dose (the dose grep on the `drugs[]` line below) and is usually the heading/first cell of a regimen table row (see "Read drug rows out of the tables directly" below). Generic grep — latinate scheme codes (`[A-Z]{2,}` catches PF/AC/DC/TPF/FOLFOX/R-CHOP… without listing them) plus Russian scheme words and INN-near-dose:
  `grep -niE "режим|схема|курс|протокол|монотерапи|[A-Z]{2,}([ /+-][A-Z]+)*" <doc_id>.md`
  (Names like PF/FOLFOX/пембролизумаб are *examples*, not a filter — extract whatever the doc writes.)
- **drugs[]** — for **every drug** in the scheme, with all six sub-fields:
  - `inn` — МНН (generic name); strip the ЖНВЛП `**` footnote marker (`фторурацил**` → `Фторурацил`);
  - `dose` — мг/м² / AUC / мг/кг / fixed mg; capture loading+maintenance both (e.g. "400 мг/м² нагруз., затем 250 мг/м²"); normalise `мг/м2` → `мг/м²`;
  - `route` — в/в / внутрь / п/к;
  - `schedule` — days + infusion type (e.g. "1–4 дни, 96-часовая инфузия", "еженедельно", "непрерывно");
  - `cycle_frequency` — "каждые 3 недели" / "еженедельно" / "каждые 2 недели";
  - `max_cycles` — int when a count ("6 циклов"→6, "4+4"→8) or string for limits ("до прогрессирования", "max 2 года"). Per-drug, so the ХТ backbone and a continued targeted/maintenance agent can differ.
  `grep -niE "мг/м|AUC|мг/кг|в/в|внутрь|п/к|цикл|еженедельн|нед\.|сут|инфузи|до прогрессир" <doc_id>.md`
  Read drug rows out of the tables directly — a regimen table row is usually one drug.
- **treatment.therapy_type** — modality(ies): ХТ/химиотерапия, ЛТ, ХЛТ, таргетная, иммунотерапия (list, ≥1). Drop pure-surgery / pure-RT-no-drug rows.
- **treatment.line_stage** — адъювантная/неоадъювантная/периоперационная/индукционная(ИХТ)/1L/2L/3L/терапия рецидивов/отдалённых метастазов/поддерживающая (from §3 subsection heading the scheme sits under).

If a scheme appears for two cohorts, emit it twice (one row each).

### 2c — Pass C: enrich each medication row (conditions, evidence, source)

- **indications.ecog**: `grep -niE "ECOG\s*[0-9]" <doc_id>.md`. If ECOG is *inferred* (not stated for this scheme — e.g. a triplet implying good PS), keep the value but say so in-line, e.g. `"0–1 (предположительно, ...)"` — do not pass off a guess as verbatim.
- **indications.biomarkers**: spans driver mutations, fusions, receptor/IHC status, MMR — not just the head&neck set; extend per nozology. Two greps — gene/marker **codes case-sensitively** (so short codes like `ER`/`PR`/`MET` don't match Russian substrings under `-i`), Russian context words with `-i`:
  ```
  grep -nE "PD-L1|PD-1|HER2|MSI|dMMR|EGFR|ALK|ROS1|BRAF|KRAS|NRAS|NTRK|BRCA|RET|MET|CPS|TPS|\bER\b|\bPR\b" <doc_id>.md
  grep -niE "экспресси|мутаци|транслокац|амплификац|рецептор|платинорезистентн" <doc_id>.md
  ```
  §3 text often refines a cohort with a biomarker/ECOG the appendix lacked — fold it in here.
- **indications.stage**: TNM / Roman numeral / M1 for this cohort (from Приложение Б or §3 heading).
- **evidence.uur** (A/B/C) + **evidence.udd** (1–5): `grep -niE "УУР|УДД|уровень убедительности|достоверности" <doc_id>.md` — the УУР/УДД line directly under the recommendation.
- **maintenance_therapy**: `grep -niE "поддержив" <doc_id>.md`.
- **special_conditions**: free-text caveats — "неоптимальный режим", "только при противопоказаниях к …", "для пациентов с ECOG 2", etc.
- **source.section** from the nearest `<!-- section N.N -->` / heading; **source.table** = table caption / image marker if the scheme came from one; **source.page** usually null (HTML has no pages).
- **source.references**: bracketed citation numbers next to the scheme — `grep -noE "\[[0-9, –-]+\]"`.
- **source.citation** — resolve the *first* reference id to its full bibliography entry. Find Список литературы and pull the numbered line:
  `grep -niE "Список литературы" <doc_id>.md` to locate it, then read that block and match the number. Emit "Автор, журнал, год" (or the whole entry). Leave `null` only if the bibliography is absent/unparseable.

### 2d. Refine loop (minimize empty must-have fields)

Must-have fields (red/bold in spec): `disease.name`, `disease.icd10`, `disease.histology_type`,
`treatment.line_stage`, `treatment.regimen_name`,
`drugs[].{inn,dose,route,schedule}`, `indications.stage` (+ `ecog`/`biomarkers` when stated),
`source.{section,references,citation}`, `maintenance_therapy` when present.

After a first draft of the JSON array:
1. Count rows whose must-have fields are empty/null.
2. For each empty must-have, run a targeted `grep` (synonyms, nearby lines with `-A/-B`, the transcribed image blocks) to fill it.
3. Repeat. **Stop** when a round fills nothing new, or after ~8 rounds. Leave a field `null` (drug fields) or `[]` (lists) rather than inventing data — never fabricate doses/stages.

## Output schema (one object per regimen×cohort)

Nested structure. `cycle_frequency` and `max_cycles` live **inside each drug**
(drugs in one scheme can differ — e.g. ХТ stops at 6 циклов while the targeted
agent continues to progression).

```json
{
  "cohort_id": "C3",
  "disease": {
    "name": "Злокачественные новообразования губы",
    "icd10": "C00",
    "histology_type": "плоскоклеточный рак"
  },
  "treatment": {
    "line_stage": "1-я линия (метастатический/рецидивный процесс, неоперабельные опухоли)",
    "therapy_type": ["химиотерапия", "таргетная терапия"],
    "regimen_name": "PF + Cet"
  },
  "drugs": [
    {
      "inn": "Цисплатин",
      "dose": "75–100 мг/м²",
      "route": "в/в",
      "schedule": "1-й день",
      "cycle_frequency": "каждые 3 недели",
      "max_cycles": 6
    },
    {
      "inn": "Цетуксимаб",
      "dose": "400 мг/м² (нагрузочная), затем 250 мг/м²",
      "route": "в/в",
      "schedule": "еженедельно (нагрузочная доза в 1-й день 1-го цикла)",
      "cycle_frequency": "еженедельно",
      "max_cycles": "до прогрессирования или непереносимой токсичности (после 6 циклов ХТ – поддерживающая)"
    }
  ],
  "indications": {
    "stage": "IV стадия (M1; рецидивные/первично-неоперабельные, в т.ч. T4bN0–3)",
    "ecog": "0–1 (предположительно, так как для ECOG 2 есть отдельный режим Pacli+Carbo+Cet)",
    "biomarkers": []
  },
  "evidence": { "uur": "C", "udd": 2 },
  "source": {
    "page": null,
    "section": "3.3",
    "table": "Таблица №1",
    "references": ["23"],
    "citation": "Vermorken J.B., Mesia R., Rivera F. et al. Platinum-based chemotherapy plus cetuximab in head and neck cancer. N Engl J Med 2008;359:1116−27"
  },
  "special_conditions": "",
  "maintenance_therapy": "Цетуксимаб 250 мг/м² еженедельно до прогрессирования или непереносимой токсичности"
}
```

Rules: medication regimens only; one object per (regimen × cohort) — same scheme for two cohorts = two objects. Empty list → `[]`, unknown scalar → `null`. Ground every regimen in the doc (`source.section` / image marker). Inferred values (esp. `indications.ecog`) must say "предположительно" — never disguise a guess as verbatim.

## Finish

Write the regimen array to `output-cohort/<doc_id>.regimens.json` (the cohort
skeleton was already written to `<doc_id>.cohorts.json` in Pass 2a). Then report:
row count, and a per-must-have-field fill rate (e.g. "drugs.dose filled 18/20").
Flag rows still missing a must-have so the gap is visible. The clean pipeline
audit is `output-cohort/<doc_id>.extraction.log` (Phase-1 + per-cohort/per-regimen
provenance via `audit.py`).
