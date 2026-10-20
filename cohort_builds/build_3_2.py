# -*- coding: utf-8 -*-
"""Build cohorts + medication regimens for doc 3_2 (рак полости носа и придаточных пазух)."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit  # noqa: E402

DOC = "3_2"

DISEASE = {
    "name": "Злокачественные новообразования полости носа и придаточных пазух",
    "icd10": "C30.0 (полость носа), C31.0–C31.9 (придаточные пазухи)",
    "histology_type": "плоскоклеточный рак (наиболее часто), аденокарцинома, аденокистозный рак, синоназальная недифференцированная карцинома (SNUC), эстезионейробластома, синоназальный нейроэндокринный рак (исключая меланому, саркому, лимфому)",
}

def drug(inn, dose, route, schedule, cycle_frequency=None, max_cycles=None):
    return {"inn": inn, "dose": dose, "route": route, "schedule": schedule,
            "cycle_frequency": cycle_frequency, "max_cycles": max_cycles}

def base(cid, line, ttype, name, drugs, stage, ecog=None, bio=None, uur=None, udd=None,
         section="3.1", refs=None, cite=None, special="", maint=None, table=None):
    return {
        "cohort_id": cid, "disease": DISEASE,
        "treatment": {"line_stage": line, "therapy_type": ttype, "regimen_name": name},
        "drugs": drugs,
        "indications": {"stage": stage, "ecog": ecog, "biomarkers": bio or []},
        "evidence": {"uur": uur, "udd": udd},
        "source": {"page": None, "section": section, "table": table,
                   "references": refs or [], "citation": cite},
        "special_conditions": special,
        "maintenance_therapy": maint,
    }

REF_NCCN = ["5"]
CITE_NCCN = "NCCN Clinical Practice Guidelines in Oncology (NCCN Guidelines®). Head and Neck Cancers. Version 2.2023"
RUSSCO_HN = ("Болотина Л.В., Владимирова Л.Ю., Деньгина Н.В., Новик А.В., Романов И.С. "
             "Практические рекомендации по лечению злокачественных опухолей головы и шеи. RUSSCO")

cohorts = [
    {"cohort_id": "C1", "disease": DISEASE, "stage": "рак полости носа/клеток решетчатого лабиринта, T1–T2, первично выявленный",
     "resectability": "резектабельный", "clinical_situation": "первичный процесс",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["хирургическое лечение + послеоперационная ЛТ (лекарственная терапия не предусмотрена)"],
     "source": {"section": "3 (Общая концепция лечения)"}},
    {"cohort_id": "C2", "disease": DISEASE, "stage": "рак полости носа/клеток решетчатого лабиринта, T3–T4a, первично выявленный",
     "resectability": "резектабельный/погранично резектабельный", "clinical_situation": "первичный процесс",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["хирургия на первом этапе, либо ЛТ/ХЛТ, либо индукционная ХТ с последующей операцией или сочетанной ХЛТ; далее послеоперационная ЛТ или одновременная ХЛТ"],
     "source": {"section": "3 (Общая концепция лечения)"}},
    {"cohort_id": "C3", "disease": DISEASE, "stage": "рак полости носа/клеток решетчатого лабиринта, T4b N0–N3 M0, либо отказ от обширной операции, либо абсолютные противопоказания к хирургии",
     "resectability": "нерезектабельный", "clinical_situation": "первичный процесс",
     "ecog": "ECOG 0–1: одновременная ХЛТ или ИХТ с последующей ЛТ/ХЛТ; ECOG 2: ЛТ ± ХТ; ECOG 3: паллиативная ЛТ или монохимиотерапия или паллиативная помощь",
     "biomarkers": [], "treatment_stages": ["клинические исследования или выбор метода по ECOG"], "source": {"section": "3 (Общая концепция лечения)"}},
    {"cohort_id": "C4", "disease": DISEASE, "stage": "рак верхнечелюстной пазухи T1–T4a (T1–T2 N0 любая гистология кроме аденокистозного рака; T1–T2 N0 аденокистозный рак; T3–T4a N0; T1–T4a N+)",
     "resectability": "резектабельный", "clinical_situation": "первичный процесс",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["радикальная операция; после операции ЛТ или одновременная/конкурентная ХЛТ при неблагоприятных прогностических факторах (края резекции, периневральная/сосудистая/лимфатическая инвазия, экстракапсулярное распространение)"],
     "source": {"section": "3 (Общая концепция лечения)"}},
    {"cohort_id": "C5", "disease": DISEASE, "stage": "рак верхнечелюстной пазухи T4b N0–N3 M0, либо отказ от обширного хирургического вмешательства",
     "resectability": "нерезектабельный", "clinical_situation": "первичный процесс",
     "ecog": "ECOG 0–1: одновременная ХЛТ или ИХТ с последующей ЛТ/ХЛТ; ECOG 2: ЛТ ± ХТ; ECOG 3: паллиативная ЛТ или монохимиотерапия или паллиативная помощь",
     "biomarkers": [], "treatment_stages": ["клинические исследования или выбор метода по ECOG"], "source": {"section": "3 (Общая концепция лечения)"}},
    {"cohort_id": "C6", "disease": DISEASE, "stage": "локальный рецидив или остаточная опухоль без предшествующей лучевой терапии",
     "resectability": None, "clinical_situation": "рецидив/остаточная опухоль",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["хирургическое вмешательство, или одновременная ХЛТ, или индукционная ХТ с последующей одновременной ХЛТ"], "source": {"section": "3 (Общая концепция лечения)"}},
    {"cohort_id": "C7", "disease": DISEASE, "stage": "локальный рецидив или остаточная опухоль после лучевой терапии",
     "resectability": None, "clinical_situation": "рецидив после ЛТ",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["хирургическое вмешательство с обсуждением повторной ЛТ либо повторная ЛТ с последующей противорецидивной ХТ"], "source": {"section": "3 (Общая концепция лечения)"}},
    {"cohort_id": "C8", "disease": DISEASE, "stage": "локальный рецидив или остаточная опухоль с отдалёнными метастазами (M1)",
     "resectability": None, "clinical_situation": "диссеминация",
     "ecog": "ECOG 0–1: одновременная ХЛТ или индукционная ХТ; ECOG 2: ЛТ ± одновременная ХТ; ECOG 3: паллиативная ЛТ или монохимиотерапия или паллиативная помощь",
     "biomarkers": [], "treatment_stages": ["клинические исследования или выбор метода по ECOG"], "source": {"section": "3 (Общая концепция лечения)"}},
    {"cohort_id": "C9", "disease": DISEASE, "stage": "синоназальная недифференцированная карцинома, низкодифференцированная эстезионейробластома или синоназальный нейроэндокринный рак (любая стадия, требующая системной терапии)",
     "resectability": None, "clinical_situation": "агрессивные гистологические варианты",
     "ecog": None,
     "biomarkers": ["гистология: SNUC / низкодифференцированная эстезионейробластома / синоназальный нейроэндокринный рак"],
     "treatment_stages": ["системная химиотерапия включается в план лечения; индукционная ПХТ перед операцией/ЛТ"], "source": {"section": "3 (Общая концепция лечения); 3.2"}},
    {"cohort_id": "C10", "disease": DISEASE, "stage": "рецидивные, первично-неоперабельные опухоли или метастатический опухолевый процесс при невозможности проведения одновременной ХЛТ",
     "resectability": None, "clinical_situation": "противорецидивная поли-/монохимиотерапия",
     "ecog": "часть режимов только для ECOG 0–1/ECOG 2; монотерапии — для пациентов с ECOG >2 баллов",
     "biomarkers": ["PD-L1 CPS ≥1 (пембролизумаб 1-я линия)", "PD-L1 TPS ≥50 (пембролизумаб после платины)", "платинорезистентность (ниволумаб 2L+)"],
     "treatment_stages": ["поли- или монохимиотерапия; количество курсов определяется переносимостью и эффективностью"], "source": {"section": "3.2"}},
]

R = []
crt_note = "# off-label у компонентов; тот же подход применяется при нерезектабельных опухолях (T4b, ECOG 0–1) и локальном рецидиве без предшествующей ЛТ"

# ---- ХЛТ (§3.1 / §3.2) ----
crt_refs = REF_NCCN + ["27", "71"]; crt_cite = "Beckmann G.K., Hoppe F., Pfreundner L., Flentje M.P. Hyperfractionated accelerated radiotherapy in combination with weekly cisplatin for locally advanced head and neck cancer. Head Neck 2005;27:36-43"
for cid, stg in (("C2", "рак полости носа/решетчатого лабиринта T3–T4a"),
                 ("C4", "рак верхнечелюстной пазухи T1–T4a (после операции при неблагоприятных прогностических факторах)")):
    R += [
        base(cid, "одновременная химиолучевая терапия (послеоперационная/радикальная)", ["химиолучевая терапия (ХЛТ)", "химиотерапия"],
             "Цисплатин + ЛТ (цисплатин в дни 1, 22, 43)",
             [drug("Цисплатин", "100 мг/м² (суммарно за курс ЛТ — 300 мг/м²)", "в/в", "в 1, 22 и 43-й дни ЛТ на фоне гипергидратации (ЛТ 66–70 Гр, 2 Гр/фракция)")],
             stg, uur="C", udd=4, section="3.1", refs=crt_refs, cite=crt_cite, special="** ЖНВЛП; " + crt_note),
        base(cid, "одновременная химиолучевая терапия (послеоперационная/радикальная)", ["химиолучевая терапия (ХЛТ)", "химиотерапия"],
             "Цисплатин еженедельный + ЛТ",
             [drug("Цисплатин", "40 мг/м²", "в/в", "еженедельно на фоне гипергидратации во время ЛТ")],
             stg, uur="C", udd=4, section="3.1", refs=crt_refs, cite=crt_cite, special="# off-label (** ЖНВЛП); предпочтительна сочетанная ХЛТ; " + crt_note),
        base(cid, "одновременная химиолучевая терапия (альтернатива платине)", ["химиолучевая терапия (ХЛТ)", "химиотерапия"],
             "Карбоплатин еженедельный + ЛТ",
             [drug("Карбоплатин", "AUC 1,5–2 (70 мг/м²)", "в/в", "еженедельно, до 7 введений")],
             stg, uur="C", udd=4, section="3.1", refs=REF_NCCN + ["18", "19", "27", "72", "75"], cite="Haddad R., O'Neill A., Rabinowits G. et al. Induction chemotherapy followed by concurrent chemoradiotherapy (sequential chemoradiotherapy) versus concurrent chemoradiotherapy alone in locally advanced head and neck cancer", special="** ЖНВЛП; " + crt_note),
        base(cid, "одновременная химиолучевая терапия (при противопоказаниях к соединениям платины)", ["химиолучевая терапия (ХЛТ)", "таргетная терапия"],
             "Цетуксимаб + ЛТ",
             [drug("Цетуксимаб", "400 мг/м² нагрузочная, далее 250 мг/м²", "в/в", "400 мг/м² за неделю до начала ЛТ, далее еженедельно во время ЛТ")],
             stg, ecog="предпочтителен при противопоказаниях к платине (ХПН, СКФ <50–60 мл/мин, возраст >65 лет, выраженная сопутствующая патология, ECOG >1)",
             uur="A", udd=2, section="3.1", refs=["18", "19", "58", "59"],
             cite="Ang K.K., Zhang Q., Rosenthal D.I. et al. Randomized phase III trial of concurrent accelerated radiation plus cisplatin with or without cetuximab for stage III to IV head and neck carcinoma: RTOG 0522. J Clin Oncol 2014",
             special="** ЖНВЛП; предпочтительная замена соединений платины при ХПН/СКФ<50–60 мл/мин, возрасте >65 лет, выраженной сопутствующей патологии и/или ECOG >1"),
    ]

# ---- Индукционная ХТ (§3.2) ----
R += [
    base("C2", "индукционная химиотерапия (ИХТ) с последующей одновременной ХЛТ", ["химиотерапия"], "TPF (доцетаксел + цисплатин + фторурацил)",
         [drug("Доцетаксел", None, "в/в", None), drug("Цисплатин", None, "в/в", None), drug("Фторурацил", None, "в/в", None)],
         "рак полости носа/решетчатого лабиринта T3–T4a (также применим при T4b ECOG 0–1 и рецидиве без предшествующей ЛТ)",
         bio=["ECOG 0–1 (предположительно, для режима ИХТ)"],
         uur="A", udd=2, section="3.2", refs=["75"], cite=RUSSCO_HN,
         special="** ЖНВЛП; всего 2–3 курса с интервалом 3 недели; дозы компонентов в данном разделе не приведены (см. профильные КР по раку гортани/головы и шеи)"),
    base("C9", "индукционная химиотерапия (SNUC / нейроэндокринный рак / эстезионейробластома)", ["химиотерапия"], "Карбоплатин + этопозид",
         [drug("Карбоплатин", "AUC 5–6", "в/в", None, None, None), drug("Этопозид", "100 мг/м²", "в/в", "1–3 дни")],
         "синоназальная недифференцированная карцинома / низкодифференцированная эстезионейробластома / синоназальный нейроэндокринный рак",
         uur="A", udd=2, section="3.2", refs=["46", "49", "75"],
         cite="Patil V.M., Joshi A., Noronha V. et al. Neoadjuvant chemotherapy in locally advanced and borderline resectable nonsquamous sinonasal tumors (esthesioneuroblastoma and sinonasal tumor with neuroendocrine differentiation)",
         special="** ЖНВЛП; интервал 3 недели"),
    base("C9", "индукционная химиотерапия (SNUC / нейроэндокринный рак / эстезионейробластома)", ["химиотерапия"], "Цисплатин + этопозид",
         [drug("Цисплатин", "75 мг/м²", "в/в", None, None, None), drug("Этопозид", "100 мг/м²", "в/в", "1–3 дни")],
         "синоназальная недифференцированная карцинома / низкодифференцированная эстезионейробластома / синоназальный нейроэндокринный рак",
         uur="A", udd=2, section="3.2", refs=["46", "49", "75"],
         cite="Resto V.A., Eisele D.W., Forastiere A. et al. Esthesioneuroblastoma: the Johns Hopkins experience. Head Neck 2000;22:550-558",
         special="** ЖНВЛП; интервал 3 недели"),
    base("C9", "индукционная химиотерапия (SNUC / нейроэндокринный рак / эстезионейробластома)", ["химиотерапия"], "Циклофосфамид + винкристин + доксорубицин + цисплатин",
         [drug("Циклофосфамид", "500 мг/м²", "в/в", "1-й день", "каждые 3 недели"), drug("Доксорубицин", "50 мг/м²", "в/в", "1-й день", "каждые 3 недели"),
          drug("Винкристин", None, "в/в", None, "каждые 3 недели"), drug("Цисплатин", "50 мг/м²", "в/в", None, "каждые 3 недели")],
         "синоназальная недифференцированная карцинома / низкодифференцированная эстезионейробластома / синоназальный нейроэндокринный рак",
         uur="A", udd=2, section="3.2", refs=["46", "49", "75"], cite=RUSSCO_HN,
         special="** ЖНВЛП (# off-label у циклофосфамида/винкристина); доза винкристина не указана в документе"),
]

# ---- Противорецидивная поли-/монохимиотерапия (таблица §3.2) ----
tbl = "Таблица режимов противорецидивной поли-/монохимиотерапии"
rec_line = "противорецидивная химиотерапия (рецидивные, первично-неоперабельные опухоли или метастатический процесс)"
rec_stage = "рецидивные, первично-неоперабельные опухоли или метастатический процесс при невозможности одновременной ХЛТ"
uur_rec, udd_rec = "C", 5
R += [
    base("C10", rec_line + ", 1-я линия", ["химиотерапия", "таргетная терапия"], "PF + Cet",
         [drug("Цисплатин", "75–100 мг/м²", "в/в", "1-й день", "каждые 3 недели", 6),
          drug("Фторурацил", "1000 мг/м²/сут", "в/в", "96-часовая инфузия, 1–4-й дни", "каждые 3 недели", 6),
          drug("Цетуксимаб", "400 мг/м² (нагрузочная), затем 250 мг/м²", "в/в", "нагрузочная в 1-й день, далее еженедельно", "еженедельно", "до прогрессирования или непереносимой токсичности")],
         rec_stage, uur=uur_rec, udd=udd_rec, section="3.2", refs=["75"], cite=RUSSCO_HN,
         maint="После 6 циклов ХТ завершается; при отсутствии прогрессирования — поддерживающая терапия цетуксимабом 250 мг/м² в/в еженедельно",
         table=tbl),
    base("C10", rec_line + ", 1-я линия", ["химиотерапия", "таргетная терапия"], "DC + Cet",
         [drug("Доцетаксел", "75 мг/м²", "в/в", "1-й день", "каждые 3 недели", 4),
          drug("Цисплатин", "75 мг/м²", "в/в", "1-й день", "каждые 3 недели", 4),
          drug("Цетуксимаб", "400 мг/м² (нагрузочная), затем 250 мг/м²", "в/в", "нагрузочная в 1-й день, далее еженедельно", "еженедельно", "до прогрессирования или непереносимой токсичности")],
         rec_stage, uur=uur_rec, udd=udd_rec, section="3.2", refs=["75", "76"],
         cite="Guigay J., Fayette J., Dillies A-F. et al. Cetuximab, docetaxel, and cisplatin (TPEx) as first-line treatment in patients with recurrent or metastatic squamous cell carcinoma of the head and neck",
         maint="После 4 циклов ХТ завершается; поддерживающая терапия цетуксимабом 500 мг/м² в/в 1 раз в 2 недели",
         table=tbl),
    base("C10", rec_line + ", 1-я линия", ["химиотерапия", "таргетная терапия"], "Цисплатин + Cet",
         [drug("Цисплатин", "75–100 мг/м²", "в/в", None, "1 раз в 3 недели", "не более 6–8 введений"),
          drug("Цетуксимаб", "400 мг/м² (нагрузочная), затем 250 мг/м²", "в/в", "нагрузочная в 1-й день, далее еженедельно", "еженедельно", "до прогрессирования или непереносимой токсичности")],
         rec_stage, uur=uur_rec, udd=udd_rec, section="3.2", refs=["75"], cite=RUSSCO_HN, table=tbl),
    base("C10", rec_line + ", 1-я линия", ["химиотерапия", "таргетная терапия"], "Pacli + Carbo + Cet",
         [drug("Паклитаксел", "100 мг/м²", "в/в", "1-й и 8-й дни", "21-дневный цикл", 6),
          drug("Карбоплатин", "AUC 2,5", "в/в", "1-й и 8-й дни", "21-дневный цикл", 6),
          drug("Цетуксимаб", "400 мг/м² (нагрузочная, 2-часовая инфузия), затем 250 мг/м² (1-часовая инфузия)", "в/в", "нагрузочная в 1-й день 1-го цикла, далее еженедельно", "еженедельно", "до прогрессирования или непереносимой токсичности")],
         rec_stage, uur=uur_rec, udd=udd_rec, section="3.2", refs=["75", "77"],
         cite="Herbst R.S., Arquette M., Shin D.M. et al. Phase II multicenter study of the epidermal growth factor receptor antibody cetuximab and cisplatin for recurrent and refractory squamous cell carcinoma of the head and neck",
         maint="После 6 циклов ХТ — поддерживающая терапия цетуксимабом 250 мг/м² в/в еженедельно",
         table=tbl),
    base("C10", rec_line + ", 1-я линия", ["химиотерапия", "таргетная терапия"], "Pacli + Carbo + Cet (еженедельный)",
         [drug("Паклитаксел", "80 мг/м²", "в/в", "еженедельно", "еженедельно", None),
          drug("Карбоплатин", "AUC 2,0", "в/в", "еженедельно", "еженедельно", None),
          drug("Цетуксимаб", "400 мг/м² (нагрузочная, 2-часовая инфузия), затем 250 мг/м²", "в/в", "нагрузочная в 1-й день 1-го цикла, далее еженедельно", "еженедельно", "до прогрессирования или непереносимой токсичности")],
         rec_stage, ecog="для пациентов в общем состоянии по ECOG 2 балла",
         uur=uur_rec, udd=udd_rec, section="3.2", refs=["75", "78"],
         cite="Geraghty L., Schultz T.E., Hoffman S. et al. Weekly vs. 3-weekly paclitaxel, carboplatin, and cetuximab (PCC) in recurrent/metastatic head and neck cancer",
         special="** ЖНВЛП; количество введений цитостатиков определяется индивидуально", table=tbl),
    base("C10", rec_line + ", 1-я линия", ["химиотерапия"], "PF",
         [drug("Цисплатин", "75–100 мг/м²", "в/в", "1-й день", "каждые 3 недели"),
          drug("Фторурацил", "1000 мг/м²/сут", "в/в", "96-часовая инфузия, 1–4-й дни", "каждые 3 недели")],
         rec_stage, uur=uur_rec, udd=udd_rec, section="3.2", refs=["75", "79", "80"],
         cite="Gibson M.K., Li Y., Murphy B. et al. Randomized phase III evaluation of cisplatin plus fluorouracil versus cisplatin plus paclitaxel in advanced head and neck cancer (E1395)", table=tbl),
    base("C10", rec_line + ", 1-я линия", ["химиотерапия"], "Карбоплатин + фторурацил",
         [drug("Карбоплатин", "AUC 5", "в/в", "1-й день", "каждые 3 недели", "6 (при отсутствии токсичности и положительной динамике — до 8)"),
          drug("Фторурацил", "1000 мг/м²/сут", "в/в", "96-часовая инфузия, 1–4-й дни", "каждые 3 недели", "6 (при отсутствии токсичности и положительной динамике — до 8)")],
         rec_stage, uur=uur_rec, udd=udd_rec, section="3.2", refs=["81", "70"],
         cite="Denis F., Garaud P., Bardet E. et al. Final results of the 94-01 French Head and Neck Oncology and Radiotherapy Group randomized trial comparing radiotherapy alone with concomitant radiochemotherapy in advanced-stage disease", table=tbl),
    base("C10", rec_line + ", 1-я линия", ["химиотерапия"], "Pacli + Carbo",
         [drug("Паклитаксел", "175 мг/м²", "в/в", "1-й день", "каждые 3 недели", "6 (возможно до 8)"),
          drug("Карбоплатин", "AUC 5–6", "в/в", "1-й день", "каждые 3 недели", "6 (возможно до 8)")],
         rec_stage, uur=uur_rec, udd=udd_rec, section="3.2", refs=["75", "83"],
         cite="Samlowski W.E., Moon J., Kuebler J.P. et al. Evaluation of the combination of docetaxel/carboplatin in patients with metastatic or recurrent squamous cell carcinoma of the head and neck (SWOG)",
         special="Неоптимальный режим лечения; возможен к применению только в случае абсолютных противопоказаний к назначению анти-EGFR МКА", table=tbl),
    base("C10", rec_line + ", 1-я линия", ["химиотерапия"], "Паклитаксел еженедельный + карбоплатин еженедельный",
         [drug("Паклитаксел", "60–80 мг/м²", "в/в", "еженедельно", "еженедельно", "до прогрессирования или неприемлемой токсичности, но не более 18 недель"),
          drug("Карбоплатин", "AUC 2", "в/в", "еженедельно", "еженедельно", "до прогрессирования или неприемлемой токсичности, но не более 18 недель")],
         rec_stage, uur=uur_rec, udd=udd_rec, section="3.2", refs=["75", "84"],
         cite="Pêtre A., Dalban C., Karabajakian A. et al. Carboplatin in combination with weekly paclitaxel as first-line treatment in recurrent/metastatic head and neck squamous cell carcinoma",
         special="Неоптимальный режим лечения; возможен к применению только в случае абсолютных противопоказаний к назначению анти-EGFR МКА", table=tbl),
    base("C10", rec_line + ", 1-я линия", ["химиотерапия"], "DC (доцетаксел + цисплатин)",
         [drug("Доцетаксел", "75 мг/м²", "в/в", "1-й день", "каждые 3 недели", "6 (возможно до 8)"),
          drug("Цисплатин", "75 мг/м²", "в/в", "1-й день", "каждые 3 недели", "6 (возможно до 8)")],
         rec_stage, uur=uur_rec, udd=udd_rec, section="3.2", refs=["75", "85", "86"],
         cite="Specht L., Kornum Larsen S., Sand Hansen H. Phase II study of docetaxel and cisplatin in patients with recurrent or disseminated squamous-cell carcinoma of the head and neck. Annals of Oncology 2000;11:845-849",
         special="Неоптимальный режим лечения; возможен к применению только в случае абсолютных противопоказаний к назначению анти-EGFR МКА", table=tbl),
    base("C10", rec_line + ", 2-я и последующие линии", ["иммунотерапия"], "Ниволумаб монотерапия",
         [drug("Ниволумаб", "3 мг/кг, или 240 мг, или 480 мг", "в/в", "60-минутная инфузия (первое введение), далее 30-минутная; 3 мг/кг или 240 мг — 1 раз в 2 нед, 480 мг — 1 раз в 4 нед", "каждые 2 или 4 недели", "до прогрессирования или неприемлемой токсичности, но не более 2 лет")],
         rec_stage, bio=["платинорезистентная опухоль (может назначаться независимо от уровня экспрессии PD-L1)"],
         uur=uur_rec, udd=udd_rec, section="3.2", refs=["75"], cite=RUSSCO_HN,
         special="** ЖНВЛП; во 2-й и последующих линиях терапии при платинорезистентных опухолях", table=tbl),
    base("C10", rec_line + ", иммунотерапия (1-я линия при PD-L1 CPS ≥1; после прогрессирования на платине при TPS ≥50)", ["иммунотерапия"], "Пембролизумаб монотерапия",
         [drug("Пембролизумаб", "200 мг или 400 мг", "в/в", "30-минутная инфузия; 200 мг 1 раз в 3 нед или 400 мг 1 раз в 6 нед", "каждые 3 или 6 недель", "до прогрессирования или неприемлемой токсичности, но не более 2 лет")],
         rec_stage, bio=["экспрессия PD-L1 CPS ≥1 (1-я линия)", "PD-L1 TPS ≥50% (при прогрессировании после ХТ с препаратами платины)"],
         uur=uur_rec, udd=udd_rec, section="3.2", refs=["75"], cite=RUSSCO_HN,
         special="** ЖНВЛП; длительность применения соответствует дизайну регистрационных исследований", table=tbl),
    base("C10", rec_line + ", 1-я линия", ["химиотерапия", "иммунотерапия"], "PF + Пембролизумаб",
         [drug("Пембролизумаб", "200 мг", "в/в", None, "1 раз в 3 недели", "6 циклов ХТ, далее поддержание"),
          drug("Карбоплатин", "AUC 5", "в/в", None, "1 раз в 3 недели", 6),
          drug("Цисплатин", "100 мг/м²", "в/в", None, "1 раз в 3 недели", 6),
          drug("Фторурацил", "1000 мг/м²", "в/в", "1–4 дни", "1 раз в 3 недели", 6),
          drug("Пембролизумаб (поддержание)", "200 мг или 400 мг", "в/в", "200 мг 1 раз в 3 нед или 400 мг 1 раз в 6 нед", "каждые 3 или 6 недель", "до 35 введений в целом")],
         rec_stage, bio=["PD-L1 CPS ≥1"],
         uur=uur_rec, udd=udd_rec, section="3.2", refs=["75", "87"],
         cite="Burtness B., Harrington K.J., Greil R. et al. Pembrolizumab alone or with chemotherapy versus cetuximab with chemotherapy for recurrent or metastatic squamous cell carcinoma of the head and neck (KEYNOTE-048)",
         special="** ЖНВЛП; в качестве 1-й линии при CPS ≥1; карбоплатин AUC 5 ИЛИ цисплатин 100 мг/м² (один из препаратов платины)",
         maint="После 6 циклов ХТ — пембролизумаб 200 мг 1 раз в 3 недели или 400 мг 1 раз в 6 недель, максимум до 35 введений в целом",
         table=tbl),
]

# Монотерапии для ECOG >2
mono_refs = ["75"]
mono_line = rec_line + " (монотерапия для пациентов в общем состоянии по ECOG >2 баллов)"
mono_specs = "** ЖНВЛП; количество введений определяется индивидуально"
R += [
    base("C10", mono_line, ["химиотерапия"], "Цисплатин монотерапия",
         [drug("Цисплатин", "60–70 мг/м²", "в/в", None, "1 раз в 3 недели", "количество введений индивидуально (целесообразность >6–8 введений сомнительна)")],
         rec_stage, ecog="ECOG >2 баллов", uur=uur_rec, udd=udd_rec, section="3.2", refs=mono_refs, cite=RUSSCO_HN, special=mono_specs, table=tbl),
    base("C10", mono_line, ["химиотерапия"], "Карбоплатин монотерапия",
         [drug("Карбоплатин", "AUC 5–6, или AUC 2 еженедельно", "в/в", None, "1 раз в 3 недели или еженедельно", "количество введений определяется индивидуально")],
         rec_stage, ecog="ECOG >2 баллов", uur=uur_rec, udd=udd_rec, section="3.2", refs=mono_refs, cite=RUSSCO_HN, special=mono_specs, table=tbl),
    base("C10", mono_line, ["химиотерапия"], "Паклитаксел монотерапия",
         [drug("Паклитаксел", "175 мг/м² 1 раз в 3 нед или 80 мг/м² еженедельно", "в/в", None, "1 раз в 3 недели или еженедельно", "количество введений определяется индивидуально")],
         rec_stage, ecog="ECOG >2 баллов", uur=uur_rec, udd=udd_rec, section="3.2", refs=mono_refs, cite=RUSSCO_HN, special=mono_specs, table=tbl),
    base("C10", mono_line, ["химиотерапия"], "Доцетаксел монотерапия",
         [drug("Доцетаксел", "70–75 мг/м²", "в/в", None, "1 раз в 3 недели", "количество введений определяется индивидуально")],
         rec_stage, ecog="ECOG >2 баллов", uur=uur_rec, udd=udd_rec, section="3.2", refs=mono_refs, cite=RUSSCO_HN, special=mono_specs, table=tbl),
    base("C10", mono_line, ["химиотерапия"], "Капецитабин монотерапия",
         [drug("Капецитабин", "2000 мг/м² внутрь в 2 приема, или 2000 мг/сут ежедневно (метрономный режим)", "внутрь", "1–14-й дни с перерывом 1 неделя, либо ежедневно в метрономном режиме", None, "длительность терапии определяется индивидуально")],
         rec_stage, ecog="ECOG >2 баллов", uur=uur_rec, udd=udd_rec, section="3.2", refs=mono_refs, cite=RUSSCO_HN, special=mono_specs, table=tbl),
    base("C10", mono_line, ["химиотерапия"], "Метотрексат монотерапия",
         [drug("Метотрексат", "40 мг/м²", "в/в", "еженедельно", "еженедельно", "количество введений определяется индивидуально")],
         rec_stage, ecog="ECOG >2 баллов", uur=uur_rec, udd=udd_rec, section="3.2", refs=mono_refs, cite=RUSSCO_HN, special=mono_specs, table=tbl),
    base("C10", mono_line, ["таргетная терапия"], "Цетуксимаб монотерапия",
         [drug("Цетуксимаб", "400 мг/м² (нагрузочная, 2-часовая инфузия), затем 250 мг/м²", "в/в", "нагрузочная в 1-й день 1-го курса, далее еженедельно", "еженедельно", None)],
         rec_stage, ecog="ECOG >2 баллов", uur=uur_rec, udd=udd_rec, section="3.2", refs=mono_refs, cite=RUSSCO_HN, special="** ЖНВЛП", table=tbl),
]

audit.event(DOC, "phase2-start", "3_2 рак полости носа и придаточных пазух: cohort-first extraction")
audit.read_block(DOC, "3_2.md", 970, 1086, "§3 Общая концепция лечения; §3.1 ЛТ (+ХЛТ цисплатин/карбоплатин/цетуксимаб); §3.2 Лекарственное лечение (ИХТ + таблица противорецидивной ХТ)")
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
