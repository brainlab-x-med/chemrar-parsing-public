# -*- coding: utf-8 -*-
"""Build cohorts + regimens JSON for doc 555_3 (Плоскоклеточный рак анального канала) with audit."""
import sys, json, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit

DOC = "555_3"

audit.event(DOC, "phase2-start",
            "Плоскоклеточный рак анального канала/края/перианальной кожи (C21): "
            "ХЛТ митомицин+фторпиримидины, паллиативная ХТ 5ФУ+цисплатин")

disease = {
    "name": "Плоскоклеточный рак анального канала, анального края, перианальной кожи",
    "icd10": "C21",
    "histology_type": "плоскоклеточный рак (в т.ч. базалоидный); отдельно — аденокарцинома и НЭО/мелкоклеточный рак анального канала",
}

def drug(inn, dose, route, schedule, freq=None, max_cycles=None):
    return {"inn": inn, "dose": dose, "route": route, "schedule": schedule,
            "cycle_frequency": freq, "max_cycles": max_cycles}

cohorts = [
    {"cohort_id": "C1", "parent": None, "disease": disease,
     "stage": "TisN0M0 (интраэпителиальный рак; AIN II–III, болезнь Боуэна/Пэджета)",
     "resectability": None,
     "clinical_situation": "местное иссечение; лекарственной терапии нет",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["хирургическое лечение"],
     "source": {"section": "3.4"}},
    {"cohort_id": "C2", "parent": None, "disease": disease,
     "stage": "T1N0M0 (ранний рак перианальной кожи и анального края)",
     "resectability": None,
     "clinical_situation": "местное иссечение (край резекции ≥1 см, высокая дифференцировка); пациентам, не подходящим под критерии местного иссечения, — ХЛТ по принципам T2N0-2M0",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["хирургическое лечение", "при невозможности иссечения — ХЛТ"],
     "source": {"section": "3.5"}},
    {"cohort_id": "C3", "parent": None, "disease": disease,
     "stage": "T1–2 N0–2 M0 (рак анального канала, анального края или перианальной кожи)",
     "resectability": None,
     "clinical_situation": "ХЛТ: ЛТ РОД 2 Гр, СОД 40–44 Гр + буст на первичную опухоль СОД 6–10 Гр (итого 48–52 Гр) на фоне ХТ фторпиримидинами и митомицином С",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["одновременная химиолучевая терапия"],
     "source": {"section": "3.6, 3.2.1"}},
    {"cohort_id": "C4", "parent": None, "disease": disease,
     "stage": "T3–4 N0–2 M0 или T1–2 N1–2 M0 (местнораспространенный)",
     "resectability": None,
     "clinical_situation": "ХЛТ: ЛТ РОД 2 Гр, СОД 40–44 Гр + буст СОД 10–16 Гр (итого 54–60 Гр) на фоне ХТ фторпиримидинами и митомицином С; хирургия только при остаточной опухоли/кровотечении/отказе от ЛТ",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["одновременная химиолучевая терапия"],
     "source": {"section": "3.7, 3.2.1"}},
    {"cohort_id": "C5", "parent": None, "disease": disease,
     "stage": "Диссеминированный рак анального канала T1–4 N0–2 M1",
     "resectability": "нерезектабельный / метастатический",
     "clinical_situation": "системная химиотерапия",
     "ecog": None,
     "biomarkers": ["для НЭО — градация по Gr и Ki-67; аденокарцинома лечится по схемам рака прямой кишки"],
     "treatment_stages": ["паллиативная химиотерапия"],
     "source": {"section": "3.8, 3.2.2"}},
]

regimens = []
def row(cohort, line_stage, ttypes, name, drugs, stage_txt, ecog, bms, uur, udd, sec,
        refs, cite, special="", maint=None, table=None):
    return {
        "cohort_id": cohort, "disease": disease,
        "treatment": {"line_stage": line_stage, "therapy_type": ttypes, "regimen_name": name},
        "drugs": drugs,
        "indications": {"stage": stage_txt, "ecog": ecog, "biomarkers": bms},
        "evidence": {"uur": uur, "udd": udd},
        "source": {"page": None, "section": sec, "table": table, "references": refs, "citation": cite},
        "special_conditions": special, "maintenance_therapy": maint}

MM_FU = [
    drug("Митомицин С", "10 мг/м²", "в/в", "болюсно в дни 1 и 29", "2 введения за курс ХЛТ (день 1 и день 29)", None),
    drug("Фторурацил", "1000 мг/м²/сут", "в/в", "непрерывная инфузия в дни 1–4 и дни 29–32", "2 блока инфузий за курс ХЛТ", None),
]
XRT_NOTE = "ЛТ ежедневно, фотоны 6–18 МэВ (3DCRT/IMRT/RapidArc): первый этап РОД 2 Гр, СОД 40–44 Гр на первичную опухоль и зону регионарного метастазирования, второй этап — буст на исходные очаги"

regimens += [
    row("C3", "неоадъювантная/радикальная одновременная химиолучевая терапия (основной метод лечения)",
        ["химиотерапия", "лучевая терапия"], "Митомицин С + фторурацил + ЛТ (ХЛТ)",
        MM_FU, "Рак анального канала/края/перианальной кожи T1–2 N0–2 M0", None, [], "A", "Ib",
        "3.6, 3.2.1", ["15"],
        "Gunderson L.L. et al. Long-term update of US GI intergroup RTOG 98-11 phase III trial for anal carcinoma: survival, relapse, and colostomy failure with concurrent chemoradiation involving fluorouracil/mitomycin versus fluorouracil/cisplatin. J Clin Oncol 2012;30(35):4344-51",
        special=XRT_NOTE + "; при T1–2N0–2M0 буст на первичную опухоль СОД 6–10 Гр (суммарно 48–52 Гр). При локализованном раке предпочтительны схемы полихимиотерапии с 5-фторурацилом и митомицином С (I, A)",
        table=None),
    row("C4", "радикальная одновременная химиолучевая терапия (основной метод лечения)",
        ["химиотерапия", "лучевая терапия"], "Митомицин С + фторурацил + ЛТ (ХЛТ)",
        MM_FU, "Рак анального канала/края/перианальной кожи T3–4 N0–2 M0 или T1–2 N1–2 M0", None, [], "A", "Ib",
        "3.7, 3.2.1", ["15"],
        "Gunderson L.L. et al. Long-term update of US GI intergroup RTOG 98-11 phase III trial for anal carcinoma: survival, relapse, and colostomy failure with concurrent chemoradiation involving fluorouracil/mitomycin versus fluorouracil/cisplatin. J Clin Oncol 2012;30(35):4344-51",
        special=XRT_NOTE + "; буст на первичную опухоль СОД 10–16 Гр (минимум 10 Гр), суммарно 54–60 Гр. Ожидается полная регрессия у 50–80% пациентов; оценка эффекта через 8–12 недель. Перерывы в курсе ХЛТ — только при осложнениях ≥III степени (RTOG/NCI-CTC)",
        table=None),
    row("C2", "химиолучевая терапия у пациентов, не подходящих для местного иссечения (по принципам T2N0-2M0)",
        ["химиотерапия", "лучевая терапия"], "Митомицин С + фторурацил + ЛТ (ХЛТ)",
        MM_FU, "Ранний рак перианальной кожи и анального края T1N0M0, не подходящий для местного иссечения", None, [],
        "A", "Ib", "3.5, 3.2.1", ["15"],
        "Gunderson L.L. et al. Long-term update of US GI intergroup RTOG 98-11 phase III trial for anal carcinoma. J Clin Oncol 2012;30(35):4344-51",
        special="Проведение ХЛТ по принципам, аналогичным стадии T2N0-2M0",
        table=None),
    row("C4", "радикальная одновременная химиолучевая терапия при противопоказаниях к митомицину С",
        ["химиотерапия", "лучевая терапия"], "Цисплатин + фторурацил + ЛТ (ХЛТ)",
        [drug("Цисплатин", "60 мг/м²", "в/в", "в дни 1 и 29", "2 введения за курс ХЛТ", None),
         drug("Фторурацил", "1000 мг/м²/сут", "в/в", "непрерывная инфузия в дни 1–4 и дни 29–32", "2 блока инфузий за курс ХЛТ", None)],
        "Рак анального канала T3–4 N0–2 M0 или T1–2 N1–2 M0 (и другие cohorts ХЛТ)", None, [], "A", "Ib",
        "3.2.1", ["16"],
        "James R.D. et al. Mitomycin or cisplatin chemoradiation with or without maintenance chemotherapy for treatment of squamous-cell carcinoma of the anus (ACT II): a randomised, phase 3, open-label, 2 x 2 factorial trial. Lancet Oncol 2013;14(6):516-24",
        special="Схема используется при наличии противопоказаний к применению митомицина С (I, A)",
        table=None),
    row("C3", "радикальная одновременная химиолучевая терапия (замена 5-фторурацила капецитабином)",
        ["химиотерапия", "лучевая терапия"], "Митомицин С + капецитабин + ЛТ (ХЛТ)",
        [drug("Митомицин С", "10 мг/м²", "в/в", "болюсно в дни 1 и 29", "2 введения за курс ХЛТ", None),
         drug("Капецитабин", "825 мг/м² 2 раза в сутки", "внутрь", "per os в дни облучения", "ежедневно в дни ЛТ", None)],
        "Рак анального канала T1–2 N0–2 M0", None, [], "B", "IIa",
        "3.2.1", ["15"],
        "Gunderson L.L. et al. Long-term update of US GI intergroup RTOG 98-11 phase III trial for anal carcinoma. J Clin Oncol 2012;30(35):4344-51",
        special="#капецитабин — off-label. Для удобства применения возможна замена 5-фторурацила капецитабином (IIa, B)",
        table=None),
    row("C5", "паллиативная системная химиотерапия диссеминированного рака", ["химиотерапия"],
        "Фторурацил + цисплатин",
        [drug("Фторурацил", "1000 мг/м²/сут", "в/в", "непрерывная внутривенная инфузия в дни 1–5", "4-дневные курсы", None),
         drug("Цисплатин", "100 мг/м²", "в/в", "во 2-й день курса", "совместно с курсами ФУ", None)],
        "Диссеминированный рак анального канала T1–4 N0–2 M1", None, [], "B", "III",
        "3.8, 3.2.2", ["17"],
        "Faivre C. et al. [5-fluorouracile and cisplatinum combination chemotherapy for metastatic squamous-cell anal cancer]. Bulletin du cancer 1999;86(10):861-865",
        table=None),
    row("C5", "паллиативная химиотерапия мелкоклеточного (НЭО) рака анального канала", ["химиотерапия"],
        "ЕР (этопозид + цисплатин)",
        [drug("Этопозид", "120 мг/м²", "в/в", "в дни 1, 2, 3", "каждые 3 недели", None),
         drug("Цисплатин", "75 мг/м²", "в/в", "в 1-й день", "каждые 3 недели", None)],
        "Мелкоклеточный рак анального канала (НЭО)", None,
        ["вариант терапии зависит от пролиферативной активности опухоли (Gr, Ki-67)"], "C", "IV",
        "3.8", [],
        None,
        special="Основная лекарственная комбинация 1-й линии при мелкослеточном раке; приведена в комментарии к §3.8 без отдельной библиографической ссылки; НЭО лечатся как НЭО других локализаций. УУР/УДД не указаны явно — оценены как C/IV (комментарий без собственной доказательной строки)",
        table=None),
]

os.makedirs("output-cohort", exist_ok=True)
with open(f"output-cohort/{DOC}.cohorts.json", "w", encoding="utf-8") as f:
    json.dump(cohorts, f, ensure_ascii=False, indent=2)
with open(f"output-cohort/{DOC}.regimens.json", "w", encoding="utf-8") as f:
    json.dump(regimens, f, ensure_ascii=False, indent=2)

audit.read_block(DOC, f"{DOC}.md", 240, 332, "§3.1–3.8: ХЛТ (3.2.1) и паллиативная ХТ (3.2.2, 3.8)")
for c in cohorts:
    audit.cohort(DOC, c)
for r in regimens:
    audit.regimen(DOC, r)
audit.event(DOC, "phase2-done", f"{len(regimens)} regimens, {len(cohorts)} cohorts")
print(f"{DOC}: {len(cohorts)} cohorts, {len(regimens)} regimens written")
