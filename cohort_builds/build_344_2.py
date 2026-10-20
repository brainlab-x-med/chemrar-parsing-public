# -*- coding: utf-8 -*-
"""Build cohorts + medication regimens for doc 344_2 (рак влагалища, C52)."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit  # noqa: E402

DOC = "344_2"

DISEASE = {
    "name": "Злокачественное новообразование влагалища (рак влагалища, РВл)",
    "icd10": "C52 (D07.2 — карцинома in situ влагалища)",
    "histology_type": "плоскоклеточный рак (~90% всех гистологических типов); по МКБ ВОЗ 5-го изд. также аденокарциномы и др. эпителиальные опухоли",
}

cohorts = [
    {
        "cohort_id": "C1", "disease": DISEASE,
        "stage": "TisN0M0 (рак in situ, D07.2)",
        "resectability": None, "clinical_situation": "первичный процесс, in situ",
        "ecog": None, "biomarkers": [],
        "treatment_stages": ["локальные тактики: лазерная хирургия, широкая локальная эксцизия, фотодинамическая терапия, контактная ЛТ"],
        "source": {"section": "3.1.1"},
    },
    {
        "cohort_id": "C2", "disease": DISEASE,
        "stage": "I стадия (T1N0M0)",
        "resectability": None, "clinical_situation": "первичный процесс",
        "ecog": None, "biomarkers": [],
        "treatment_stages": ["радикальная сочетанная ЛТ (ДЛТ + брахитерапия)", "хирургическое лечение при опухоли верхней трети влагалища", "адъювантная ЛТ при факторах неблагоприятного прогноза"],
        "source": {"section": "3.1.2"},
    },
    {
        "cohort_id": "C3", "disease": DISEASE,
        "stage": "II стадия (T2N0M0)",
        "resectability": None, "clinical_situation": "местно-распространенный процесс",
        "ecog": None, "biomarkers": [],
        "treatment_stages": ["радикальная сочетанная ЛТ; радиомодификация платиносодержащей ХТ, адъювантная ХТ (см. п. 3.2)"],
        "source": {"section": "3.1.3"},
    },
    {
        "cohort_id": "C4", "disease": DISEASE,
        "stage": "III стадия (T3N0M0; T1N1M0; T2N1M0; T3N1M0)",
        "resectability": "нерезектабельный (хирургическое лечение не показано)",
        "clinical_situation": "местно-распространенный процесс",
        "ecog": None, "biomarkers": [],
        "treatment_stages": ["радикальная сочетанная ЛТ (последовательная ДЛТ + брахитерапия)"],
        "source": {"section": "3.1.4"},
    },
    {
        "cohort_id": "C5", "disease": DISEASE,
        "stage": "IVa стадия (Tлюбое Nлюбое M0)",
        "resectability": None, "clinical_situation": "местно-распространенный процесс",
        "ecog": "оценка тяжести состояния по ВОЗ/ECOG и/или шкале Карновского (см. Приложение Г1-2)",
        "biomarkers": [],
        "treatment_stages": ["условно-радикальная или паллиативная ЛТ"],
        "source": {"section": "3.1.5"},
    },
    {
        "cohort_id": "C6", "disease": DISEASE,
        "stage": "IVb стадия (Tлюбое Nлюбое M1)",
        "resectability": None, "clinical_situation": "метастатический процесс",
        "ecog": "оценка тяжести состояния по ВОЗ/ECOG и/или шкале Карновского (см. Приложение Г1-2)",
        "biomarkers": [],
        "treatment_stages": ["системная ХТ как основной метод первичного лечения; паллиативная ЛТ для облегчения симптомов; возможна регионарная ХТ"],
        "source": {"section": "3.1.6"},
    },
    {
        "cohort_id": "C7", "disease": DISEASE,
        "stage": "рецидив/диссеминация РВл",
        "resectability": None, "clinical_situation": "рецидив заболевания",
        "ecog": None, "biomarkers": [],
        "treatment_stages": ["лечение по индивидуальному плану: ХТ, варианты ЛТ по резерву толерантности с паллиативной целью; в отдельных случаях хирургия/эвисцерация таза"],
        "source": {"section": "3.1.7"},
    },
]

def drug(inn, dose, route, schedule, cycle_frequency=None, max_cycles=None):
    return {"inn": inn, "dose": dose, "route": route, "schedule": schedule,
            "cycle_frequency": cycle_frequency, "max_cycles": max_cycles}

regimens = []

# R1/R2 — химиолучевая терапия: цисплатин 40 мг/м² еженедельно на фоне ДЛТ (§3.2), off-label (#)
for cid, sec, stg in (("C3", "3.1.3 / 3.2", "II стадия (T2N0M0)"),
                      ("C4", "3.1.4 / 3.2", "III стадия (T3N0M0; T1–3N1M0)")):
    regimens.append({
        "cohort_id": cid, "disease": DISEASE,
        "treatment": {
            "line_stage": "первичное лечение местно-распространенного РВл (радиомодификация на фоне ДЛТ)",
            "therapy_type": ["химиолучевая терапия (ХЛТ)", "химиотерапия"],
            "regimen_name": "Цисплатин еженедельный на фоне дистанционной ЛТ (по аналогии с лечением местнораспространенного РШМ)",
        },
        "drugs": [drug("Цисплатин", "40 мг/м²", "в/в", "еженедельно на фоне проведения дистанционной лучевой терапии", "еженедельно", 7)],
        "indications": {"stage": stg, "ecog": None, "biomarkers": []},
        "evidence": {"uur": None, "udd": None},
        "source": {"page": None, "section": "3.2", "table": None,
                   "references": ["73"],
                   "citation": "Miyamoto D.T., Viswanathan A.N. Concurrent chemoradiation for vaginal cancer. PLoS One 2013;8:e65078"},
        "special_conditions": "# off-label (маркер # у цисплатина в тексте); режим экстраполирован с рака шейки матки из-за малого числа случаев; большие рандомизированные исследования не представлены; УУР/УДД для блока явно не указаны (у соседнего блока топометрии УУР C, УДД 5)",
        "maintenance_therapy": None,
    })

# R3 — минимальный объем ХТ (ослабленные пациенты): цисплатин 50 мг/м² q21d, до 6 курсов
regimens.append({
    "cohort_id": "C6", "disease": DISEASE,
    "treatment": {
        "line_stage": "первичная системная ХТ распространенного РВл с паллиативной целью (минимальный объем ХТ)",
        "therapy_type": ["химиотерапия"],
        "regimen_name": "Цисплатин монотерапия (минимальный объем ХТ)",
    },
    "drugs": [drug("Цисплатин", "50 мг/м²", "в/в", "1 раз в 21-й день", "каждые 21 день", 6)],
    "indications": {"stage": "IVb стадия (Tлюбое Nлюбое M1)", "ecog": None, "biomarkers": []},
    "evidence": {"uur": "C", "udd": 4},
    "source": {"page": None, "section": "3.3", "table": None,
               "references": ["32", "55", "56"],
               "citation": "Thigpen J.T., Blessing J.A., Homesley H.D. et al. Phase II trial of cisplatin in advanced or recurrent cancer of the vagina: a gynecologic oncology group study. Gynecol Oncol 1986;23(1):101−4"},
    "special_conditions": "# off-label; показан ослабленным пациентам (минимальный объем ХТ); лечение проводится до прогрессирования или непереносимой токсичности",
    "maintenance_therapy": None,
})

# R4–R7 — режимы оптимального объема ХТ (дозы — в КР по РШМ, здесь не приведены)
opt_ref = ["53", "53", "62-70"]
opt_cite = ("Shaitelman S.F., Cromwell K.D., Rasmussen J.C. et al. Recent progress in the treatment "
            "and prevention of cancer-related lymphedema. CA Cancer J Clin 2015;65(1):55−81")
opt_cond = ("# off-label; режимы оптимального объема ХТ аналогичны таковым при лечении РШМ, дозировки представлены "
            "в клинических рекомендациях по РШМ (в данном документе дозы не приведены)")
for name, drugs, ttype in (
    ("Паклитаксел + Цисплатин", ["Паклитаксел", "Цисплатин"], ["химиотерапия"]),
    ("Паклитаксел + Карбоплатин", ["Паклитаксел", "Карбоплатин"], ["химиотерапия"]),
    ("Цисплатин + Гемцитабин", ["Цисплатин", "Гемцитабин"], ["химиотерапия"]),
    ("Паклитаксел в монорежиме", ["Паклитаксел"], ["химиотерапия"]),
):
    regimens.append({
        "cohort_id": "C6", "disease": DISEASE,
        "treatment": {
            "line_stage": "первичная системная ХТ распространенного РВл с паллиативной целью (режим оптимального объема ХТ)",
            "therapy_type": ttype,
            "regimen_name": name,
        },
        "drugs": [drug(d, None, None, None, None, None) for d in drugs],
        "indications": {"stage": "IVb стадия (Tлюбое Nлюбое M1)", "ecog": None, "biomarkers": []},
        "evidence": {"uur": "C", "udd": 4},
        "source": {"page": None, "section": "3.3", "table": None,
                   "references": opt_ref, "citation": opt_cite},
        "special_conditions": opt_cond,
        "maintenance_therapy": None,
    })

# R8 — пембролизумаб (MSI-H/dMMR, рецидив)
regimens.append({
    "cohort_id": "C7", "disease": DISEASE,
    "treatment": {
        "line_stage": "терапия рецидива заболевания",
        "therapy_type": ["иммунотерапия"],
        "regimen_name": "Пембролизумаб монотерапия",
    },
    "drugs": [drug("Пембролизумаб", "200 мг", "в/в", "1 раз в 3 нед", "каждые 3 недели", "до прогрессирования или непереносимой токсичности")],
    "indications": {"stage": "прогрессирующий/рецидивный РВл",
                    "ecog": None,
                    "biomarkers": ["микросателлитная нестабильность высокого уровня (MSI-H), включая нарушения системы репарации ДНК (dMMR)"]},
    "evidence": {"uur": "C", "udd": 4},
    "source": {"page": None, "section": "3.3", "table": None,
               "references": ["69"],
               "citation": "Shields L.B.E., Gordinier M.E. Pembrolizumab in Recurrent Squamous Cell Carcinoma of the Vulva: Case Report and Review of the Literature. Gynecol Obstet Invest 2019;84(1):94−98"},
    "special_conditions": "** ЖНВЛП; только при наличии микросателлитной нестабильности высокого уровня (MSI-H)/dMMR",
    "maintenance_therapy": None,
})

# R9 — капецитабин (2-я и последующие линии)
regimens.append({
    "cohort_id": "C7", "disease": DISEASE,
    "treatment": {
        "line_stage": "2-я и последующие линии ХТ",
        "therapy_type": ["химиотерапия"],
        "regimen_name": "Капецитабин монотерапия",
    },
    "drugs": [drug("Капецитабин", "2500 мг/м²/сут", "внутрь", "1−14-й дни 21-дневного цикла", "каждые 21 день", None)],
    "indications": {"stage": "прогрессирующий/распространенный РВл", "ecog": None, "biomarkers": []},
    "evidence": {"uur": "C", "udd": 4},
    "source": {"page": None, "section": "3.3", "table": None,
               "references": ["66", "68"],
               "citation": "Garcia A.A. et al. Phase II clinical trial of capecitabine in the treatment of advanced, persistent or recurrent squamous cell carcinoma of the cervix with translational research: a gynecologic oncology group study. Gynecol Oncol 2007;104(3):572−579"},
    "special_conditions": "# off-label (** ЖНВЛП); возврат к платиносодержащей ХТ как в 1-й линии возможен при безплатиновом интервале >6 мес",
    "maintenance_therapy": None,
})

# R10 — сенсибилизирующая ХТ с ЛТ: цисплатин 40 мг/м² еженедельно до 7 циклов
regimens.append({
    "cohort_id": "C5", "disease": DISEASE,
    "treatment": {
        "line_stage": "сенсибилизирующая химиотерапия на фоне лучевой терапии (распространенный плоскоклеточный РВ)",
        "therapy_type": ["химиолучевая терапия (ХЛТ)", "химиотерапия"],
        "regimen_name": "Цисплатин еженедельный (сенсибилизирующая ХТ с ЛТ, как при плоскоклеточном раке шейки матки)",
    },
    "drugs": [drug("Цисплатин", "40 мг/м²", "в/в", "1 раз в неделю", "еженедельно", 7)],
    "indications": {"stage": "распространенный плоскоклеточный РВ (IVa стадия cohort C5; применяется с ЛТ)", "ecog": None, "biomarkers": []},
    "evidence": {"uur": "C", "udd": 4},
    "source": {"page": None, "section": "3.3", "table": None,
               "references": ["70"],
               "citation": "Rose P.G. et al. Concurrent cisplatin-based radiotherapy and chemotherapy for locally advanced cervical cancer. N Engl J Med 1999;340(15):1144−53"},
    "special_conditions": "# off-label (** ЖНВЛП); по аналогии с плоскоклеточным раком шейки матки",
    "maintenance_therapy": None,
})

audit.event(DOC, "phase2-start", "344_2 рак влагалища: cohort-first extraction")
audit.read_block(DOC, "344_2.md", 316, 445, "§3 Лечение: 3.1 стадии, 3.2 ЛТ (+ХЛТ цисплатин), 3.3 системная ХТ")
for c in cohorts:
    audit.cohort(DOC, c)
for r in regimens:
    audit.regimen(DOC, r)
audit.event(DOC, "phase2-done", f"{len(regimens)} regimens")

with open(f"output-cohort/{DOC}.cohorts.json", "w", encoding="utf-8") as f:
    json.dump(cohorts, f, ensure_ascii=False, indent=2)
with open(f"output-cohort/{DOC}.regimens.json", "w", encoding="utf-8") as f:
    json.dump(regimens, f, ensure_ascii=False, indent=2)

# must-have validation
mh = []
filled = {}
for r in regimens:
    mh.append(bool(r["disease"]["name"]) and bool(r["disease"]["icd10"]) and bool(r["disease"]["histology_type"]))
    for k in ("line_stage", "regimen_name"):
        filled.setdefault(k, []).append(bool(r["treatment"][k]))
    for dk in ("inn", "dose", "route", "schedule"):
        vals = [bool(d[dk]) for d in r["drugs"]]
        filled.setdefault(f"drugs.{dk}", []).extend(vals)
    filled.setdefault("indications.stage", []).append(bool(r["indications"]["stage"]))
    for k in ("section", "references", "citation"):
        filled.setdefault(f"source.{k}", []).append(bool(r["source"][k]))

total = len(regimens)
print(f"{DOC}: {total} rows, {len(cohorts)} cohorts")
for k, v in filled.items():
    print(f"  {k}: {sum(v)}/{len(v)}")
