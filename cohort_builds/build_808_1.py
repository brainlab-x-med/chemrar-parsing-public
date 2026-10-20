# Build 808_1 (Первичный плазмоклеточный лейкоз) — cohorts + medication regimens
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit

DOC = "808_1"
DISEASE = {
    "name": "Первичный плазмоклеточный лейкоз",
    "icd10": "C90.1",
    "histology_type": "плазмоклеточная неоплазия (клональная плазматическая клетка; клинический вариант множественной миеломы с циркуляцией ≥5% плазматических клеток в периферической крови)",
}

audit.event(DOC, "phase2-start", "§3 Лечение L215-320 + Приложение А3.1 схемы ЛТ L550-598 + Список литературы")
audit.read_block(DOC, f"{DOC}.md", 215, 320, "§3.1-3.4: стратегия, индукция, ТГСК, консолидация, поддерживающая терапия, рецидивы")
audit.read_block(DOC, f"{DOC}.md", 550, 598, "Приложение А3.1: дозы VRD/VCD/PAD/Dara-CVRd/Rd/KRd/Dara-KRd/Isa-KRd")

cohorts = [
    {"cohort_id": "C1", "disease": DISEASE, "stage": None,
     "resectability": None,
     "clinical_situation": "Впервые диагностированный ПКЛ, кандидаты на ауто-ТГСК: возраст <65 лет (или 65–70 лет с хорошим соматическим статусом без тяжелых сопутствующих заболеваний)",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["индукционная терапия", "ВДХТ с ауто-ТГСК", "консолидирующая терапия", "поддерживающая терапия"],
     "parent": None, "source": {"section": "3.2"}},
    {"cohort_id": "C2", "disease": DISEASE, "stage": None,
     "resectability": None,
     "clinical_situation": "Впервые диагностированный ПКЛ, не кандидаты на ауто-ТГСК: возраст ≥65 лет или молодые пациенты с клинически значимыми сопутствующими заболеваниями",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["индукционная терапия без ВДХТ/ТГСК", "поддерживающая терапия"],
     "parent": None, "source": {"section": "3.2"}},
    {"cohort_id": "C3", "disease": DISEASE, "stage": None,
     "resectability": None,
     "clinical_situation": "Рецидив/рефрактерный ПКЛ: лечение по принципам рефрактерных/рецидивных форм ММ высокого риска; при позднем рецидиве (>12 мес) возможно возобновление первичной терапии",
     "ecog": None, "biomarkers": [], "treatment_stages": ["противорецидивная терапия"], "parent": None,
     "source": {"section": "3.4"}},
]

CITES = {
    "19": "Gavriatopoulou M. et al. European myeloma network recommendations on diagnosis and management of patients with rare plasma cell dyscrasias // Leukemia. 2018. Vol. 32. P. 1883–1898",
    "29": "Royer B. et al. Bortezomib, Doxorubicin, Cyclophosphamide, Dexamethasone Induction Followed by Stem Cell Transplantation for Primary Plasma Cell Leukemia: A Prospective Phase II Study of the Intergroupe Francophone du Myélome // J. Clin. Oncol. 2016. Vol. 34, № 18. P. 2125–2132",
    "34": "Telek B. et al. Effective PAD (bortezomib, doxorubicine, dexamethasone) treatment of a patient with plasma cell leukaemia developed after autologous stem cell transplantation // Orv. Hetil. 2008. Vol. 149, № 41. P. 1957–1959",
    "35": "Musto P. et al. Lenalidomide and low-dose dexamethasone for newly diagnosed primary plasma cell leukemia // Leukemia. 2013. Vol. 28, № 1. P. 222–225",
    "36": "van de Donk N.W.C.J. et al. Treatment of primary plasma cell leukaemia with carfilzomib and lenalidomide-based therapy (EMN12/HOVON-129): final analysis of a non-randomised, multicentre, phase 2 study // Lancet Oncol. 2023. Vol. 24, № 10. P. 1119–1133",
    "37": "Kaiser M.F. et al. Daratumumab, Cyclophosphamide, Bortezomib, Lenalidomide, and Dexamethasone as Induction and Extended Consolidation Improves Outcome in Ultra-High-Risk Multiple Myeloma // J. Clin. Oncol. 2023. Vol. 41, № 23. P. 3945–3955",
    "38": "Lawless S. et al. Comparison of autologous and allogeneic hematopoietic cell transplantation strategies in patients with primary plasma cell leukemia // Haematologica. 2023. Vol. 108, № 4. P. 1105–1114",
    "40": "Derman B.A. et al. Final analysis of a phase II trial of daratumumab, carfilzomib, lenalidomide, and dexamethasone in newly diagnosed multiple myeloma without transplant // Blood Cancer J. 2024. Vol. 14, № 1",
    "41": "Leypoldt L.B. et al. Isatuximab, carfilzomib, lenalidomide, and dexamethasone (Isa-KRd) in front-line treatment of high-risk multiple myeloma: interim analysis of the GMMG-CONCEPT trial // Leukemia. 2022. Vol. 36, № 3. P. 885–888",
}


def cite(refs):
    return CITES.get(refs[0]) if refs else None


def row(cid, line_stage, therapy_type, name, drugs, refs, uur, udd, section,
        special="", maint=None):
    # Для первичного ПКЛ системы стадирования не разработаны (§1.5); применяются
    # системы стадирования ММ (ISS/R-ISS/R2-ISS) — указывается как контекст.
    stage = "Первичный ПКЛ (стадии не применимы; для стратификации используются ISS/R-ISS/R2-ISS по ММ)"
    return {
        "cohort_id": cid,
        "disease": DISEASE,
        "treatment": {"line_stage": line_stage, "therapy_type": therapy_type, "regimen_name": name},
        "drugs": drugs,
        "indications": {"stage": stage, "ecog": None, "biomarkers": []},
        "evidence": {"uur": uur, "udd": udd},
        "source": {"page": None, "section": section, "table": "Приложение А3.1 Схемы лекарственного лечения первичного плазмоклеточного лейкоза",
                   "references": refs, "citation": cite(refs)},
        "special_conditions": special,
        "maintenance_therapy": maint,
    }


rows = [
    row("C1", "Индукционная терапия (впервые диагностированный ПКЛ)", ["химиотерапия", "иммунотерапия"], "VRd (#бортезомиб/#леналидомид/#дексаметазон)",
        [{"inn": "Бортезомиб", "dose": "1,3 мг/м²", "route": "п/к", "schedule": "дни 1, 4, 8, 11", "cycle_frequency": "цикл 21 день (лечение возобновляется на 22-й день)", "max_cycles": None},
         {"inn": "Леналидомид", "dose": "25 мг", "route": "внутрь", "schedule": "дни 1–14", "cycle_frequency": "цикл 21 день", "max_cycles": None},
         {"inn": "Дексаметазон", "dose": "20 мг", "route": "внутрь", "schedule": "дни 1, 2, 4, 5, 8, 9, 11, 12 каждого цикла", "cycle_frequency": "цикл 21 день", "max_cycles": None}],
        ["19", "31", "33"], "B", 4, "3.2.1"),
    row("C1", "Индукционная терапия (впервые диагностированный ПКЛ)", ["химиотерапия"], "VCd (#бортезомиб/#циклофосфамид/#дексаметазон)",
        [{"inn": "Бортезомиб", "dose": "1,3 мг/м²", "route": "п/к или в/в", "schedule": "дни 1, 4, 8, 11", "cycle_frequency": "цикл 21 день (лечение возобновляется на 22-й день)", "max_cycles": None},
         {"inn": "Циклофосфамид", "dose": "300 мг/м²", "route": "в/в капельно", "schedule": "дни 1, 8", "cycle_frequency": "цикл 21 день", "max_cycles": None},
         {"inn": "Дексаметазон", "dose": "40 мг", "route": "в/в капельно или внутрь", "schedule": "дни 1, 4, 8, 11", "cycle_frequency": "цикл 21 день", "max_cycles": None}],
        ["29"], "B", 4, "3.2.1"),
    row("C1", "Индукционная терапия (впервые диагностированный ПКЛ)", ["химиотерапия"], "PAd (#бортезомиб/#доксорубицин пегилированный/#дексаметазон)",
        [{"inn": "Бортезомиб", "dose": "1,3 мг/м²", "route": "п/к или в/в", "schedule": "дни 1, 4, 8, 11", "cycle_frequency": "цикл 21 день (лечение возобновляется на 22-й день)", "max_cycles": None},
         {"inn": "Доксорубицин пегилированный", "dose": "30 мг/м²", "route": "в/в", "schedule": "день 4", "cycle_frequency": "цикл 21 день", "max_cycles": None},
         {"inn": "Дексаметазон", "dose": "40 мг", "route": "в/в капельно или внутрь", "schedule": "дни 1, 4, 8, 11", "cycle_frequency": "цикл 21 день", "max_cycles": None}],
        ["29", "34"], "B", 4, "3.2.1",
        special="Во всех схемах на основе бортезомиба оптимальным является подкожное введение бортезомиба; при клинически значимой кардиальной патологии антрациклины исключаются из терапии"),
    row("C2", "Индукционная терапия (впервые диагностированный ПКЛ)", ["химиотерапия"], "Rd (#леналидомид/#дексаметазон)",
        [{"inn": "Леналидомид", "dose": "25 мг", "route": "внутрь", "schedule": "дни 1–21", "cycle_frequency": "цикл 28 дней (лечение возобновляется на 29-й день)", "max_cycles": None},
         {"inn": "Дексаметазон", "dose": "40 мг", "route": "внутрь", "schedule": "дни 1, 8, 15, 22", "cycle_frequency": "цикл 28 дней", "max_cycles": None}],
        ["35"], "B", 3, "3.2.1"),
    row("C2", "Индукционная терапия (впервые диагностированный ПКЛ)", ["химиотерапия"], "KRd (#карфилзомиб/#леналидомид/#дексаметазон)",
        [{"inn": "Карфилзомиб", "dose": "36 мг/м²", "route": "в/в", "schedule": "дни 1, 2, 8, 9, 15, 16", "cycle_frequency": "цикл 28 дней (лечение возобновляется на 29-й день)", "max_cycles": None},
         {"inn": "Леналидомид", "dose": "25 мг", "route": "внутрь", "schedule": "дни 1–21", "cycle_frequency": "цикл 28 дней", "max_cycles": None},
         {"inn": "Дексаметазон", "dose": "20 мг", "route": "внутрь", "schedule": "дни 1, 2, 8, 9, 15, 16, 22, 23", "cycle_frequency": "цикл 28 дней", "max_cycles": None}],
        ["36"], "B", 3, "3.2.1"),
    row("C1", "Индукционная и консолидирующая многокомпонентная терапия", ["химиотерапия", "иммунотерапия"], "Dara-CVRd (#даратумумаб/#циклофосфамид/#бортезомиб/#леналидомид/#дексаметазон)",
        [{"inn": "Даратумумаб", "dose": "16 мг/кг", "route": "в/в", "schedule": "дни 1, 8, 15 в первые 2 курса, затем в день 1 с 3-го по 6-й курс", "cycle_frequency": "цикл 21 день", "max_cycles": None},
         {"inn": "Циклофосфамид", "dose": "500 мг", "route": "внутрь", "schedule": "дни 1, 8", "cycle_frequency": "цикл 21 день", "max_cycles": None},
         {"inn": "Бортезомиб", "dose": "1,3 мг/м²", "route": "п/к", "schedule": "дни 1, 4, 8, 11", "cycle_frequency": "цикл 21 день", "max_cycles": None},
         {"inn": "Леналидомид", "dose": "25 мг", "route": "внутрь", "schedule": "дни 1–14", "cycle_frequency": "цикл 21 день", "max_cycles": None},
         {"inn": "Дексаметазон", "dose": "40 мг", "route": "внутрь", "schedule": "дни 1, 4, 8, 11", "cycle_frequency": "цикл 21 день", "max_cycles": None}],
        ["35", "37"], "B", 3, "3.2.1",
        maint="Многокомпонентная таргетная поддерживающая терапия после индукции/ауто-ТГСК (УУР C, УДД 4); мобилизацию ГСК у кандидатов на ауто-ТГСК проводить после 4 циклов при достижении ремиссии"),
    row("C1", "Индукционная и консолидирующая многокомпонентная терапия", ["химиотерапия", "иммунотерапия"], "Dara-KRd (#даратумумаб/#карфилзомиб/#леналидомид/#дексаметазон)",
        [{"inn": "Даратумумаб", "dose": "16 мг/кг", "route": "в/в", "schedule": "1 раз в неделю в 1–2-м курсах, 1 раз в 2 недели с 3-го по 8-й курс, 1 раз в 4 недели с 9-го по 24-й курс", "cycle_frequency": "цикл 28 дней", "max_cycles": 24},
         {"inn": "Карфилзомиб", "dose": "20 мг/м² в дни 1, 2 в 1-м курсе, затем 36 мг/м² (дни 8, 9, 15, 16 в 1-м курсе; дни 1, 2, 8, 9, 15, 16 в курсах 2–8; дни 1, 2, 15, 16 с 9-го курса)", "route": "в/в", "schedule": "см. schedule", "cycle_frequency": "цикл 28 дней", "max_cycles": 24},
         {"inn": "Леналидомид", "dose": "25 мг", "route": "внутрь", "schedule": "дни 1–21, суммарно 24 курса", "cycle_frequency": "цикл 28 дней", "max_cycles": 24},
         {"inn": "Дексаметазон", "dose": "40 мг (курсы 1–8), затем 20 мг (курсы 9–24)", "route": "внутрь", "schedule": "дни 1, 8, 15, 22", "cycle_frequency": "цикл 28 дней", "max_cycles": 24}],
        ["38", "39"], "C", 5, "3.2.1"),
    row("C1", "Индукционная и консолидирующая многокомпонентная терапия", ["химиотерапия", "иммунотерапия"], "Isa-KRd (#изатуксимаб/#карфилзомиб/#леналидомид/#дексаметазон)",
        [{"inn": "Изатуксимаб", "dose": "10 мг/кг", "route": "в/в", "schedule": "дни 1, 8, 15, 22 в 1-м курсе; затем дни 1 и 15 последующих курсов", "cycle_frequency": "цикл 28 дней", "max_cycles": None},
         {"inn": "Карфилзомиб", "dose": "вариант 1: 20 мг/м² дни 1, 2 в 1-м курсе, далее 36 мг/м² (дни 8, 9, 15, 16 в 1-м курсе; дни 1, 2, 8, 9, 15, 16 далее); вариант 2: 20 мг/м² день 1 в 1-м курсе, далее 56 мг/м² дни 8, 15 (1-й курс), затем дни 1, 8, 15", "route": "в/в", "schedule": "по выбранному варианту введения", "cycle_frequency": "цикл 28 дней", "max_cycles": None},
         {"inn": "Леналидомид", "dose": "25 мг", "route": "внутрь", "schedule": "дни 1–21", "cycle_frequency": "цикл 28 дней", "max_cycles": None},
         {"inn": "Дексаметазон", "dose": "40 мг", "route": "внутрь или в/в", "schedule": "дни 1, 8, 15, 22", "cycle_frequency": "цикл 28 дней", "max_cycles": None}],
        ["41", "42", "43"], "C", 5, "3.2.1"),
    row("C1", "Трансплантационный этап: ВДХТ с ауто-ТГСК", ["высокодозная химиотерапия"], "Высокодозный мелфалан (кондиционирование)",
        [{"inn": "Мелфалан", "dose": "140–200 мг/м² (при СКФ <30 мл/мин без гемодиализа, возрасте 65–70 лет или программном гемодиализе — 140 мг/м²)", "route": "в/в", "schedule": "кондиционирование перед трансфузией ауто-ГСК; интервал от сбора ГСК до кондиционирования 2–4 нед.", "cycle_frequency": "однократно", "max_cycles": 1}],
        ["19", "31", "49", "50"], "B", 3, "3.2.2",
        special="При программном гемодиализе гемодиализ проводится в −4-й, −2-й (перед введением мелфалана) и 0-й день (перед трансфузией лейкоконцентрата); рекомендуется сбор ГСК, достаточный для двух трансплантаций"),
]

with open(f"output-cohort/{DOC}.cohorts.json", "w", encoding="utf-8") as f:
    json.dump(cohorts, f, ensure_ascii=False, indent=2)
with open(f"output-cohort/{DOC}.regimens.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

for c in cohorts:
    audit.cohort(DOC, c)
for r in rows:
    audit.regimen(DOC, r)
audit.event(DOC, "phase2-done", f"{len(rows)} regimens, {len(cohorts)} cohorts")

n = len(rows)


def filled(v):
    return v is not None and v != "" and v != []


checks = {
    "disease.name/icd10/histology": sum(1 for r in rows if all(filled(r["disease"].get(k)) for k in ("name", "icd10", "histology_type"))),
    "treatment.line_stage": sum(1 for r in rows if filled(r["treatment"]["line_stage"])),
    "treatment.regimen_name": sum(1 for r in rows if filled(r["treatment"]["regimen_name"])),
    "drugs.inn/dose/route/schedule": sum(1 for r in rows if all(filled(d.get(k)) for d in r["drugs"] for k in ("inn", "dose", "route", "schedule"))),
    "indications.stage": sum(1 for r in rows if filled(r["indications"]["stage"])),
    "source.section": sum(1 for r in rows if filled(r["source"]["section"])),
    "source.references": sum(1 for r in rows if filled(r["source"]["references"])),
    "source.citation": sum(1 for r in rows if filled(r["source"]["citation"])),
}
for k, v in checks.items():
    audit.event(DOC, "fill-rate", f"{k}: {v}/{n}")
print(f"{DOC}: {len(cohorts)} cohorts, {n} regimens")
for k, v in checks.items():
    print(f"  {k}: {v}/{n}")
