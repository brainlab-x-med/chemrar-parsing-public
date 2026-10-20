# -*- coding: utf-8 -*-
"""Build cohorts + regimens JSON for doc 551_3 (ГИСО/GIST) with audit trail."""
import sys, json, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit

DOC = "551_3"

audit.event(DOC, "phase2-start",
            "ГИСО (GIST): cohort-first extraction; doc contains two merged revisions "
            "(2014 TNM7 + AJCC/UICC 8th ed); regimens identical across revisions")

disease = {
    "name": "Гастроинтестинальные стромальные опухоли (ГИСО)",
    "icd10": "C15-C20, C48",
    "histology_type": "стромальные опухоли ЖКТ (саркомы из интерстициальных клеток Кахаля); гистологические подтипы: веретеноклеточные (~70%), эпителиоидноклеточные (~20%), смешанные (~10%)",
}

cohorts = [
    {
        "cohort_id": "C1",
        "parent": None,
        "disease": disease,
        "stage": "Локализованные и местно-распространенные ГИСО (стадии I–III по TNM)",
        "resectability": "резектабельные / сомнительно резектабельные",
        "clinical_situation": "первичный операбельный процесс",
        "ecog": None,
        "biomarkers": [],
        "treatment_stages": ["хирургическое лечение (основной метод)", "неоадъювантная терапия иматинибом", "адъювантная терапия иматинибом"],
        "source": {"section": "3.1"},
    },
    {
        "cohort_id": "C1a",
        "parent": "C1",
        "disease": disease,
        "stage": "Местно-распространенный процесс",
        "resectability": "сомнительная резектабельность опухоли; также возможна предоперационная терапия при локализации в пищеводе, кардии, двенадцатиперстной или прямой кишке для органосохранной операции",
        "clinical_situation": "предоперационная (неоадъювантная) терапия иматинибом",
        "ecog": None,
        "biomarkers": [],
        "treatment_stages": ["неоадъювантная терапия"],
        "source": {"section": "3.1.1"},
    },
    {
        "cohort_id": "C1b",
        "parent": "C1",
        "disease": disease,
        "stage": "Любая стадия после радикальной операции",
        "resectability": "радикально оперированные (R0/R1)",
        "clinical_situation": "высокий и промежуточный риск прогрессирования (Joensuu 2008 / Miettinen-Lasota 2006)",
        "ecog": None,
        "biomarkers": [],
        "treatment_stages": ["адъювантная терапия"],
        "source": {"section": "3.1.2"},
    },
    {
        "cohort_id": "C2",
        "parent": None,
        "disease": disease,
        "stage": "IV стадия (M1); метастатические/диссеминированные ГИСО",
        "resectability": "неоперабельные либо метастатические (хирургия — дополнение на фоне эффективной ТКИ)",
        "clinical_situation": "метастатическая болезнь; основной метод лечения — таргетная терапия ТКИ (3 линии: иматиниб, сунитиниб, регорафениб)",
        "ecog": None,
        "biomarkers": [],
        "treatment_stages": ["1L иматиниб", "2L сунитиниб", "3L регорафениб", "последующие линии"],
        "source": {"section": "3.2"},
    },
    {
        "cohort_id": "C2a",
        "parent": "C2",
        "disease": disease,
        "stage": "IV стадия (M1)",
        "resectability": None,
        "clinical_situation": "первая линия лечения метастатических ГИСО",
        "ecog": None,
        "biomarkers": ["мутации KIT (экзоны 9, 11, 13, 17) и/или PDGFRA; WT ~10–15%"],
        "treatment_stages": ["1-я линия"],
        "source": {"section": "3.2.1"},
    },
    {
        "cohort_id": "C2b",
        "parent": "C2a",
        "disease": disease,
        "stage": "IV стадия (M1)",
        "resectability": None,
        "clinical_situation": "первая линия лечения метастатических ГИСО",
        "ecog": None,
        "biomarkers": ["мутация в 9 экзоне KIT (дупликации)"],
        "treatment_stages": ["1-я линия (высокая доза иматиниба)"],
        "source": {"section": "3.2.1"},
    },
    {
        "cohort_id": "C2c",
        "parent": "C2a",
        "disease": disease,
        "stage": "IV стадия (M1)",
        "resectability": None,
        "clinical_situation": "прогрессирование на фоне иматиниба 400 мг/сутки",
        "ecog": None,
        "biomarkers": [],
        "treatment_stages": ["эскалация дозы иматиниба (интервенная терапия)"],
        "source": {"section": "3.2.1"},
    },
    {
        "cohort_id": "C2d",
        "parent": "C2",
        "disease": disease,
        "stage": "IV стадия (M1)",
        "resectability": None,
        "clinical_situation": "вторая линия лечения метастатических ГИСО, резистентных к иматинибу",
        "ecog": None,
        "biomarkers": [],
        "treatment_stages": ["2-я линия"],
        "source": {"section": "3.2.2"},
    },
    {
        "cohort_id": "C2e",
        "parent": "C2",
        "disease": disease,
        "stage": "IV стадия (M1)",
        "resectability": None,
        "clinical_situation": "третья линия лечения метастатических ГИСО, резистентных к иматинибу и сунитинибу",
        "ecog": None,
        "biomarkers": [],
        "treatment_stages": ["3-я линия"],
        "source": {"section": "3.2.3"},
    },
    {
        "cohort_id": "C2f",
        "parent": "C2",
        "disease": disease,
        "stage": "IV стадия (M1)",
        "resectability": None,
        "clinical_situation": "прогрессирование после иматиниба, сунитиниба и регорафениба (когда другие методы недоступны)",
        "ecog": None,
        "biomarkers": [],
        "treatment_stages": ["последняя линия (повторное назначение иматиниба)"],
        "source": {"section": "3.2.3"},
    },
]

def drug(inn, dose, route, schedule, freq=None, max_cycles=None):
    return {"inn": inn, "dose": dose, "route": route, "schedule": schedule,
            "cycle_frequency": freq, "max_cycles": max_cycles}

regimens = [
    {
        "cohort_id": "C1a",
        "disease": disease,
        "treatment": {
            "line_stage": "неоадъювантная (предоперационная) терапия",
            "therapy_type": ["таргетная терапия"],
            "regimen_name": "Неоадъювантная терапия иматинибом",
        },
        "drugs": [drug("Иматиниб", "400 мг в сутки", "внутрь",
                       "непрерывно, ежедневно за один прием во время еды",
                       "ежедневно непрерывно",
                       "до максимального эффекта (обычно 6–12 месяцев) с последующим продолжением лечения в течение 3 лет; хирургическое лечение на максимальном эффекте")],
        "indications": {
            "stage": "Местно-распространенный процесс при сомнительной резектабельности; также пищевод, кардия, двенадцатиперстная и прямая кишка (органосохранная операция)",
            "ecog": None,
            "biomarkers": [],
        },
        "evidence": {"uur": "B", "udd": "IIb"},
        "source": {
            "page": None,
            "section": "3.1.1",
            "table": None,
            "references": ["19"],
            "citation": "Piotr Rutkowski. Neoadjuvant Imatinib in Locally Advanced Gastrointestinal Stromal Tumors (GIST): The EORTC STBSG Experience / A. Gronchi et al. Ann Surg Oncol 2013;20:2937–2943",
        },
        "special_conditions": "",
        "maintenance_therapy": None,
    },
    {
        "cohort_id": "C1b",
        "disease": disease,
        "treatment": {
            "line_stage": "адъювантная терапия",
            "therapy_type": ["таргетная терапия"],
            "regimen_name": "Адъювантная терапия иматинибом",
        },
        "drugs": [drug("Иматиниб", "400 мг в сутки", "внутрь",
                       "ежедневно в течение 3 лет",
                       "ежедневно непрерывно", "3 года (по данным PERSIST-5 возможно 5 лет)")],
        "indications": {
            "stage": "После радикального хирургического лечения; высокий и промежуточный риск прогрессирования",
            "ecog": None,
            "biomarkers": [],
        },
        "evidence": {"uur": "A", "udd": "Ia"},
        "source": {
            "page": None,
            "section": "3.1.2",
            "table": None,
            "references": ["20", "21"],
            "citation": "Corless C.L., Ballman K.V., Antonescu C. et al. Relation of tumor pathologic and molecular features to outcome after surgical resection of localized primary GIST (ACOSOG Z9001). J Clin Oncol 2010;28(15):Suppl. Abstract 10006",
        },
        "special_conditions": "Больным с низким и очень низким риском прогрессирования адъювантная терапия НЕ показана",
        "maintenance_therapy": None,
    },
    {
        "cohort_id": "C2a",
        "disease": disease,
        "treatment": {
            "line_stage": "1-я линия лечения метастатических ГИСО",
            "therapy_type": ["таргетная терапия"],
            "regimen_name": "Иматиниб 400 мг/сут (стандарт первой линии)",
        },
        "drugs": [drug("Иматиниб", "400 мг", "внутрь",
                       "ежедневно за один прием во время еды (с нежирной пищей)",
                       "ежедневно непрерывно", "до прогрессирования")],
        "indications": {
            "stage": "IV стадия (метастатические/неоперабельные ГИСО)",
            "ecog": None,
            "biomarkers": ["наиболее высокая эффективность при мутации 11 экзона KIT (ответ 70–85%)"],
        },
        "evidence": {"uur": "A", "udd": "Ib"},
        "source": {
            "page": None,
            "section": "3.2.1",
            "table": None,
            "references": [],
            "citation": None,
        },
        "special_conditions": "Коррекция дозы при токсичности (редукция на 25%: 400→300 мг/сут или 800→600 мг/сут); учитывать взаимодействия с индукторами/ингибиторами CYP3A4",
        "maintenance_therapy": None,
    },
    {
        "cohort_id": "C2b",
        "disease": disease,
        "treatment": {
            "line_stage": "1-я линия лечения метастатических ГИСО",
            "therapy_type": ["таргетная терапия"],
            "regimen_name": "Иматиниб 800 мг/сут (мутация KIT экзон 9)",
        },
        "drugs": [drug("Иматиниб", "800 мг в сутки", "внутрь",
                       "ежедневно",
                       "ежедневно непрерывно", "до прогрессирования")],
        "indications": {
            "stage": "IV стадия (метастатические/неоперабельные ГИСО)",
            "ecog": None,
            "biomarkers": ["мутация в 9 экзоне KIT (объективный ответ 59% vs 17% при 400 мг/сут)"],
        },
        "evidence": {"uur": "B", "udd": "IIb"},
        "source": {
            "page": None,
            "section": "3.2.1",
            "table": None,
            "references": ["25", "27"],
            "citation": "Le Cesne A., Ray-Coquard I., Bui B.N. et al. Discontinuation of imatinib in patients with advanced gastrointestinal stromal tumours after 3 years of treatment: an open-label multicentre randomised phase 3 trial. Lancet Oncol 2010;11(10):942–949",
        },
        "special_conditions": "При мутации D842V гена PDGFRA лечение иматинибом не показано (препарат не эффективен)",
        "maintenance_therapy": None,
    },
    {
        "cohort_id": "C2c",
        "disease": disease,
        "treatment": {
            "line_stage": "эскалация дозы при прогрессировании на иматинибе 400 мг/сутки",
            "therapy_type": ["таргетная терапия"],
            "regimen_name": "Иматиниб 800 мг/сут (400 мг 2 раза в день)",
        },
        "drugs": [drug("Иматиниб", "800 мг/сутки (400 мг 2 раза в день)", "внутрь",
                       "ежедневно, 2 приема в день",
                       "ежедневно непрерывно", "до убедительных признаков прогрессирования опухоли")],
        "indications": {
            "stage": "IV стадия; прогрессирование на фоне иматиниба 400 мг/сутки",
            "ecog": None,
            "biomarkers": [],
        },
        "evidence": {"uur": "B", "udd": "IIa"},
        "source": {
            "page": None,
            "section": "3.2.1",
            "table": None,
            "references": [],
            "citation": None,
        },
        "special_conditions": "Иматиниб применять непрерывно; прерывание лечения приводит к прогрессированию заболевания",
        "maintenance_therapy": None,
    },
    {
        "cohort_id": "C2d",
        "disease": disease,
        "treatment": {
            "line_stage": "2-я линия лечения метастатических ГИСО",
            "therapy_type": ["таргетная терапия"],
            "regimen_name": "Сунитиниб (режим 4 недели/2 недели)",
        },
        "drugs": [drug("Сунитиниб", "50 мг", "внутрь",
                       "ежедневно в течение 4-х недель с 2-хнедельными интервалами (режим 4 недели/2 недели); альтернативный режим — 37,5 мг ежедневно без перерыва",
                       "курс 6 недель: 4 недели приема / 2 недели перерыва", "до прогрессирования")],
        "indications": {
            "stage": "IV стадия; метастатические ГИСО, резистентные к иматинибу",
            "ecog": None,
            "biomarkers": [],
        },
        "evidence": {"uur": "A", "udd": "Ib"},
        "source": {
            "page": None,
            "section": "3.2.2",
            "table": None,
            "references": ["33", "34", "35"],
            "citation": "Demetri GD, van Oosterom AT, Garrett CR, et al. Efficacy and safety of sunitinib in patients with advanced gastrointestinal stromal tumour after failure of imatinib: a randomised controlled trial. Lancet 2006;368:1329-38",
        },
        "special_conditions": "Альтернативный режим 37,5 мг ежедневно без перерыва обладает менее выраженной токсичностью при сопоставимой эффективности; коррекция дозы при совместном приеме с ингибиторами/индукторами CYP3A4",
        "maintenance_therapy": None,
    },
    {
        "cohort_id": "C2e",
        "disease": disease,
        "treatment": {
            "line_stage": "3-я линия лечения метастатических ГИСО",
            "therapy_type": ["таргетная терапия"],
            "regimen_name": "Регорафениб (режим 3 недели/1 неделя)",
        },
        "drugs": [drug("Регорафениб", "160 мг", "внутрь",
                       "ежедневно в течение 3-х недель с перерывом на одну неделю (режим 3 недели/1 неделя)",
                       "курс 4 недели: 3 недели приема / 1 неделя перерыва", "до прогрессирования")],
        "indications": {
            "stage": "IV стадия; метастатические ГИСО, резистентные к иматинибу и сунитинибу",
            "ecog": None,
            "biomarkers": [],
        },
        "evidence": {"uur": "A", "udd": "Ia"},
        "source": {
            "page": None,
            "section": "3.2.3",
            "table": None,
            "references": ["36"],
            "citation": "Demetri GD, Reichardt P, Kang YK et al. Efficacy and safety of regorafenib for advanced gastrointestinal stromal tumours after failure of imatinib and sunitinib (GRID): an international, multicentre, randomised, placebo-controlled, phase 3 trial. Lancet 2013;381(9863):295-302",
        },
        "special_conditions": "Улучшил время до прогрессирования на 4,8 месяца",
        "maintenance_therapy": None,
    },
    {
        "cohort_id": "C2f",
        "disease": disease,
        "treatment": {
            "line_stage": "последняя линия (после прогрессирования на иматинибе, сунитинибе и регорафенибе)",
            "therapy_type": ["таргетная терапия"],
            "regimen_name": "Повторное назначение иматиниба (ре-challenge)",
        },
        "drugs": [drug("Иматиниб", None, "внутрь",
                       "ежедневно (доза в документе не указана)",
                       "ежедневно непрерывно", "до прогрессирования")],
        "indications": {
            "stage": "IV стадия; прогрессирование после иматиниба, сунитиниба и регорафениба",
            "ecog": None,
            "biomarkers": [],
        },
        "evidence": {"uur": "B", "udd": "III"},
        "source": {
            "page": None,
            "section": "3.2.3",
            "table": None,
            "references": [],
            "citation": None,
        },
        "special_conditions": "Только если не доступны какие-либо другие методы лечения (в качестве последней линии); даже при формальной неэффективности иматиниб может замедлять рост опухоли. При прогрессировании на всех трех ТКИ также рекомендуется участие в клинических исследованиях новых таргетных препаратов",
        "maintenance_therapy": None,
    },
]

os.makedirs("output-cohort", exist_ok=True)

with open(f"output-cohort/{DOC}.cohorts.json", "w", encoding="utf-8") as f:
    json.dump(cohorts, f, ensure_ascii=False, indent=2)

with open(f"output-cohort/{DOC}.regimens.json", "w", encoding="utf-8") as f:
    json.dump(regimens, f, ensure_ascii=False, indent=2)

# ---- audit trail ----
audit.read_block(DOC, f"{DOC}.md", 33, 33, "§1–3 единый блок: МКБ C15–C20,C48; §3.1–3.2.3 режимы лекарственной терапии")
for c in cohorts:
    audit.cohort(DOC, c)
for r in regimens:
    audit.regimen(DOC, r)
audit.event(DOC, "phase2-done", f"{len(regimens)} regimens, {len(cohorts)} cohorts")
print(f"{DOC}: {len(cohorts)} cohorts, {len(regimens)} regimens written")
