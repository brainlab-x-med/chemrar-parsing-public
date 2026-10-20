# -*- coding: utf-8 -*-
"""Build cohorts + medication regimens for doc 4_2 (рак ротоглотки, C10)."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit  # noqa: E402

DOC = "4_2"

DISEASE = {
    "name": "Злокачественное новообразование ротоглотки (рак ротоглотки)",
    "icd10": "C10 (C10.0–C10.9)",
    "histology_type": "плоскоклеточный рак",
}

def drug(inn, dose, route, schedule, cycle_frequency=None, max_cycles=None):
    return {"inn": inn, "dose": dose, "route": route, "schedule": schedule,
            "cycle_frequency": cycle_frequency, "max_cycles": max_cycles}

def base(cid, line, ttype, name, drugs, stage, ecog=None, bio=None, uur=None, udd=None,
         refs=None, cite=None, special="", maint=None, table=None):
    return {
        "cohort_id": cid, "disease": DISEASE,
        "treatment": {"line_stage": line, "therapy_type": ttype, "regimen_name": name},
        "drugs": drugs,
        "indications": {"stage": stage, "ecog": ecog, "biomarkers": bio or []},
        "evidence": {"uur": uur, "udd": udd},
        "source": {"page": None, "section": "3.4", "table": table,
                   "references": refs or [], "citation": cite},
        "special_conditions": special,
        "maintenance_therapy": maint,
    }

cohorts = [
    {"cohort_id": "C1", "disease": DISEASE,
     "stage": "рак ротоглотки, первичное лечение с индукционной ХТ в качестве первичного метода",
     "resectability": None, "clinical_situation": "индукционная ХТ",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["индукционная ХТ (2–3 курса) с последующей конкурентной ХЛТ"],
     "source": {"section": "3.4"}},
    {"cohort_id": "C2", "disease": DISEASE,
     "stage": "локальный неоперабельный рецидив или остаточная опухоль после ЛТ; отдалённые метастазы",
     "resectability": None, "clinical_situation": "моно-/полихимиотерапия рецидива/метастазов",
     "ecog": "часть режимов — для ECOG 2; монотерапии — для ECOG >2 баллов",
     "biomarkers": ["PD-L1 CPS ≥1 (пембролизумаб 1-я линия)", "PD-L1 TPS ≥50% (пембролизумаб после платины)", "платинорезистентность (ниволумаб 2L+)"],
     "treatment_stages": ["поли-/монохимиотерапия; количество курсов определяется переносимостью и эффективностью"], "source": {"section": "3.4"}},
]

JNVLP = "** ЖНВЛП; "
R = []

# ---- Индукция ----
R += [
    base("C1", "индукционная полихимиотерапия (предпочтительный режим)", ["химиотерапия"],
         "TPF (доцетаксел + цисплатин + фторурацил)",
         [drug("Доцетаксел", "75 мг/м²", "в/в", "1-й день", "каждые 3 недели"),
          drug("Цисплатин", "75 мг/м²", "в/в", "1-й день", "каждые 3 недели"),
          drug("Фторурацил", "1000 мг/м²/сут", "в/в", "1–4-й дни (инфузия)", "каждые 3 недели")],
         "рак ротоглотки при выборе индукционной ХТ как первичного метода лечения",
         uur="C", udd=5, refs=["53"],
         cite="Болотина Л.В., Владимирова Л.Ю., Деньгина Н.В., Новик А.В., Романов И.С. Практические рекомендации по лечению злокачественных опухолей головы и шеи. RUSSCO",
         special="** ЖНВЛП; всего 2–3 курса ХТ с интервалом 3 нед; далее конкурентная ХЛТ"),
    base("C1", "индукционная полихимиотерапия (альтернативный режим)", ["химиотерапия"],
         "Паклитаксел + цисплатин + фторурацил",
         [drug("Паклитаксел", "175 мг/м²", "в/в", "1-й день", "каждые 3 недели", 3),
          drug("Цисплатин", "100 мг/м²", "в/в", "2-й день", "каждые 3 недели", 3),
          drug("Фторурацил", "500 мг/м²", "в/в", "длительная инфузия 2–6 дни", "каждые 3 недели", 3)],
         "рак ротоглотки при выборе индукционной ХТ как первичного метода лечения",
         uur="B", udd=2, refs=["54", "55"],
         cite="Hitt R., Lopez-Pousa A., Martinez-Trufero J. et al. Phase III study comparing cisplatin plus fluorouracil to paclitaxel, cisplatin, and fluorouracil induction chemotherapy followed by chemoradiotherapy in locally advanced head and neck cancer",
         special="** ЖНВЛП; всего 3 курса ХТ с интервалом 3 недели"),
    base("C1", "конкурентная химиолучевая терапия после индукции", ["химиолучевая терапия (ХЛТ)", "химиотерапия"],
         "Цисплатин 100 мг/м² на фоне ЛТ",
         [drug("Цисплатин", "100 мг/м²", "в/в", "на фоне лучевой терапии", "1 раз в 3 недели")],
         "рак ротоглотки после индукционной ХТ", uur="C", udd=4, refs=["56"],
         cite="Jae-Sook Ahn, Sang-Hee Cho, Ok-Ki Kim et al. The Efficacy of an Induction Chemotherapy Combination with Docetaxel, Cisplatin, and 5-FU Followed by Concurrent Chemoradiotherapy",
         special="** ЖНВЛП; с учётом высокой токсичности возможно еженедельное введение карбоплатина AUC 1,5 или цетуксимаба 400 мг/м² за неделю до начала ЛТ и 250 мг/м² еженедельно во время ЛТ; при противопоказаниях к платине (ХПН, выраженная кардиопатология) предпочтительна замена платины на цетуксимаб"),
]

# ---- Таблица №1: рецидив/метастазы ----
rec_line = "моно-/полихимиотерапия локального неоперабельного рецидива, остаточной опухоли после ЛТ или отдалённых метастазов"
tbl = "Таблица №1. Режимы лекарственной терапии плоскоклеточного рака головы и шеи"
R += [
    base("C2", rec_line, ["химиотерапия", "таргетная терапия"], "PF + Cet",
         [drug("Цисплатин", "75–100 мг/м²", "в/в", "1-й день", "каждые 3 недели", 6),
          drug("Фторурацил", "1000 мг/м²/сут", "в/в", "96-часовая инфузия, 1–4-й дни", "каждые 3 недели", 6),
          drug("Цетуксимаб", "400 мг/м² (нагрузочная), далее 250 мг/м²", "в/в", "нагрузочная в 1-й день, далее еженедельно", "еженедельно", "до прогрессирования или непереносимой токсичности")],
         "локальный неоперабельный рецидив/остаточная опухоль/отдалённые метастазы", uur="C", udd=5, refs=["56", "57"],
         cite="Vermorken J.B., Mesia R., Rivera F. et al. Platinum-based chemotherapy plus cetuximab in head and neck cancer. N Engl J Med 2008;359:1116-1127",
         maint="После 6 циклов ХТ завершается; при отсутствии прогрессирования — поддерживающая терапия цетуксимабом 250 мг/м² в/в еженедельно",
         table=tbl),
    base("C2", rec_line, ["химиотерапия", "таргетная терапия"], "DC + Cet",
         [drug("Доцетаксел", "75 мг/м²", "в/в", "1-й день", "каждые 3 недели", 4),
          drug("Цисплатин", "75 мг/м²", "в/в", "1-й день", "каждые 3 недели", 4),
          drug("Цетуксимаб", "400 мг/м² (нагрузочная), далее 250 мг/м²", "в/в", "нагрузочная в 1-й день, далее еженедельно", "еженедельно")],
         "локальный неоперабельный рецидив/остаточная опухоль/отдалённые метастазы", uur="C", udd=5, refs=["57"],
         cite="Vermorken J.B., Mesia R., Rivera F. et al. Platinum-based chemotherapy plus cetuximab in head and neck cancer. N Engl J Med 2008;359:1116-1127",
         maint="После 4 циклов ХТ завершается; поддерживающая терапия цетуксимабом 500 мг/м² в/в 1 раз в 2 недели",
         table=tbl),
    base("C2", rec_line, ["химиотерапия", "таргетная терапия"], "Цисплатин + Cet",
         [drug("Цисплатин", "75–100 мг/м²", "в/в", None, "1 раз в 3 недели", "не более 6–8 введений"),
          drug("Цетуксимаб", "400 мг/м² (нагрузочная), далее 250 мг/м²", "в/в", "нагрузочная в 1-й день, далее еженедельно", "еженедельно", "до прогрессирования или непереносимой токсичности")],
         "локальный неоперабельный рецидив/остаточная опухоль/отдалённые метастазы", uur="C", udd=5, refs=["58"],
         cite="Burtness B., Goldwasser M.A., Flood W. et al. Phase III randomized trial of cisplatin plus placebo compared with cisplatin plus cetuximab in metastatic/recurrent head and neck cancer",
         table=tbl),
    base("C2", rec_line, ["химиотерапия", "таргетная терапия"], "Pacli + Carbo + Cet",
         [drug("Паклитаксел", "100 мг/м²", "в/в", "1-й и 8-й дни", "21-дневный цикл", 6),
          drug("Карбоплатин", "AUC 2,5", "в/в", "1-й и 8-й дни", "21-дневный цикл", 6),
          drug("Цетуксимаб", "400 мг/м² (нагрузочная, 2-часовая инфузия), затем 250 мг/м² (1-часовая инфузия)", "в/в", "нагрузочная в 1-й день 1-го цикла, далее еженедельно", "еженедельно")],
         "локальный неоперабельный рецидив/остаточная опухоль/отдалённые метастазы", uur="C", udd=5, refs=["59", "60"],
         cite="Guigay J., Fayette J., Dillies A-F. et al. Cetuximab, docetaxel, and cisplatin (TPEx) as first-line treatment in patients with recurrent or metastatic squamous cell carcinoma of the head and neck",
         maint="После 6 циклов ХТ — поддерживающая терапия цетуксимабом 250 мг/м² в/в еженедельно",
         table=tbl),
    base("C2", rec_line, ["химиотерапия", "таргетная терапия"], "Pacli + Carbo + Cet (еженедельный)",
         [drug("Паклитаксел", "80 мг/м²", "в/в", "еженедельно", "еженедельно", "количество введений определяется индивидуально"),
          drug("Карбоплатин", "AUC 2,0", "в/в", "еженедельно", "еженедельно"),
          drug("Цетуксимаб", "400 мг/м² (нагрузочная, 2-часовая инфузия), затем 250 мг/м²", "в/в", "нагрузочная в 1-й день 1-го цикла, далее еженедельно", "еженедельно")],
         "локальный неоперабельный рецидив/остаточная опухоль/отдалённые метастазы",
         ecog="для пациентов в общем состоянии по ECOG 2 балла",
         uur="C", udd=5, refs=["61", "62", "63"],
         cite="Herbst R.S., Arquette M., Shin D.M. et al. Phase II multicenter study of the epidermal growth factor receptor antibody cetuximab and cisplatin for recurrent and refractory squamous cell carcinoma of the head and neck",
         table=tbl),
    base("C2", rec_line, ["химиотерапия"], "PF",
         [drug("Цисплатин", "75–100 мг/м²", "в/в", "1-й день", "каждые 3 недели"),
          drug("Фторурацил", "1000 мг/м²/сут", "в/в", "96-часовая инфузия, 1–4-й дни", "каждые 3 недели")],
         "локальный неоперабельный рецидив/остаточная опухоль/отдалённые метастазы", uur="C", udd=5, refs=["62", "63", "64"],
         cite="Hitt R., Irigoyen A., Cortes-Funes H. et al. Phase II study of the combination of cetuximab and weekly paclitaxel in patients with previously treated advanced squamous cell carcinoma of the head and neck",
         special="** ЖНВЛП", table=tbl),
    base("C2", rec_line, ["химиотерапия"], "Карбоплатин + фторурацил",
         [drug("Карбоплатин", "AUC 5", "в/в", "1-й день", "каждые 3 недели", "6 (возможно до 8)"),
          drug("Фторурацил", "1000 мг/м²/сут", "в/в", "96-часовая инфузия, 1–4-й дни", "каждые 3 недели", "6 (возможно до 8)")],
         "локальный неоперабельный рецидив/остаточная опухоль/отдалённые метастазы", uur="C", udd=5, refs=["53", "66", "67"],
         cite="Болотина Л.В., Владимирова Л.Ю., Деньгина Н.В., Новик А.В., Романов И.С. Практические рекомендации по лечению злокачественных опухолей головы и шеи. RUSSCO",
         table=tbl),
    base("C2", rec_line, ["химиотерапия"], "Pacli + Carbo",
         [drug("Паклитаксел", "175 мг/м²", "в/в", "1-й день", "каждые 3 недели", "6 (возможно до 8)"),
          drug("Карбоплатин", "AUC 5–6", "в/в", "1-й день", "каждые 3 недели", "6 (возможно до 8)")],
         "локальный неоперабельный рецидив/остаточная опухоль/отдалённые метастазы", uur="C", udd=5, refs=["64", "66", "68"],
         cite="Bourhis J., Sire C., Graff P. et al. Concomitant chemoradiotherapy versus acceleration of radiotherapy with or without concomitant chemotherapy in locally advanced head and neck carcinoma (GORTEC 99-02)",
         special="Неоптимальный режим; возможен только при абсолютных противопоказаниях к анти-EGFR МКА", table=tbl),
    base("C2", rec_line, ["химиотерапия"], "Паклитаксел еженедельный + карбоплатин еженедельный",
         [drug("Паклитаксел", "60–80 мг/м²", "в/в", "еженедельно", "еженедельно", "до прогрессирования или неприемлемой токсичности, но не более 18 недель"),
          drug("Карбоплатин", "AUC 2", "в/в", "еженедельно", "еженедельно", "до прогрессирования или неприемлемой токсичности, но не более 18 недель")],
         "локальный неоперабельный рецидив/остаточная опухоль/отдалённые метастазы", uur="C", udd=5, refs=["69", "70"],
         cite="Samlowski W.E., Moon J., Kuebler J.P. et al. Evaluation of the combination of docetaxel/carboplatin in patients with metastatic or recurrent squamous cell carcinoma of the head and neck (SWOG)",
         special="Неоптимальный режим; возможен только при абсолютных противопоказаниях к анти-EGFR МКА", table=tbl),
    base("C2", rec_line, ["химиотерапия"], "DC (доцетаксел + цисплатин)",
         [drug("Доцетаксел", "75 мг/м²", "в/в", "1-й день", "каждые 3 недели", "6 (возможно до 8)"),
          drug("Цисплатин", "75 мг/м²", "в/в", "1-й день", "каждые 3 недели", "6 (возможно до 8)")],
         "локальный неоперабельный рецидив/остаточная опухоль/отдалённые метастазы", uur="C", udd=5, refs=["68", "71"],
         cite="Pêtre A., Dalban C., Karabajakian A. et al. Carboplatin in combination with weekly paclitaxel as first-line treatment in recurrent/metastatic head and neck squamous cell carcinoma",
         special="Неоптимальный режим; возможен только при абсолютных противопоказаниях к анти-EGFR МКА", table=tbl),
    base("C2", rec_line + ", 2-я и последующие линии", ["иммунотерапия"], "Ниволумаб монотерапия",
         [drug("Ниволумаб", "3 мг/кг, или 240 мг, или 480 мг", "в/в", "60-минутная инфузия (первое введение), далее 30-минутная; 3 мг/кг или 240 мг каждые 2 нед, 480 мг каждые 4 нед", "каждые 2 или 4 недели", "до прогрессирования или неприемлемой токсичности, но не более 2 лет")],
         "прогрессирование после платиносодержащей терапии", bio=["платинорезистентная опухоль; назначается независимо от уровня экспрессии PD-L1"],
         uur="C", udd=5, refs=["72"],
         cite="Ferris R.L., Blumenschein G. Jr., Fayette J. et al. Nivolumab for recurrent squamous-cell carcinoma of the head and neck. N Engl J Med 2016;375:1856-1867",
         table=tbl),
    base("C2", rec_line, ["иммунотерапия"], "Пембролизумаб монотерапия",
         [drug("Пембролизумаб", "200 мг или 400 мг", "в/в", "30-минутная инфузия; 200 мг 1 раз в 3 нед или 400 мг 1 раз в 6 нед", "каждые 3 или 6 недель", "до прогрессирования или неприемлемой токсичности, но не более 2 лет")],
         "рецидив/метастатический процесс", bio=["экспрессия PD-L1 CPS ≥1 (1-я линия)", "TPS ≥50% (при прогрессировании на фоне/после платины)"],
         uur="C", udd=5, refs=["74"],
         cite="Burtness B., Harrington K.J., Greil R. et al. Pembrolizumab alone or with chemotherapy versus cetuximab with chemotherapy for recurrent or metastatic squamous cell carcinoma of the head and neck (KEYNOTE-048)",
         special="** ЖНВЛП; длительность соответствует дизайну регистрационных исследований", table=tbl),
    base("C2", rec_line, ["химиотерапия", "иммунотерапия"], "PF + пембролизумаб",
         [drug("Пембролизумаб", "200 мг", "в/в", None, "1 раз в 3 недели", "6 циклов, далее поддержание"),
          drug("Карбоплатин", "AUC 5", "в/в", None, "1 раз в 3 недели", 6),
          drug("Цисплатин", "100 мг/м²", "в/в", None, "1 раз в 3 недели", 6),
          drug("Фторурацил", "1000 мг/м²", "в/в", "1–4 дни", "1 раз в 3 недели", 6),
          drug("Пембролизумаб (поддержание)", "200 мг или 400 мг", "в/в", "200 мг 1 раз в 3 нед или 400 мг 1 раз в 6 нед", "каждые 3 или 6 недель", "максимум до 35 введений в целом")],
         "рецидив/метастатический процесс", bio=["экспрессия PD-L1 ≥1%"],
         uur="C", udd=5, refs=["53", "73", "74"],
         cite="Specht L., Kornum Larsen S., Sand Hansen H. Phase II study of docetaxel and cisplatin in patients with recurrent or disseminated squamous-cell carcinoma of the head and neck. Annals of Oncology 2000;11:845-849",
         special="** ЖНВЛП; карбоплатин AUC 5 ИЛИ цисплатин 100 мг/м² (один из препаратов платины)",
         maint="После 6 циклов — пембролизумаб 200 мг 1 раз в 3 недели или 400 мг 1 раз в 6 недель, максимум до 35 введений в целом",
         table=tbl),
]

# Монотерапии ECOG>2
mono_line = rec_line + " (монотерапия для пациентов в общем состоянии по ECOG >2 баллов)"
mono_specs = "** ЖНВЛП; количество введений определяется индивидуально"
R += [
    base("C2", mono_line, ["химиотерапия"], "Цисплатин монотерапия",
         [drug("Цисплатин", "60–70 мг/м²", "в/в", None, "1 раз в 3 недели", "количество введений индивидуально (>6–8 введений сомнительно)")],
         "локальный неоперабельный рецидив/метастазы", ecog="ECOG >2 баллов", uur="C", udd=5, refs=["58", "73", "74", "75"],
         cite="Jacobs C., Lyman G., Velez-Garcia E. et al. A phase III randomized study comparing cisplatin and fluorouracil as single agents and in combination for advanced squamous cell carcinoma of the head and neck",
         special=JNVLP, table=tbl),
    base("C2", mono_line, ["химиотерапия"], "Карбоплатин монотерапия",
         [drug("Карбоплатин", "AUC 5–6, или AUC 2 еженедельно", "в/в", None, "1 раз в 3 недели или еженедельно", "количество введений индивидуально")],
         "локальный неоперабельный рецидив/метастазы", ecog="ECOG >2 баллов", uur="C", udd=5, refs=["76"],
         cite="Al-Sarraf M., Metch B., Kish J. et al. Platinum analogs in recurrent and advanced head and neck cancer: a Southwest Oncology Group and Wayne State University Study. Cancer Treat Rep",
         special=JNVLP, table=tbl),
    base("C2", mono_line, ["химиотерапия"], "Паклитаксел монотерапия",
         [drug("Паклитаксел", "175 мг/м² 1 раз в 3 нед или 80 мг/м² еженедельно", "в/в", None, "1 раз в 3 недели или еженедельно", "количество введений индивидуально")],
         "локальный неоперабельный рецидив/метастазы", ecog="ECOG >2 баллов", uur="C", udd=5, refs=["74", "77", "78"],
         cite="Burtness B., Harrington K.J., Greil R. et al. Pembrolizumab alone or with chemotherapy versus cetuximab with chemotherapy for recurrent or metastatic squamous cell carcinoma of the head and neck (KEYNOTE-048)",
         special=JNVLP, table=tbl),
    base("C2", mono_line, ["химиотерапия"], "Доцетаксел монотерапия",
         [drug("Доцетаксел", "70–75 мг/м²", "в/в", None, "1 раз в 3 недели", "количество введений индивидуально")],
         "локальный неоперабельный рецидив/метастазы", ecog="ECOG >2 баллов", uur="C", udd=5, refs=["53", "78", "79", "80"],
         cite="Catimel G., Verweij J., Mattijssen V. et al. Docetaxel (Taxotere): an active drug for the treatment of patients with advanced squamous cell carcinoma of the head and neck. EORTC Early Clinical Trials Group",
         special=JNVLP, table=tbl),
    base("C2", mono_line, ["химиотерапия"], "Капецитабин монотерапия",
         [drug("Капецитабин", "2000 мг/м² внутрь в 2 приема, или 2000 мг/сут ежедневно (метрономный режим)", "внутрь", "1–14-й дни с перерывом 1 неделя либо ежедневно в метрономном режиме", None, "длительность определяется индивидуально")],
         "локальный неоперабельный рецидив/метастазы", ecog="ECOG >2 баллов", uur="C", udd=5, refs=["53", "80", "81"],
         cite="Martinez-Trufero J., Isla D., Adansa J.C. et al. Phase II study of capecitabine as palliative treatment for patients with recurrent and metastatic squamous head and neck cancer after previous chemotherapy",
         special=JNVLP, table=tbl),
    base("C2", mono_line, ["химиотерапия"], "Метотрексат монотерапия",
         [drug("Метотрексат", "40 мг/м²", "в/в", "еженедельно", "еженедельно", "количество введений индивидуально")],
         "локальный неоперабельный рецидив/метастазы", ecog="ECOG >2 баллов", uur="C", udd=5, refs=["81", "82", "83"],
         cite="Stewart J.S., Cohen E.E., Licitra L. et al. Phase III study of gefitinib compared with intravenous methotrexate for recurrent squamous cell carcinoma of the head and neck",
         special=JNVLP + "; режим соответствует клиническим исследованиям, при плохой переносимости дозу редуцировать", table=tbl),
    base("C2", mono_line, ["таргетная терапия"], "Цетуксимаб монотерапия",
         [drug("Цетуксимаб", "400 мг/м² (нагрузочная, 2-часовая инфузия), затем 250 мг/м²", "в/в", "нагрузочная в 1-й день 1-го курса, далее еженедельно", "еженедельно")],
         "локальный неоперабельный рецидив/метастазы", ecog="ECOG >2 баллов", uur="C", udd=5, refs=["84", "85"],
         cite="Vermorken J.B., Trigo J., Hitt R. et al. Open-label, uncontrolled, multicenter phase II study to evaluate the efficacy and toxicity of cetuximab as a single agent in patients with recurrent and/or metastatic squamous cell carcinoma of the head and neck",
         special=JNVLP, table=tbl),
]

audit.event(DOC, "phase2-start", "4_2 рак ротоглотки: cohort-first extraction")
audit.read_block(DOC, "4_2.md", 888, 935, "§3.4 Принципы системной химиотерапии: индукция, ХЛТ, таблица №1")
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
