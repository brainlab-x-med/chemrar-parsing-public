# -*- coding: utf-8 -*-
"""Build cohorts + medication regimens for doc 501_2 (рак вульвы, C51)."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit  # noqa: E402

DOC = "501_2"

DISEASE = {
    "name": "Злокачественное новообразование вульвы (рак вульвы, РВ)",
    "icd10": "C51 (C51.0–C51.9); D07 — карцинома in situ",
    "histology_type": "плоскоклеточный рак (основной гистологический тип)",
}

def drug(inn, dose, route, schedule, cycle_frequency=None, max_cycles=None):
    return {"inn": inn, "dose": dose, "route": route, "schedule": schedule,
            "cycle_frequency": cycle_frequency, "max_cycles": max_cycles}

def base(cid, line, ttype, name, drugs, stage, ecog=None, bio=None, uur=None, udd=None,
         refs=None, cite=None, special="", maint=None):
    return {
        "cohort_id": cid, "disease": DISEASE,
        "treatment": {"line_stage": line, "therapy_type": ttype, "regimen_name": name},
        "drugs": drugs,
        "indications": {"stage": stage, "ecog": ecog, "biomarkers": bio or []},
        "evidence": {"uur": uur, "udd": udd},
        "source": {"page": None, "section": "3.3", "table": None,
                   "references": refs or [], "citation": cite},
        "special_conditions": special,
        "maintenance_therapy": maint,
    }

cohorts = [
    {"cohort_id": "C1", "disease": DISEASE,
     "stage": "распространённый РВ: сомнительная резектабельность опухоли Ib стадии; нерезектабельные опухоли III стадии",
     "resectability": "сомнительная резектабельность / нерезектабельный",
     "clinical_situation": "неоадъювантная химиотерапия с последующей радикальной вульвэктомией либо химиолучевая терапия при неэффективности ХТ",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["неоадъювантная ХТ на основе соединений платины → вульвэктомия с пахово-бедренной лимфаденэктомией"],
     "source": {"section": "3.1.3 / 3.1.5 / 3.3"}},
    {"cohort_id": "C2", "disease": DISEASE,
     "stage": "метастатический или рецидивирующий РВ (IVB стадия, T1–3 N0–3 M1); рецидивы плоскоклеточного РВ",
     "resectability": None, "clinical_situation": "1-я линия системной химиотерапии метастатического/рецидивного процесса",
     "ecog": None,
     "biomarkers": ["высокий уровень микросателлитной нестабильности (MSI-H), включая нарушения системы репарации ДНК (dMMR) — для пембролизумаба"],
     "treatment_stages": ["комбинированная ХТ со соединениями платины — лечение первой линии; при рецидиве — схемы аналогичны рецидиву плоскоклеточного РШМ"],
     "source": {"section": "3.1.6 / 3.3"}},
    {"cohort_id": "C3", "disease": DISEASE,
     "stage": "местно-распространённый РВ (II–IVA стадии): II стадия (T2N0M0), III стадия нерезектабельные, IVA (T1–2N3M0, T3N0–3M0)",
     "resectability": None, "clinical_situation": "радикальная химиолучевая терапия",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["лучевая терапия с платиносодержащей сенсибилизирующей химиотерапией (как при РШМ)"],
     "source": {"section": "3.1.4–3.1.6 / 3.3"}},
]

JNVLP = "** ЖНВЛП; "
R = [
    base("C1", "неоадъювантная комбинированная химиотерапия на основе соединений платины", ["химиотерапия"],
         "Паклитаксел + цисплатин (неоадъювантная ХТ)",
         [drug("Паклитаксел", "175 мг/м²", "в/в", "1-й день", "каждые 21 день", None),
          drug("Цисплатин", "70 мг/м²", "в/в", "1-й день", "каждые 21 день")],
         "распространённый РВ, на первом этапе не подлежащий первичной операции",
         uur="C", udd=5, refs=["12", "56", "45"],
         cite="Koh W.J. et al. Vulvar Cancer, Version 2.2019, NCCN Clinical Practice Guidelines in Oncology",
         special=JNVLP + "# off-label у паклитаксела; дозировка по режиму оптимального объёма [57]"),
    base("C2", "химиотерапия минимального объёма (метастатический/рецидивный процесс)", ["химиотерапия"],
         "Цисплатин монотерапия (минимальный объём ХТ)",
         [drug("Цисплатин", "50 мг/м²", "в/в", "1-й день", "с интервалом 21 день", "4–6 курсов")],
         "распространённый РВ (аналогично ХТ при РШМ)", uur="C", udd=5, refs=["12", "59"],
         cite="Mazzotta M., Pizzuti L., Krasniqi E. et al. Role of Chemotherapy in Vulvar Cancers: Time to Revolution?",
         special=JNVLP),
    base("C2", "химиотерапия оптимального объёма (1-я линия метастатического/рецидивного процесса)", ["химиотерапия"],
         "Паклитаксел + цисплатин",
         [drug("Паклитаксел", "175 мг/м²", "в/в", "1-й день", "каждые 21 день", 6),
          drug("Цисплатин", "70 мг/м²", "в/в", "1-й день", "каждые 21 день", 6)],
         "метастатический или рецидивирующий РВ", uur="C", udd=4, refs=["12", "57"],
         cite="Raspagliesi F. et al. Role of paclitaxel and cisplatin as the neoadjuvant treatment for locally advanced squamous cell carcinoma of the vulva. J Gynecol Oncol 2014;25(1):22-29",
         special=JNVLP + "# off-label"),
    base("C2", "химиотерапия оптимального объёма (1-я линия метастатического/рецидивного процесса)", ["химиотерапия"],
         "Паклитаксел + карбоплатин",
         [drug("Паклитаксел", "175 мг/м²", "в/в", "1-й день", "каждые 21 день", 6),
          drug("Карбоплатин", "AUC 5–6", "в/в", "1-й день", "каждые 21 день", 6)],
         "метастатический или рецидивирующий РВ", uur="C", udd=4, refs=["46"],
         cite="Amant F., Nooij L., Annibali D. et al. Brief Report on 3-Weekly Paclitaxel Carboplatin Efficacy in Locally Advanced Vulvar Cancer",
         special=JNVLP + "# off-label"),
    base("C2", "химиотерапия оптимального объёма (1-я линия метастатического/рецидивного процесса)", ["химиотерапия"],
         "Паклитаксел монотерапия",
         [drug("Паклитаксел", "175 мг/м²", "в/в", "1-й день", "каждые 21 день", 6)],
         "метастатический или рецидивирующий РВ", uur="C", udd=4, refs=["47"],
         cite="Witteveen P.O. et al. Phase II study on paclitaxel in patients with recurrent, metastatic or locally advanced vulvar cancer not amenable to surgery or radiotherapy (EORTC-GCG)",
         special=JNVLP + "# off-label"),
    base("C2", "иммунотерапия (оптимальный объём лекарственного лечения)", ["иммунотерапия"],
         "Пембролизумаб монотерапия",
         [drug("Пембролизумаб", "200 мг", "в/в", None, "1 раз в 21 день")],
         "распространённый/рецидивный РВ", bio=["высокий уровень микросателлитной нестабильности (MSI-H), включая нарушения системы репарации ДНК (dMMR)"],
         uur="C", udd=4, refs=["48"],
         cite="Shields L.B.E., Gordinier M.E. Pembrolizumab in Recurrent Squamous Cell Carcinoma of the Vulva: Case Report and Review of the Literature. Gynecol Obstet Invest 2019;84(1):94-98",
         special=JNVLP + "; только при MSI-H/dMMR"),
    base("C3", "сенсибилизирующая химиотерапия на фоне лучевой терапии (радикальная химиолучевая терапия)", ["химиолучевая терапия (ХЛТ)", "химиотерапия"],
         "Цисплатин (сенсибилизирующая ХТ) на фоне лучевой терапии — как при РШМ",
         [drug("Цисплатин", None, "в/в", "на фоне дистанционной лучевой терапии", None, None)],
         "местно-распространённый РВ (II–IVA стадии), радикальная программа",
         uur="C", udd=5, refs=["12", "56", "45"],
         cite="Oonk M.H.M. et al. European Society of Gynaecological Oncology Guidelines for the Management of Patients With Vulvar Cancer. Int J Gynecol Cancer 2017;27:832Y837",
         special=JNVLP + "; конкретные дозы и график введения цисплатина в документе не приведены (режим «как при РШМ», см. КР рак шейки матки)"),
]

audit.event(DOC, "phase2-start", "501_2 рак вульвы: cohort-first extraction")
audit.read_block(DOC, "501_2.md", 317, 451, "§3.1 стадии, §3.2 ЛТ, §3.3 системная химиотерапия")
for c in cohorts:
    audit.cohort(DOC, c)
for r in R:
    audit.regimen(DOC, r)
audit.event(DOC, "phase2-done", f"{len(R)} regimens")

with open(f"output-cohort/{DOC}.cohorts.json", "w", encoding="utf-8") as f:
    json.dump(cohorts, f, ensure_ascii=False, indent=2)
with open(f"output-cohort/{DOC}.regimens.json", "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=2)

filled = {}
for r in R:
    for k in ("line_stage", "regimen_name"):
        filled.setdefault(k, []).append(bool(r["treatment"][k]))
    for dk in ("inn", "dose", "route", "schedule"):
        filled.setdefault(f"drugs.{dk}", []).extend([bool(d[dk]) for d in r["drugs"]])
    filled.setdefault("indications.stage", []).append(bool(r["indications"]["stage"]))
    for k in ("section", "references", "citation"):
        filled.setdefault(f"source.{k}", []).append(bool(r["source"][k]))

print(f"{DOC}: {len(R)} rows, {len(cohorts)} cohorts")
for k, v in filled.items():
    print(f"  {k}: {sum(v)}/{len(v)}")
