# Build 80_1 (Трофобластические опухоли / ЗТО) — cohorts + medication regimens
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit

DOC = "80_1"
DISEASE = {
    "name": "Трофобластические опухоли (гестационная трофобластическая болезнь)",
    "icd10": "C58",
    "histology_type": "трофобластические неоплазии по классификации FIGO (2003): пузырный занос (полный, частичный), инвазивный/диссеминированный пузырный занос, хориокарцинома, трофобластическая опухоль плацентарного ложа, эпителиоидная трофобластическая опухоль",
}

audit.event(DOC, "phase2-start", "§3 Лечение L536-630 + таблицы 2-3 режимов ХТ + Список литературы")
audit.read_block(DOC, f"{DOC}.md", 536, 630, "§3.3 Консервативное лечение ЗТО: ХТ 1-й и 2-й линий, редкие ТО, церебральные метастазы")

cohorts = [
    {"cohort_id": "C1", "disease": DISEASE,
     "stage": "Злокачественная ТО (хориокарцинома, инвазивный пузырный занос и др.), стадия по FIGO",
     "resectability": None,
     "clinical_situation": "ЗТО низкого риска резистентности: сумма баллов по шкале FIGO-ВОЗ ≤6; химиотерапия 1-й линии до нормализации ХГЧ (<5 мМЕ/мл) + 3 консолидирующих курса (при IV стадии — 4)",
     "ecog": None, "biomarkers": ["ХГЧ сыворотки (динамический контроль, критерий излеченности ≤5 мМЕ/мл)"],
     "treatment_stages": ["ХТ 1-й линии"], "parent": None, "source": {"section": "3.3.1"}},
    {"cohort_id": "C2", "disease": DISEASE,
     "stage": "Злокачественная ТО, стадия по FIGO",
     "resectability": None,
     "clinical_situation": "ЗТО высокого риска резистентности: сумма баллов по шкале FIGO-ВОЗ ≥7; химиотерапия 1-й линии",
     "ecog": None, "biomarkers": ["ХГЧ сыворотки (контроль в 0, 7, 14, 22-й дни, еженедельно)"],
     "treatment_stages": ["ХТ 1-й линии"], "parent": None, "source": {"section": "3.3.1"}},
    {"cohort_id": "C3", "disease": DISEASE, "stage": "Резистентная ЗТО исходно низкого риска (после пересчета FIGO-ВОЗ ≤6 баллов)",
     "resectability": None,
     "clinical_situation": "Резистентность к стандартной ХТ 1-й линии; химиотерапия 2-й линии",
     "ecog": None, "biomarkers": [], "treatment_stages": ["ХТ 2-й линии"], "parent": None,
     "source": {"section": "3.3.1"}},
    {"cohort_id": "C4", "disease": DISEASE, "stage": "Резистентная ЗТО исходно высокого риска (после пересчета FIGO-ВОЗ ≥7 баллов)",
     "resectability": None,
     "clinical_situation": "Резистентность к стандартной ХТ 1-й линии; химиотерапия 2-й линии (требуется клиника с наибольшим опытом лечения)",
     "ecog": None, "biomarkers": [], "treatment_stages": ["ХТ 2-й линии"], "parent": None,
     "source": {"section": "3.3.1"}},
]

CITES = {
    "1": "Мещерякова Л.А. Злокачественные трофобластические опухоли: современная диагностика, лечение и прогноз. Диссертация на соискание ученой степени доктора медицинских наук. М., 2005",
    "3": "Seckl M.J., Sebire N.J., Fisher R.A. et al. Gestational trophoblastic disease: ESMO clinical practice guidelines // Ann. Oncol. 2013. V. 24 (Suppl 6). P. vi39-vi50",
    "40": "(источник примечания к премедикации ТР/ТЕ — ссылка [40] в тексте таблицы 3)",
}


def cite(refs):
    return CITES.get(refs[0]) if refs else None


def row(cid, line_stage, name, drugs, refs, section, table, special=""):
    return {
        "cohort_id": cid,
        "disease": DISEASE,
        "treatment": {"line_stage": line_stage, "therapy_type": ["химиотерапия"], "regimen_name": name},
        "drugs": drugs,
        "indications": {"stage": None, "ecog": None, "biomarkers": []},
        "evidence": {"uur": "C", "udd": 5},
        "source": {"page": None, "section": section, "table": table, "references": refs, "citation": cite(refs)},
        "special_conditions": special,
        "maintenance_therapy": None,
    }


rows = [
    row("C1", "1-я линия (ЗТО низкого риска, FIGO-ВОЗ ≤6 баллов)", "Mtx/FA (#метотрексат + #кальция фолинат)",
        [{"inn": "Метотрексат", "dose": "50 мг", "route": "в/м", "schedule": "дни 1, 3, 5, 7", "cycle_frequency": "повторение курсов с 15-го дня от начала курса ХТ", "max_cycles": None},
         {"inn": "Кальция фолинат", "dose": "6 мг", "route": "в/м", "schedule": "дни 2, 4, 6, 8, через 30 часов от введения метотрексата", "cycle_frequency": "повторение курсов с 15-го дня", "max_cycles": None}],
        ["1", "3"], "3.3.1", "Таблица 2. Стандарты химиотерапии 1-й линии для пациентов с ЗТО"),
    row("C2", "1-я линия (ЗТО высокого риска, FIGO-ВОЗ ≥7 баллов)", "EMA-CO",
        [{"inn": "Этопозид", "dose": "100 мг/м²", "route": "в/в капельно", "schedule": "дни 1, 2", "cycle_frequency": "повторение курсов с 15-го дня от начала курса ХТ", "max_cycles": None},
         {"inn": "Дактиномицин", "dose": "500 мкг", "route": "в/в", "schedule": "дни 1, 2", "cycle_frequency": "повторение курсов с 15-го дня", "max_cycles": None},
         {"inn": "Метотрексат", "dose": "100 мг/м² в/в струйно + 200 мг/м² 12-часовой инфузией", "route": "в/в струйно, затем инфузия", "schedule": "день 1 (с кальция фолинатом 15 мг в/м через 24 ч от метотрексата, затем каждые 12 ч, всего 4 дозы)", "cycle_frequency": "повторение курсов с 15-го дня", "max_cycles": None},
         {"inn": "Циклофосфамид", "dose": "600 мг/м²", "route": "в/в", "schedule": "день 8", "cycle_frequency": "повторение курсов с 15-го дня", "max_cycles": None},
         {"inn": "Винкристин", "dose": "1 мг/м²", "route": "в/в струйно", "schedule": "день 8", "cycle_frequency": "повторение курсов с 15-го дня", "max_cycles": None}],
        ["1", "3"], "3.3.1", "Таблица 2. Стандарты химиотерапии 1-й линии для пациентов с ЗТО",
        special="ХГЧ контролируется еженедельно (0, 7, 14, 22-й дни); при церебральных метастазах и редких ТО высокого риска лечение также начинается со стандартной ХТ 1-й линии"),
    row("C3", "2-я линия (резистентность, группа исходно низкого риска)", "Дактиномицин (монотерапия)",
        [{"inn": "Дактиномицин", "dose": "500 мкг", "route": "в/в струйно", "schedule": "дни 1–5 (с противорвотной терапией)", "cycle_frequency": "повторные курсы с 15-го дня от начала предыдущего курса", "max_cycles": None}],
        ["1"], "3.3.1", "Таблица 3. Режимы химиотерапии 2-й линии при резистентных ЗТО"),
    row("C3", "2-я линия (резистентность, группа исходно низкого риска)", "EMA-CO",
        [{"inn": "Этопозид", "dose": "100 мг/м²", "route": "в/в капельно", "schedule": "дни 1, 2", "cycle_frequency": "повторение курсов с 15-го дня", "max_cycles": None},
         {"inn": "Дактиномицин", "dose": "500 мкг", "route": "в/в", "schedule": "дни 1, 2", "cycle_frequency": "повторение курсов с 15-го дня", "max_cycles": None},
         {"inn": "Метотрексат", "dose": "100 мг/м² в/в струйно + 200 мг/м² 12-часовой инфузией", "route": "в/в струйно, затем инфузия", "schedule": "день 1 (с кальция фолинатом 15 мг через 24 ч, далее каждые 12 ч, всего 4 дозы)", "cycle_frequency": "повторение курсов с 15-го дня", "max_cycles": None},
         {"inn": "Циклофосфамид", "dose": "600 мг/м²", "route": "в/в", "schedule": "день 8", "cycle_frequency": "повторение курсов с 15-го дня", "max_cycles": None},
         {"inn": "Винкристин", "dose": "1 мг/м²", "route": "в/в струйно", "schedule": "день 8", "cycle_frequency": "повторение курсов с 15-го дня", "max_cycles": None}],
        ["1"], "3.3.1", "Таблица 3 (вариант «ЕМА-CO (табл. 2)» для группы низкого риска резистентности)",
        special="Лечение в 1-й и 2-й дни проводится с обязательной гидратацией (не менее 2 л физ. р-ра), трансфузией раствора гидрокарбоната натрия и противорвотной терапией"),
    row("C4", "2-я линия (резистентность, группа исходно высокого риска)", "EMA-EP",
        [{"inn": "Этопозид", "dose": "100 мг/м²", "route": "в/в", "schedule": "дни 1, 2 и 8", "cycle_frequency": "повторные курсы с 15-го дня от начала предыдущего курса", "max_cycles": None},
         {"inn": "Дактиномицин", "dose": "500 мкг", "route": "в/в", "schedule": "дни 1, 2", "cycle_frequency": "повторные курсы с 15-го дня", "max_cycles": None},
         {"inn": "Метотрексат", "dose": "100 мг/м² в/в струйно + 1000 мг/м² 12-часовой инфузией", "route": "в/в струйно, затем инфузия", "schedule": "день 1 (с кальция фолинатом 30 мг в/м через 24 ч от начала метотрексата, затем каждые 12 ч, всего 8 доз)", "cycle_frequency": "повторные курсы с 15-го дня", "max_cycles": None},
         {"inn": "Кальция фолинат", "dose": "30 мг", "route": "в/м", "schedule": "через 24 ч после начала введения метотрексата, затем каждые 12 ч, всего 8 доз", "cycle_frequency": "повторные курсы с 15-го дня", "max_cycles": None},
         {"inn": "Цисплатин", "dose": "60–100 мг/м²", "route": "в/в", "schedule": "день 8", "cycle_frequency": "повторные курсы с 15-го дня", "max_cycles": None}],
        ["1"], "3.3.1", "Таблица 3. Режимы химиотерапии 2-й линии при резистентных ЗТО",
        special="Лечение в 1, 2 и 8-й дни проводится с обязательной гидратацией (не менее 2 л физ. р-ра), трансфузией раствора гидрокарбоната натрия и противорвотной терапией"),
    row("C4", "2-я линия (резистентность, группа исходно высокого риска)", "TP/TE (#паклитаксел/#цисплатин → #паклитаксел/#этопозид)",
        [{"inn": "Паклитаксел", "dose": "135 мг/м²", "route": "в/в капельно (в 400 мл физ. р-ра в течение 3 ч)", "schedule": "день 1 (премедикация: дексаметазон 20 мг за 12 и 6 ч; кальция фолинат 50 мг и фамотидин 20 мг за 30 мин до паклитаксела) и день 15 (премедикация: дексаметазон 20 мг, дифенгидрамин 50 мг, фамотидин 20 мг)", "cycle_frequency": "повторение курсов с 29-го дня от начала предыдущего курса", "max_cycles": None},
         {"inn": "Маннитол 10%", "dose": "500 мл (50 г)", "route": "в/в в течение 1 ч", "schedule": "день 1 (перед цисплатином)", "cycle_frequency": "повторение курсов с 29-го дня", "max_cycles": None},
         {"inn": "Цисплатин", "dose": "60 мг/м²", "route": "в/в капельно (в 800 мл физ. р-ра в течение 3 ч)", "schedule": "день 1 (постгидратация 1200 мл физ. р-ра + 20 ммоль калия хлорида + 1 г магния сульфата в течение 2 ч)", "cycle_frequency": "повторение курсов с 29-го дня", "max_cycles": None},
         {"inn": "Этопозид", "dose": "150 мг/м²", "route": "в/в (в 800 мл физ. р-ра)", "schedule": "день 15", "cycle_frequency": "повторение курсов с 29-го дня", "max_cycles": None}],
        ["40"], "3.3.1", "Таблица 3. Режимы химиотерапии 2-й линии при резистентных ЗТО"),
]
for r in rows:
    r["indications"]["stage"] = {
        "C1": "ЗТО низкого риска (FIGO-ВОЗ ≤6 баллов); ХГЧ-контроль в 0, 14, 28-й дни и т.д.",
        "C2": "ЗТО высокого риска (FIGO-ВОЗ ≥7 баллов); возможны церебральные метастазы",
        "C3": "Резистентная ЗТО исходно низкого риска (пересчет FIGO-ВОЗ после реcтадирования)",
        "C4": "Резистентная ЗТО исходно высокого риска (пересчет FIGO-ВОЗ после рестадирования)",
    }[r["cohort_id"]]
for r in rows:
    r["special_conditions"] = (r["special_conditions"] +
                               (" " if r["special_conditions"] else "") +
                               "ХТ проводится до нормализации уровня ХГЧ (≤5 мМЕ/мл) + 3 консолидирующих курса (при IV стадии — 4) либо до признаков резистентности").strip()

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
