# Build 88_5 (Первичный гиперпаратиреоз) — cohorts + medication regimens
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit

DOC = "88_5"
DISEASE = {
    "name": "Первичный гиперпаратиреоз (ПГПТ)",
    "icd10": "E21.0 (рак ОЩЖ — C75.0)",
    "histology_type": "аденома/гиперплазия околощитовидных желез; рак околощитовидной железы (редко)",
}

audit.event(DOC, "phase2-start", "§3 Лечение L554-672 + §7.2 рак ОЩЖ L831-832 + §7.7 тяжелая гиперкальциемия L927-932 + Список литературы")
audit.read_block(DOC, f"{DOC}.md", 554, 672, "§3.1 хирургия, §3.2 консервативное лечение (алендроновая к-та, деносумаб, цинакальцет, колекальциферол), §3.3 гиперкальциемический криз")

cohorts = [
    {"cohort_id": "C1", "disease": DISEASE,
     "stage": "Симптомный/манифестный или бессимптомный ПГПТ",
     "resectability": None,
     "clinical_situation": "Основной метод лечения — паратиреоидэктомия (ПТЭ); медикаментозная терапия — при отказе от операции, противопоказаниях или невозможности хирургического лечения",
     "ecog": None, "biomarkers": ["иПТГ повышен", "альбумин-скорректированный кальций крови"],
     "treatment_stages": ["хирургическое лечение (ПТЭ)", "послеоперационный период"], "parent": None,
     "source": {"section": "3.1"}},
    {"cohort_id": "C2", "disease": DISEASE,
     "stage": "ПГПТ с показаниями к ПТЭ либо симптомный; невозможно хирургическое лечение",
     "resectability": "неоперабельный/отказ от операции",
     "clinical_situation": "Консервативное лечение: коррекция гиперкальциемии, профилактика переломов и гиперкальциемических кризов (антирезорбтивная терапия и/или цинакальцет); при снижении МПК ≤−2,5 SD и/или низкоэнергетических переломах",
     "ecog": None, "biomarkers": [], "treatment_stages": ["консервативная терапия"], "parent": None,
     "source": {"section": "3.2"}},
    {"cohort_id": "C3", "disease": DISEASE,
     "stage": "Рак ОЩЖ (в т.ч. диссеминированная форма), C75.0",
     "resectability": None,
     "clinical_situation": "Тяжелая гиперкальциемия при раке ОЩЖ: цинакальцет — препарат первой линии при диссеминированной форме, в комбинации с бифосфонатами или деносумабом",
     "ecog": None, "biomarkers": [], "treatment_stages": ["консервативная терапия гиперкальциемии"], "parent": None,
     "source": {"section": "7.2"}},
]

CITES = {
    "113": "Witteveen J., et al. Therapy of endocrine disease: hungry bone syndrome: still a challenge in the post-operative management of primary hyperparathyroidism",
    "445": "Armstrong A.J., et al. Effect of Prophylactic Calcitriol Administration on Serum Ionized Calcium Concentrations after Parathyroidectomy",
    "269": "Marcocci C., et al. Medical management of primary hyperparathyroidism: proceedings of the fourth International Workshop",
    "272": "Leere J.S., et al. Denosumab and cinacalcet for primary hyperparathyroidism (DENOCINA): a randomised, double-blind, placebo-controlled trial",
    "299": "Shah V.N., et al. Effect of 25(OH)D replacements in patients with primary hyperparathyroidism (PHPT) and concomitant vitamin D deficiency",
    "408": "Takeuchi Y., et al. Cinacalcet hydrochloride relieves hypercalcemia in Japanese patients with parathyroid cancer",
    "411": "Thosani S. and Hu M.I. Denosumab: a new agent in the management of hypercalcemia of malignancy // Future Oncol",
}


def cite(refs):
    return CITES.get(refs[0]) if refs else None


def row(cid, line_stage, name, drugs, refs, uur, udd, section, special=""):
    return {
        "cohort_id": cid, "disease": DISEASE,
        "treatment": {"line_stage": line_stage, "therapy_type": ["лекарственная терапия"], "regimen_name": name},
        "drugs": drugs,
        "indications": {"stage": None, "ecog": None, "biomarkers": []},
        "evidence": {"uur": uur, "udd": udd},
        "source": {"page": None, "section": section, "table": None, "references": refs, "citation": cite(refs)},
        "special_conditions": special, "maintenance_therapy": None,
    }


rows = [
    row("C2", "Консервативное лечение при невозможности хирургического лечения (костные проявления)", "#Алендроновая кислота (бифосфонаты, M05BA)",
        [{"inn": "Алендроновая кислота", "dose": "10 мг ежедневно или 70 мг 1 раз в неделю", "route": "внутрь", "schedule": "ежедневно / еженедельно", "cycle_frequency": "ежедневно или еженедельно", "max_cycles": None}],
        ["269"], "B", 2, "3.2",
        special="Антирезорбтивная терапия показана при снижении МПК ≤−2,5 SD по Т-критерию и/или низкоэнергетических переломах при невозможности операции; сопоставимый с ПТЭ прирост МПК за 1–2 года"),
    row("C2", "Консервативное лечение при невозможности хирургического лечения (костные проявления)", "#Деносумаб",
        [{"inn": "Деносумаб", "dose": "60 мг", "route": "п/к", "schedule": "1 введение каждые 6 месяцев", "cycle_frequency": "1 раз в 6 месяцев", "max_cycles": None}],
        ["269"], "B", 2, "3.2",
        special="# off-label; эффективность показана в РКИ 3 фазы DENOCINA независимо от сочетанной терапии цинакальцетом; преимущество перед бифосфонатами по приросту МПК в кортикальной кости и отсутствие ограничений по СКФ"),
    row("C2", "Консервативное лечение при невозможности хирургического лечения (коррекция гиперкальциемии)", "#Цинакальцет",
        [{"inn": "Цинакальцет", "dose": "30–120 мг/сут (дозы в исследованиях; титрация по кальциемии)", "route": "внутрь", "schedule": "ежедневно", "cycle_frequency": "ежедневно", "max_cycles": "эффект сохраняется до 5 лет; после отмены кальций возвращается к исходному"}],
        ["269"], "B", 2, "3.2",
        special="Нормализация кальциемии у 70–80% пациентов; напрямую не влияет на МПК и маркеры костной резорбции; для значимого эффекта могут требоваться высокие дозы (до 90 мг × 2 раза в сутки)"),
    row("C1", "Дооперационный этап (при уровне кальция <3 ммоль/л) и после ПТЭ", "#Колекальциферол (восполнение дефицита витамина D)",
        [{"inn": "Колекальциферол", "dose": "насыщающие дозировки до 100000 МЕ в неделю (мета-анализ наблюдательных исследований); в РКИ — 2800 МЕ/сут в течение 6 месяцев до и после операции", "route": "внутрь", "schedule": "ежедневно/еженедельно; цель — уровень 25(ОН)D не менее 20 нг/мл (оптимум >30 нг/мл)", "cycle_frequency": "ежедневно или еженедельно", "max_cycles": "до достижения целевого уровня 25(ОН)D"}],
        ["299"], "A", 2, "3.2",
        special="# off-label (высокие дозы); при уровне кальция >3 ммоль/л (>12 мг/дл) восполнение дефицита витамина D до успешной ПТЭ НЕ рекомендуется из-за отсутствия данных о безопасности; прием колекальциферола от 2 недель до 2 месяцев перед ПТЭ снижает риск послеоперационной гипокальциемии в 2–33 раза"),
    row("C1", "Послеоперационный период (профилактика/лечение гипокальциемии)", "Витамин D и его аналоги ± препараты кальция",
        [{"inn": "Витамин D (колекальциферол и аналоги)", "dose": None, "route": "внутрь", "schedule": "всем пациентам с симптомным ПГПТ после ПТЭ; препараты кальция добавляются при клинических проявлениях гипокальциемии и/или альбумин-скорректированном кальции <2,1 ммоль/л (ионизированном <1,0 ммоль/л)", "cycle_frequency": "ежедневно", "max_cycles": "до нормализации кальциемии (может сохраняться несколько месяцев)"}],
        ["113", "445"], "A", 2, "3.1",
        special="ГЭП: конкретные дозировки витамина D/кальция для послеоперационного периода даны отсылкой к разделу 7.6; необходима коррекция дефицита магния"),
    row("C3", "Тяжелая гиперкальциемия при раке ОЩЖ (первая линия при диссеминированной форме)", "#Цинакальцет (± бифосфонаты/#деносумаб)",
        [{"inn": "Цинакальцет", "dose": "до 360 мг/сут при необходимости", "route": "внутрь", "schedule": "ежедневно, титрация по кальциемии", "cycle_frequency": "ежедневно", "max_cycles": "длительная терапия"},
         {"inn": "Деносумаб", "dose": "120 мг", "route": "п/к", "schedule": "1 раз в 28 дней (режим для коррекции гиперкальциемии при раке ОЩЖ)", "cycle_frequency": "1 раз в 28 дней", "max_cycles": None}],
        ["408", "411"], "C", 4, "7.2",
        special="# off-label; оценка эффективности — по кальциемии, а не уровню иПТГ; деносумаб предпочтительнее в/в бифосфонатов у пациентов с ХБП (отсутствие нефротоксичности)"),
]

for r in rows:
    r["indications"]["stage"] = {
        "C1": "ПГПТ (симптомный или бессимптомный; гиперкальциемический/нормокальциемический вариант)",
        "C2": "ПГПТ при наличии показаний к ПТЭ, но невозможности/отказе от хирургического лечения",
        "C3": "Рак ОЩЖ (C75.0), в т.ч. диссеминированная форма; тяжелая гиперкальциемия",
    }[r["cohort_id"]]

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
