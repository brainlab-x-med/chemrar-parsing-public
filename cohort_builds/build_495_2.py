# -*- coding: utf-8 -*-
"""Build cohorts + medication regimens for doc 495_2 (рак желчевыводящей системы / билиарный рак)."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit  # noqa: E402

DOC = "495_2"

DISEASE = {
    "name": "Рак желчевыводящей системы (билиарный рак: холангиокарцинома, рак желчного пузыря, рак внепеченочных желчных протоков)",
    "icd10": "C22.1 (внутрипеченочные желчные протоки), C23 (желчный пузырь), C24 (внепеченочные желчные протоки и другие билиарные локализации)",
    "histology_type": "аденокарцинома (>90% холангиокарцином; ~80% продуцируют муцин); гистологические модели роста: объём-формирующий, перидуктально-инфильтративный, внутрипротоковый",
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
    {"cohort_id": "C1", "disease": DISEASE, "stage": "рак билиарного тракта после радикального хирургического лечения (R0)",
     "resectability": "резектабельный (радикально оперированный)", "clinical_situation": "адъювантная химиотерапия",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["адъювантная химиотерапия вне зависимости от поражения лимфоузлов и степени дифференцировки"], "source": {"section": "3.3"}},
    {"cohort_id": "C2", "disease": DISEASE, "stage": "после нерадикальной операции (R1/R2) или с метастазами в лимфатических узлах",
     "resectability": "краевая резекция (R1/R2)", "clinical_situation": "адъювантная системная ХТ и химиолучевая терапия",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["системная ХТ (по принципам лечения метастатического процесса), химиолучевая терапия с фторпиримидинами, после ХЛТ — монохимиотерапия капецитабином"], "source": {"section": "3.3"}},
    {"cohort_id": "C3", "disease": DISEASE, "stage": "неоперабельный местнораспространённый рак билиарного тракта (стадии IIIa–IVa; T3–4 N0–1 M0)",
     "resectability": "нерезектабельный, локализованный", "clinical_situation": "первичное лечение (лока-регионарные методы, ХЛТ)",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["лока-регионарные методы (деструкция, ТАХЭ, селективная внутриартериальная ХТ, стереотаксическая ЛТ), фотодинамическая терапия, химиолучевая терапия"], "source": {"section": "3.3"}},
    {"cohort_id": "C4", "disease": DISEASE, "stage": "диссеминированный рак билиарного тракта (стадия IVb, M1)",
     "resectability": None, "clinical_situation": "1-я линия системной терапии",
     "ecog": "удовлетворительное общее состояние (ECOG 0–1)",
     "biomarkers": ["PD-L1 не требуется для комбинаций с иммунотерапией"],
     "treatment_stages": ["системная химиотерапия гемцитабином с производными платины +/- иммунотерапия; длительность определяется переносимостью/эффективностью (нет пользы >6 мес)"], "source": {"section": "3.3"}},
    {"cohort_id": "C5", "disease": DISEASE, "stage": "диссеминированный рак билиарного тракта (стадия IVb, M1)",
     "resectability": None, "clinical_situation": "паллиативная монохимиотерапия",
     "ecog": "ослабленное общее состояние (ECOG 2); при ECOG>2 — только симптоматическая терапия",
     "biomarkers": [], "treatment_stages": ["монохимиотерапия гемцитабином или капецитабином с паллиативной целью"], "source": {"section": "3.3"}},
    {"cohort_id": "C6", "disease": DISEASE, "stage": "диссеминированный рак билиарного тракта, прогрессирование после 1-й линии",
     "resectability": None, "clinical_situation": "химиотерапия второй линии",
     "ecog": "удовлетворительное состояние пациента",
     "biomarkers": [], "treatment_stages": ["режим 2-й линии с учётом эффективности 1-й линии (FOLFOX/FOLFIRI/XELOX/XELIRI)"], "source": {"section": "3.3"}},
    {"cohort_id": "C7", "disease": DISEASE, "stage": "нерезектабельный/метастатический билиарный рак, рефрактерный к стандартной ХТ",
     "resectability": None, "clinical_situation": "молекулярно-направленная терапия",
     "ecog": "ECOG не хуже 2, компенсированная функция печени",
     "biomarkers": ["HER2/neu (ERBB2) гиперэкспрессия/амплификация при «диком» типе RAS", "мутация BRAF V600E", "MSI-H/dMMR", "транслокации FGFR2/FGFR1-4", "транслокация RET"],
     "treatment_stages": ["по исчерпании стандартных терапевтических опций, по решению консилиума"], "source": {"section": "3.3"}},
]

R = []
# ---------- C1 ----------
R.append(base("C1", "адъювантная химиотерапия", ["химиотерапия"], "Капецитабин монотерапия (BILCAP)",
              [drug("Капецитабин", "1250 мг/м² 2 раза в день", "внутрь", "1–14-й дни", "каждые 21 день", 8)],
              "рак билиарного тракта после радикального хирургического лечения (R0)",
              uur="A", udd=2, refs=["84", "85", "86", "87", "88"],
              cite="Valle J.W. et al. Cisplatin and gemcitabine for advanced biliary tract cancer: a meta-analysis of two randomised trials // Annals of Oncology. 2014. Vol. 25, № 2. P. 391–398",
              special="** ЖНВЛП; # off-label; 8 трёхнедельных курсов вне зависимости от поражения лимфоузлов и степени дифференцировки"))

# ---------- C2 ----------
R += [
    base("C2", "адъювантная системная химиотерапия после R1/R2 или при N+", ["химиотерапия"],
         "Гемцитабин + цисплатин (или гемцитабин + капецитабин) — комбинированные режимы",
         [drug("Гемцитабин", "1000 мг/м²", "в/в", "1-й и 8-й дни", "каждые 3 недели"),
          drug("Цисплатин", "25 мг/м²", "в/в", "1-й и 8-й дни", "каждые 3 недели")],
         "нерадикальная операция (R1/R2) или метастазы в лимфатических узлах",
         uur="A", udd=2, refs=["93", "94"],
         cite="Cereda S., Belli C., Reni M. Adjuvant treatment in biliary tract cancer: To treat or not to treat? // World J Gastroenterol. 2012. Vol. 18, № 21. P. 2591–2596",
         special="** ЖНВЛП; # off-label; при низкой степени дифференцировки и/или метастазах в лимфоузлах возможно применение комбинированных режимов гемцитабин/цисплатин или гемцитабин/капецитабин; дозы приведены по таблице 6 (метастатический процесс)"),
    base("C2", "адъювантная химиолучевая терапия", ["химиолучевая терапия (ХЛТ)", "химиотерапия"],
         "Капецитабин + лучевая терапия (адъювантная ХЛТ с фторпиримидинами)",
         [drug("Капецитабин", None, "внутрь", "во время проведения ЛТ (СОД 46 Гр; при R1/R2 — 50–60 Гр на ложе опухоли)", "ежедневно в дни ЛТ")],
         "нерадикальная операция (R1/R2) или метастазы в лимфатических узлах",
         uur="A", udd=2, refs=["93", "94"],
         cite="Kelley S.T. et al. Cholangiocarcinoma: Advocate an Aggressive Operative Approach with Adjuvant Chemotherapy // The American Surgeon. 2004. Vol. 70",
         special="** ЖНВЛП; # off-label; после завершения ХЛТ показана монохимиотерапия капецитабином; разовая/суточная доза капецитабина в разделе не приведена (см. SWOG S0809 [183])"),
]

# ---------- C3: неоперабельный местнораспространённый ----------
R.append(base("C3", "неоперабельный местнораспространённый процесс (поздние стадии IIIa–IVa)", ["химиолучевая терапия (ХЛТ)", "химиотерапия"],
              "Индукция гемцитабин + капецитабин с последующей консолидацией капецитабином на фоне стереотаксической ЛТ",
              [drug("Гемцитабин", "1000 мг/м²", "в/в", "1-й и 8-й дни цикла", "каждые 21 день", 4),
               drug("Капецитабин (индукция)", "1500 мг/м²", "внутрь", "с 1-го по 14-й день", "каждые 21 день", 4),
               drug("Капецитабин (на фоне ЛТ)", "1330 мг/м² в день", "внутрь", "одновременно с лучевой терапией (СТОД 30–50 Гр за 3–5 фракций)", "ежедневно в дни ЛТ")],
              "поздние стадии внепеченочной холангиокарциномы (IIIa–IVa, T3–4 N0–1 M0)",
              uur="C", udd=4, refs=["183", "184"],
              cite="Ben-Josef E., Guthrie K.A., El-Khoueiry A.B. et al. SWOG S0809: a phase II intergroup trial of adjuvant capecitabine and gemcitabine followed by radiotherapy and concurrent capecitabine in extrahepatic cholangiocarcinoma and gallbladder carcinoma",
              special="** ЖНВЛП; # off-label; одновременное использование гемцитабина с ЛТ не рекомендуется из-за ограниченного опыта и высокой токсичности"))

# ---------- C4: 1L диссеминированного ----------
gemcis = lambda: [drug("Гемцитабин", "1000 мг/м²", "в/в", "1-й и 8-й дни", "каждые 3 недели"),
                  drug("Цисплатин", "25 мг/м²", "в/в", "1-й и 8-й дни", "каждые 3 недели")]
l1_line = "1-я линия терапии распространённого нерезектабельного/метастатического рака билиарного тракта"
l1_stage = "диссеминированный рак билиарного тракта (IVb, M1)"
R += [
    base("C4", l1_line, ["химиотерапия"], "Гемцитабин + цисплатин",
         gemcis(), l1_stage, uur="A", udd=2, refs=["19", "107", "108", "109", "110", "111", "112", "113", "114", "122", "173"],
         cite="Valle J. et al. Cisplatin plus gemcitabine versus gemcitabine for biliary tract cancer // New England Journal of Medicine. 2010. Vol. 362, № 14. P. 1273–1281",
         special="** ЖНВЛП; # off-label; возможна при умеренно повышенном билирубине вследствие внутрипечёночного холестаза при адекватном оттоке желчи; оксалиплатин 100 мг/м² может заменить цисплатин при нарушенной функции почек/высокой токсичности цисплатина [154]",
         maint="Длительность определяется переносимостью и эффективностью; нет доказательств дополнительной пользы лечения длительностью более 6 мес"),
    base("C4", l1_line, ["химиотерапия", "иммунотерапия"], "Гемцитабин + цисплатин + дурвалумаб (TOPAZ-1)",
         gemcis()[:-1] + gemcis()[1:] if False else [
             drug("Гемцитабин", "1000 мг/м²", "в/в", "1-й и 8-й дни", "каждые 21 день", 8),
             drug("Цисплатин", "25 мг/м²", "в/в", "1-й и 8-й дни", "каждые 21 день", 8),
             drug("Дурвалумаб", "1500 мг", "в/в", "1-й день каждые 21 день (до 8 циклов), далее каждые 4 недели", "каждые 3 недели (индукция), затем каждые 4 недели", "до прогрессирования или неприемлемой токсичности")],
         l1_stage, uur="A", udd=2, refs=["122"],
         cite="Oh D.-Y. et al. Durvalumab plus Gemcitabine and Cisplatin in Advanced Biliary Tract Cancer // NEJM Evidence. 2022. P. EVIDoa2200015",
         special="** ЖНВЛП; достоверное увеличение ОВ и ВБП vs плацебо (TOPAZ-1)",
         maint="После ≤8 циклов иммунохимиотерапии — дурвалумаб 1500 мг в/в каждые 4 недели до прогрессирования или неприемлемой токсичности"),
    base("C4", l1_line, ["химиотерапия", "иммунотерапия"], "Гемцитабин + цисплатин + пембролизумаб (KEYNOTE-966)",
         [drug("Гемцитабин", "1000 мг/м²", "в/в", "1-й и 8-й дни", "без ограничения продолжительности применения"),
          drug("Цисплатин", "25 мг/м²", "в/в", "1-й и 8-й дни", None, 8),
          drug("Пембролизумаб", "200 мг", "в/в", "1-й день каждые 3 недели", "каждые 3 недели", "максимум 35 циклов")],
         l1_stage, uur="A", udd=2, refs=["173"],
         cite="Kelley R.K., Ueno M., Yoo C. et al. Pembrolizumab in combination with gemcitabine and cisplatin compared with gemcitabine and cisplatin alone for patients with advanced biliary tract cancer (KEYNOTE-966)",
         special="** ЖНВЛП; достоверное увеличение ОВ vs гемцитабин+цисплатин (KEYNOTE-966)"),
    base("C4", l1_line, ["химиотерапия"], "Гемцитабин + оксалиплатин (GEMOX)",
         [drug("Гемцитабин", "1000 мг/м²", "в/в", "1-й и 8-й дни", "каждые 3 недели"),
          drug("Оксалиплатин", "100 мг/м²", "в/в", "1-й день", "каждые 3 недели")],
         l1_stage, uur="A", udd=2, refs=["10", "19", "116"],
         cite="Jang J.-S. et al. Gemcitabine and oxaliplatin in patients with unresectable biliary cancer including gall bladder cancer: a Korean Cancer Study Group phase II trial",
         special="** ЖНВЛП; # off-label; оксалиплатин в дозе 100 мг/м² может заменить цисплатин в сочетании с гемцитабином при нарушенной функции почек, высокой токсичности или других противопоказаниях к цисплатину [154]"),
]

# ---------- C5: монохимиотерапия ECOG 2 ----------
mono_line = "паллиативная монохимиотерапия при ослабленном состоянии"
R += [
    base("C5", mono_line, ["химиотерапия"], "Гемцитабин монотерапия",
         [drug("Гемцитабин", "1000 мг/м²", "в/в", "1-й, 8-й, 15-й дни", "каждые 4 недели")],
         l1_stage, ecog="ECOG 2", uur="C", udd=5, refs=["10", "19", "172"],
         cite="NCCN Clinical Practice Guidelines in Oncology (NCCN Guidelines®) Biliary Tract Cancers Version 3.2024",
         special="** ЖНВЛП; # off-label; с паллиативной целью; при ECOG>2 химиотерапия не рекомендуется"),
    base("C5", mono_line, ["химиотерапия"], "Капецитабин монотерапия",
         [drug("Капецитабин", "1250 мг/м² 2 раза в день", "внутрь", "1–14-й дни", "каждые 21 день")],
         l1_stage, ecog="ECOG 2", uur="C", udd=5, refs=["10", "19", "172"],
         cite="NCCN Clinical Practice Guidelines in Oncology (NCCN Guidelines®) Biliary Tract Cancers Version 3.2024",
         special="** ЖНВЛП; # off-label; с паллиативной целью; выбор с учётом профиля токсичности"),
    base("C5", mono_line, ["химиотерапия"], "Иринотекан монотерапия",
         [drug("Иринотекан", "240 мг/м²", "в/в", "1-й день", "каждые 3 недели")],
         l1_stage, uur="C", udd=5, refs=["182"],
         cite="Zheng Y., Tu X., Zhao P. et al. A randomised phase II study of second-line XELIRI regimen versus irinotecan monotherapy in advanced biliary tract cancer",
         special="** ЖНВЛП; # off-label (из блока монохимиотерапии таблицы 6)"),
]

# ---------- C6: 2L ----------
l2_line = "химиотерапия второй линии диссеминированного рака билиарного тракта"
l2_stage = "диссеминированный рак билиарного тракта, прогрессирование после 1-й линии"
R += [
    base("C6", l2_line, ["химиотерапия"], "FOLFOX6",
         [drug("Оксалиплатин", "85 мг/м²", "в/в", "2-часовая инфузия, 1-й день", "каждые 2 недели"),
          drug("Кальция фолинат", "400 мг/м²", "в/в", "2-часовая инфузия, 1-й день", "каждые 2 недели"),
          drug("Фторурацил", "400 мг/м² струйно + 2400 мг/м² (1200 мг/м² в сутки) 46-часовая инфузия", "в/в", "струйно затем 46-часовая инфузия, 1-й день", "каждые 2 недели")],
         l2_stage, uur="C", udd=5, refs=["89", "117"],
         cite="Бредер В.В., Косырев В.Ю., Ледин Е.В. Практические рекомендации по лекарственному лечению билиарного рака",
         special="** ЖНВЛП; ABC-06: умеренное увеличение ОВ химиотерапии vs активная симптоматическая терапия (ОР 0,69)"),
    base("C6", l2_line, ["химиотерапия"], "FOLFIRI",
         [drug("Иринотекан", "180 мг/м²", "в/в", "90-минутная инфузия, 1-й день", "каждые 2 недели"),
          drug("Кальция фолинат", "400 мг/м²", "в/в", "2-часовая инфузия, 1-й день", "каждые 2 недели"),
          drug("Фторурацил", "400 мг/м² струйно + 2400 мг/м² (1200 мг/м² в сутки) 46-часовая инфузия", "в/в", "струйно затем 46-часовая инфузия, 1-й день", "каждые 2 недели")],
         l2_stage, uur="C", udd=5, refs=["174"],
         cite="Choi I.S., Kim K.H., Lee J.H. et al. A randomised phase II study of oxaliplatin/5-FU (mFOLFOX) versus irinotecan/5-FU (mFOLFIRI) chemotherapy in locally advanced or metastatic biliary tract cancer",
         special="** ЖНВЛП; эффективность сопоставима с mFOLFOX после гемцитабин+цисплатин"),
    base("C6", l2_line, ["химиотерапия"], "XELOX",
         [drug("Оксалиплатин", "130 мг/м²", "в/в", "1-й день", "каждые 3 недели"),
          drug("Капецитабин", "1000 мг/м² 2 раза в сутки", "внутрь", "1–14-й дни", "каждые 3 недели")],
         l2_stage, uur="C", udd=5, refs=["154"],
         cite="Kim S.T., Kang J.H., Lee J. et al. Capecitabine plus oxaliplatin versus gemcitabine plus oxaliplatin as first-line therapy for advanced biliary tract cancers",
         special="** ЖНВЛП; # off-label"),
    base("C6", l2_line, ["химиотерапия"], "XELIRI",
         [drug("Иринотекан", "200 мг/м²", "в/в", "1-й день", "каждые 3 недели"),
          drug("Капецитабин", "1700 мг/м² в сутки в 2 приема", "внутрь", "1–14-й дни", "каждые 3 недели")],
         l2_stage, uur="C", udd=5, refs=["182"],
         cite="Zheng Y., Tu X., Zhao P. et al. A randomised phase II study of second-line XELIRI regimen versus irinotecan monotherapy in advanced biliary tract cancer",
         special="** ЖНВЛП; # off-label"),
]

# ---------- C7: молекулярно-направленная терапия ----------
tgt_line = "молекулярно-направленная терапия рефрактерного к стандартной ХТ распространённого процесса"
no_dose = "; доза препарата в документе не приведена (в тексте указано «доза препарата указана в таблице 6», но в таблице отсутствует)"
R += [
    base("C7", tgt_line, ["иммунотерапия"], "Пембролизумаб монотерапия",
         [drug("Пембролизумаб", "200 мг или 400 мг", "в/в", "капельно 30 мин; 200 мг 1 раз в 3 недели или 400 мг каждые 42 дня", "каждые 3 недели или каждые 42 дня", "до двух лет")],
         "нерезектабельный/метастатический билиарный рак", bio=["MSI-H (только для MSI-H опухолей)"],
         uur="C", udd=5, refs=["159"],
         cite="Marabelle A., Le D.T., Ascierto P.A. et al. Efficacy of Pembrolizumab in Patients With Noncolorectal High Microsatellite Instability/Mismatch Repair-Deficient Cancer (KEYNOTE-158)",
         special="** ЖНВЛП; только для MSI-H опухолей (частота dMMR при билиарном раке <1%)"),
    base("C7", tgt_line, ["таргетная терапия"], "Пертузумаб + трастузумаб",
         [drug("Трастузумаб", "8 мг/кг нагрузочная, далее 6 мг/кг", "в/в", "нагрузочная в 1-й день первого цикла", "каждые 21 день"),
          drug("Пертузумаб", "840 мг нагрузочная, далее 420 мг", "в/в", "нагрузочная в 1-й день первого цикла", "каждые 21 день")],
         "нерезектабельный/метастатический билиарный рак", bio=["гиперэкспрессия или амплификация HER2/neu (ERBB2)", "«дикий» тип гена RAS"],
         uur="C", udd=5, refs=["157"],
         cite="Javle M., Borad M.J., Azad N.S. et al. Pertuzumab and trastuzumab for HER2-positive, metastatic biliary tract cancer (MyPathway)",
         special="** ЖНВЛП; при ко-мутации BRAF/RAS отмечено значимое снижение эффективности"),
    base("C7", tgt_line, ["таргетная терапия"], "Дабрафениб + траметиниб",
         [drug("Дабрафениб", None, "внутрь", None), drug("Траметиниб", None, "внутрь", None)],
         "нерезектабельный/метастатический билиарный рак", bio=["мутация BRAF V600E"],
         uur="C", udd=5, refs=["158"],
         cite="Subbiah V., Lassen U., Élez E. et al. Dabrafenib plus trametinib in patients with BRAF(V600E)-mutated biliary tract cancer (ROAR)",
         special="** ЖНВЛП; объективный эффект у 51% пациентов (ROAR)" + no_dose),
    base("C7", tgt_line, ["таргетная терапия"], "Вемурафениб + кобиметиниб",
         [drug("Вемурафениб", None, "внутрь", None), drug("Кобиметиниб", None, "внутрь", None)],
         "нерезектабельный/метастатический билиарный рак", bio=["мутация BRAF V600E"],
         uur="C", udd=5, refs=["176"],
         cite="Meric-Bernstam F., Rothe M., Mangat P.K. et al. Cobimetinib Plus Vemurafenib in Patients With Solid Tumors With BRAF Mutations (TAPUR)",
         special="** ЖНВЛП; объективный эффект у 57% пациентов (TAPUR)" + no_dose),
    base("C7", tgt_line, ["таргетная терапия"], "Селперкатиниб",
         [drug("Селперкатиниб", None, "внутрь", None)],
         "нерезектабельный/метастатический билиарный рак", bio=["транслокация гена RET"],
         uur="C", udd=5, refs=["179"],
         cite="Subbiah V., Wolf J., Konda B. et al. Tumour-agnostic efficacy and safety of selpercatinib in patients with RET fusion-positive solid tumours other than lung or thyroid tumours (LIBRETTO-001)",
         special="** ЖНВЛП" + no_dose),
    base("C7", tgt_line, ["таргетная терапия"], "Эрдафитиниб",
         [drug("Эрдафитиниб", None, "внутрь", None)],
         "нерезектабельный/метастатический билиарный рак", bio=["проканцерогенные транслокации генов FGFR1–4"],
         uur="C", udd=5, refs=["185"],
         cite="Pant S., Schuler M., Iyer G. et al. Erdafitinib in patients with advanced solid tumours with FGFR alterations (RAGNAR): an international, single-arm, phase 2 study",
         special="** ЖНВЛП; ЧОО 60% (RAGNAR)" + no_dose),
]

audit.event(DOC, "phase2-start", "495_2 рак желчевыводящей системы: cohort-first extraction")
audit.read_block(DOC, "495_2.md", 1218, 1286, "§3.3 Химиотерапия: адъювантная, ХЛТ, 1L/2L, таблица 6 режимов")
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
