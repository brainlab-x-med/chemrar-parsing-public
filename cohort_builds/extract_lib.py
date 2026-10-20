# Shared helpers for clinrec cohort extraction pipeline (one doc = one build_<id>.py).
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit  # noqa: E402

OUT = "output-cohort"
MUST_DRUG = ("inn", "dose", "route", "schedule")


def md_path(doc_id):
    return os.path.join(OUT, f"{doc_id}.md")


def load_bib(md_path_):
    """Parse 'Список литературы' ordered list of '- ' items -> list of entries.
    Anchors on the LAST markdown HEADING named 'Список литературы' and reads
    '- ' items until the next heading."""
    with open(os.path.join(OUT, md_path_), encoding="utf-8") as f:
        txt = f.read()
    matches = list(re.finditer(r"^#{1,6}[^\n]*Список литературы[^\n]*$", txt, re.M | re.I))
    if not matches:
        return []
    tail = txt[matches[-1].end():]
    # cut off at next heading of any level
    nxt = re.search(r"^#{1,6}\s", tail, re.M)
    if nxt:
        tail = tail[:nxt.start()]
    entries = []
    for line in tail.splitlines():
        s = line.strip()
        m = re.match(r"^(?:-|\d{1,3}[.)])\s+(.{20,})$", s)
        if m:
            entries.append(m.group(1).strip())
    return entries


def clean_inn(s):
    """Strip ЖНВЛП '**' footnote marker and off-label '#' marker."""
    return re.sub(r"[#*]+", "", str(s)).replace("  ", " ").strip()


def drug(inn, dose, route=None, schedule=None, freq=None, max_cycles=None):
    return {
        "inn": clean_inn(inn),
        "dose": dose,
        "route": route,
        "schedule": schedule,
        "cycle_frequency": freq,
        "max_cycles": max_cycles,
    }


def cite_first(refs, bib):
    """Resolve FIRST reference id to full bibliography entry."""
    ids = []
    for r in refs or []:
        for part in re.findall(r"\d+", str(r)):
            ids.append(int(part))
    if not ids:
        return None
    n = ids[0]
    if 1 <= n <= len(bib):
        return bib[n - 1]
    return None


def norm_refs(refs):
    out = []
    for r in refs or []:
        out.extend(re.findall(r"\d+", str(r)))
    # dedupe preserving order
    seen, res = set(), []
    for x in out:
        if x not in seen:
            seen.add(x)
            res.append(x)
    return res


def row(doc_id, cohort_id, disease, line_stage, therapy_type, regimen_name,
        drugs, stage, section, refs, bib, table=None, ecog=None, biomarkers=None,
        uur=None, udd=None, special="", maintenance=None):
    r = {
        "cohort_id": cohort_id,
        "disease": {
            "name": disease["name"],
            "icd10": disease.get("icd10"),
            "histology_type": disease.get("histology_type"),
        },
        "treatment": {
            "line_stage": line_stage,
            "therapy_type": therapy_type if isinstance(therapy_type, list) else [therapy_type],
            "regimen_name": regimen_name,
        },
        "drugs": drugs,
        "indications": {
            "stage": stage,
            "ecog": ecog,
            "biomarkers": biomarkers if biomarkers is not None else [],
        },
        "evidence": {"uur": uur, "udd": udd},
        "source": {
            "page": None,
            "section": section,
            "table": table,
            "references": norm_refs(refs),
            "citation": cite_first(norm_refs(refs), bib),
        },
        "special_conditions": special,
        "maintenance_therapy": maintenance,
    }
    audit.regimen(doc_id, r)
    return r


def write_doc(doc_id, cohorts, regimens):
    with open(os.path.join(OUT, f"{doc_id}.cohorts.json"), "w", encoding="utf-8") as f:
        json.dump(cohorts, f, ensure_ascii=False, indent=1)
    for c in cohorts:
        cc = dict(c)
        if isinstance(cc.get("source"), str):
            cc["source"] = {"section": cc["source"]}
        audit.cohort(doc_id, cc)
    with open(os.path.join(OUT, f"{doc_id}.regimens.json"), "w", encoding="utf-8") as f:
        json.dump(regimens, f, ensure_ascii=False, indent=1)


def validate(doc_id, regimens):
    n = len(regimens)
    checks = {
        "treatment.line_stage": lambda r: bool(r["treatment"]["line_stage"]),
        "treatment.regimen_name": lambda r: bool(r["treatment"]["regimen_name"]),
        "disease.name": lambda r: bool(r["disease"]["name"]),
        "disease.icd10": lambda r: bool(r["disease"]["icd10"]),
        "disease.histology_type": lambda r: bool(r["disease"]["histology_type"]),
        "indications.stage": lambda r: bool(r["indications"]["stage"]),
        "source.section": lambda r: bool(r["source"]["section"]),
        "source.references": lambda r: bool(r["source"]["references"]),
        "source.citation": lambda r: bool(r["source"]["citation"]),
        "drugs.nonempty": lambda r: len(r["drugs"]) > 0,
        "drugs.inn": lambda r: all(d["inn"] for d in r["drugs"]),
        "drugs.dose": lambda r: bool(r["drugs"]) and all(d["dose"] for d in r["drugs"]),
        "drugs.route": lambda r: bool(r["drugs"]) and all(d["route"] for d in r["drugs"]),
        "drugs.schedule": lambda r: bool(r["drugs"]) and all(d["schedule"] for d in r["drugs"]),
    }
    print(f"== {doc_id}: {n} regimen rows ==")
    gaps = {}
    for name, fn in checks.items():
        filled = sum(1 for r in regimens if fn(r))
        rate = f"{filled}/{n}"
        print(f"  {name:26s} {rate:>8s} ({100 * filled / n:.0f}%)" if n else name)
        missing = [i for i, r in enumerate(regimens) if not fn(r)]
        if missing:
            gaps[name] = missing
    for name, miss in gaps.items():
        print(f"  GAP {name}: rows {miss[:12]}{'…' if len(miss) > 12 else ''}")
    audit.event(doc_id, "validate", f"{n} rows; gaps: " + "; ".join(f"{k}={len(v)}" for k, v in gaps.items()))
