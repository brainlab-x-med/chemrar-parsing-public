#!/usr/bin/env python3
"""Build 585_2 (Первичные опухоли ЦНС) cohorts + regimens, emit audit events."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import json, audit

DOC = "585_2"

audit.event(DOC, "phase2-start", "585_2 Первичные опухоли ЦНС: cohort-first extraction")

DISEASE = {
    "name": "Первичные опухоли центральной нервной системы",
    "icd10": "C70-C72",
    "histology_type": "глиомы (диффузные глиомы взрослого типа: астроцитома IDH-мутантная, олигодендроглиома IDH-мутантная с 1p/19q-коделецией, глиобластома IDH-дикого типа), медуллобластома, первичная лимфома ЦНС, первичные герминогенные опухоли ЦНС, паренхиматозные опухоли шишковидной железы (пинеобластома, пинеоцитома), менингиомы, эпендимомы",
}

cohorts = [
    {"cohort_id": "C1", "disease": DISEASE, "stage": "стадирование TNM не применяется; grade 3–4 (ВОЗ, 2021)", "resectability": None,
     "clinical_situation": "Глиомы (впервые выявленные): проведение ХТ в одном из рекомендованных режимов в зависимости от клинической ситуации и состояния пациента",
     "ecog": None, "biomarkers": ["IDH1/IDH2", "1p/19q-коделеция", "BRAF V600", "H3K27"], "treatment_stages": ["первичная ХТ/ХЛТ"],
     "source": {"section": "3.3"}},
    {"cohort_id": "C1a", "parent": "C1", "disease": DISEASE, "stage": "неоперабельные глиомы; диффузные глиомы ствола мозга; распространённые диффузные интрамедуллярные глиомы", "resectability": "неоперабельные",
     "clinical_situation": "Глиомы: ТМЗ+Бев / монотерапия Бев у пациентов с неоперабельными глиомами", "ecog": None,
     "biomarkers": [], "treatment_stages": ["первичная ХТ"], "source": {"section": "3.3"}},
    {"cohort_id": "C2", "disease": DISEASE, "stage": "рецидивы глиом grade 3–4", "resectability": None,
     "clinical_situation": "Рецидивы глиом: ХТ в одном из рекомендованных режимов", "ecog": None,
     "biomarkers": ["MGMT"], "treatment_stages": ["терапия рецидивов"], "source": {"section": "3.3"}},
    {"cohort_id": "C3", "disease": DISEASE, "stage": "первичная лимфома головного мозга (ЦНС)", "resectability": None,
     "clinical_situation": "Первичная лимфома ЦНС: ХТ в одном из рекомендованных режимов", "ecog": "индекс Карновского >50 для высокодозного метотрексата в 1-й линии (возраст ≤65 лет)",
     "biomarkers": [], "treatment_stages": ["1-я линия", "последующие линии"], "source": {"section": "3.3"}},
    {"cohort_id": "C3a", "parent": "C3", "disease": DISEASE, "stage": "первичная лимфома ЦНС", "resectability": None,
     "clinical_situation": "Пациенты пожилого возраста и/или с низким функциональным статусом (ИК ≤60)", "ecog": "индекс Карновского ≤60",
     "biomarkers": ["MGMT (для монотерапии темозоломидом у пожилых)"], "treatment_stages": ["1-я линия"], "source": {"section": "3.3.1"}},
    {"cohort_id": "C4", "disease": DISEASE, "stage": "первичные герминативно-клеточные опухоли ЦНС (герминома, маркеры АФП/ХГЧ отрицательные)", "resectability": None,
     "clinical_situation": "Первичные герминативно-клеточные опухоли ЦНС: ХТ цисплатин + этопозид", "ecog": None,
     "biomarkers": ["АФП", "ХГЧ (отрицательные)"], "treatment_stages": ["первичная ХТ"], "source": {"section": "3.3"}},
    {"cohort_id": "C5", "disease": DISEASE, "stage": "первичные негерминомные герминативно-клеточные опухоли ЦНС (маркеры АФП/ХГЧ повышены)", "resectability": None,
     "clinical_situation": "Негерминомные герминативно-клеточные опухоли ЦНС: ХТ в одном из режимов", "ecog": None,
     "biomarkers": ["АФП", "ХГЧ (повышены)"], "treatment_stages": ["первичная ХТ"], "source": {"section": "3.3"}},
    {"cohort_id": "C6", "disease": DISEASE, "stage": "медуллобластома, пинеобластома, пинеоцитома с промежуточной дифференцировкой", "resectability": None,
     "clinical_situation": "Медуллобластома/пинеобластома: адъювантная ХТ после удаления опухоли и ЛТ (КСО+буст)", "ecog": None,
     "biomarkers": [], "treatment_stages": ["адъювантная ХТ после ЛТ"], "source": {"section": "3.3"}},
    {"cohort_id": "C7", "disease": DISEASE, "stage": "рецидив анапластической менингиомы / агрессивное течение иных морфологических типов менингиом", "resectability": None,
     "clinical_situation": "Рецидив анапластической менингиомы или агрессивное рецидивирующее течение (прогрессия после ЛТ, шванноматоз) — опция", "ecog": None,
     "biomarkers": [], "treatment_stages": ["терапия рецидивов"], "source": {"section": "3.3"}},
    {"cohort_id": "C8", "disease": DISEASE, "stage": "постлучевые реакции и лучевой некроз после ЛТ (стандартное фракционирование, гипофракционирование, радиохирургия)", "resectability": None,
     "clinical_situation": "Лучевой некроз: бевацизумаб", "ecog": None, "biomarkers": [],
     "treatment_stages": ["лечение осложнений ЛТ"], "source": {"section": "3.3"}},
]

def d(inn, dose, route, sched=None, freq=None, mx=None):
    return {"inn": inn, "dose": dose, "route": route, "schedule": sched,
            "cycle_frequency": freq, "max_cycles": mx}

rows = []
def R(cid, line, rtype, name, drugs, uur="C", udd=5, refs=(), sec="3.3", table=None, stage=None, ecog=None, biom=None, special="", maint=None):
    rows.append({
        "cohort_id": cid,
        "disease": DISEASE,
        "treatment": {"line_stage": line, "therapy_type": rtype, "regimen_name": name},
        "drugs": drugs,
        "indications": {"stage": stage or next(c["stage"] for c in cohorts if c["cohort_id"] == cid),
                        "ecog": ecog or next(c["ecog"] for c in cohorts if c["cohort_id"] == cid),
                        "biomarkers": biom if biom is not None else next(c["biomarkers"] for c in cohorts if c["cohort_id"] == cid)},
        "evidence": {"uur": uur, "udd": udd},
        "source": {"page": None, "section": sec, "table": table,
                   "references": [str(x) for x in refs],
                   "citation": CITE.get(str(refs[0]))},
        "special_conditions": special,
        "maintenance_therapy": maint,
    })

CITE = {
 "8": "NCCN Clinical Practice Guidelines in Oncology (NCCN Guidelines). Central Nervous System Cancers. 2021",
 "71": "RUSSCO, Рекомендации по поддерживающей и сопроводительной терапии. 2024. URL: https://rosoncoweb.ru/standarts/RUSSCO/2024/2024-1_1-10.pdf",
 "72": "NCCN Clinical Practice Guidelines in Oncology (NCCN Guidelines), Central Nervous System Cancers. 2024. URL: https://www.nccn.org/professionals/physician_gls/pdf/cns.pdf",
 "22": "Stupp R., Hegi M.E., Mason W.P., et al. Effects of radiotherapy with concomitant and adjuvant temozolomide versus radiotherapy alone on survival in glioblastoma in a randomised phase III study: 5-year analysis of the EORTC-NCIC trial. Lancet Oncol 2009;10(5):459–66",
 "25": "Taal W., Oosterkamp H.M., Walenkamp A.M., et al. Single-agent bevacizumab or lomustine versus a combination of bevacizumab plus lomustine in patients with recurrent glioblastoma (BELOB trial). Lancet Oncol 2014;15(9):943–53",
 "76": "Wick A., Felsberg J., Steinbach J.P., et al. Efficacy and tolerability of temozolomide in an alternating weekly regimen in patients with recurrent glioma. J Clin Oncol. 2007;25(22):3357–61",
 "85": "Wick W., Platten M., Weller M. New (alternative) temozolomide regimens for the treatment of glioma. Neuro Oncol. 2009;11(1):69–79",
 "86": "Mrugala M.M., Crew L.K., Fink J.R., Spence A.M. Carboplatin and bevacizumab for recurrent malignant glioma. Oncol Lett. 2012;4(5):1082–1086",
 "80": "Zoto Mustafayev T., Turna M., Bolukbasi Y., et al. Clinical and radiological effects of Bevacizumab for the treatment of radionecrosis after stereotactic brain radiotherapy. BMC Cancer. 2024;24(1):918",
 "26": "Vredenburgh J.J., Desjardins A., Herndon J.E. 2nd, et al. Phase II trial of bevacizumab and irinotecan in recurrent malignant glioma. Clin Cancer Res 2007;13(4):1253–9",
 "88": "Leonardo Rojas et al. Profiling response to carmustine/bevacizumab in recurrent glioblastoma. JCO 2016;34(15_suppl):2059",
 "48": "She L., Su L., Liu C. Bevacizumab combined with re-irradiation in recurrent glioblastoma. Front Oncol. 2022;12:961014",
 "81": "Niyazi M., Harter P.N., Hattingen E., et al. Bevacizumab and radiotherapy for the treatment of glioblastoma. Oncotarget. 2016;7(3):2313–28",
 "28": "Friedman H.S., Prados M.D., Wen P.Y., et al. Bevacizumab alone and in combination with irinotecan in recurrent glioblastoma. J Clin Oncol 2009;27:4733–40",
 "83": "Takei J., Fukasawa N., Tanaka T., et al. Impact of Neoadjuvant Bevacizumab on Neuroradiographic Response... Front Oncol. 2022;12:898614",
 "84": "Balana C., De Las Penas R., Sepulveda J.M., et al. Bevacizumab and temozolomide versus temozolomide alone as neoadjuvant treatment in unresected glioblastoma: the GENOM 009 randomized phase II trial. J Neurooncol. 2016;127(3):569–79",
 "13": "Практические рекомендации по лечению злокачественных опухолей Российского общества клинической онкологии (RUSSCO). М.: 2017",
 "78": "Manuel Diezi, Barry Pizer, Matthew J. Murray. Overview of current European practice for the management of patients with intracranial germ cell tumours. EJC Paediatric Oncology 2024;3:100146",
 "18": "Osorio D.S., Allen J.C. Management of CNS germinoma. CNS Oncol. 2015;4(4):273–9",
 "89": "Cardona A.F., Ruiz-Patino A., Zatarain-Barron Z.L., et al. Systemic management of malignant meningiomas: A comparative survival and molecular marker analysis between Octreotide in combination with Everolimus and Sunitinib. PLoS One. 2019;14(6):e0217340",
}

GL = "первичная ХТ при глиомах (grade 3–4)"
RL = "терапия рецидивов глиом"
# --- Глиомы, впервые выявленные (C1) ---
R("C1", GL, ["химиотерапия"], "PCV",
  [d("Ломустин (CCNU)", "100 мг/м²", "в/в", "1-й день", "каждые 6 недель"),
   d("Винкристин", "1,4 мг/м²", "в/в", "дни 1, 8"),
   d("Прокарбазин", "70 мг/м²", "внутрь", "дни 8–21")],
  refs=(8,71), special="стандартный режим при grade 3")
R("C1", GL, ["химиотерапия"], "PC",
  [d("Ломустин (CCNU)", "70–100 мг/м²", "в/в", "1-й день", "каждые 6 недель"),
   d("Прокарбазин", "60 мг/м²", "внутрь", "дни 1–14")], refs=(8,71))
R("C1", GL, ["химиотерапия"], "Монотерапия ломустином",
  [d("Ломустин (CCNU)", "110 мг/м²", "в/в", "1-й день", "каждые 6 недель")],
  refs=(25,71), special="# off-label")
R("C1", GL, ["химиотерапия"], "Темозоломид 5/23",
  [d("Темозоломид", "150–200 мг/м²", "внутрь", "дни 1–5", "каждые 28 дней")],
  refs=(8,71), special="стандартный режим при grade 3–4")
R("C1", GL, ["химиолучевая терапия"], "Темозоломид в составе ХЛТ",
  [d("Темозоломид", "75 мг/м²", "внутрь", "ежедневно на протяжении всего курса ЛТ (30 фракций по 2 Гр)")],
  refs=(22,71), special="стандартный режим при grade 3–4; далее 6–12 курсами темозоломида 150–200 мг/м² в режиме 5/23 (§3.3.1)")
R("C1", GL, ["химиотерапия"], "Темозоломид + Карбоплатин",
  [d("Темозоломид", "150 мг/м²", "внутрь", "дни 1–5", "каждые 4 недели"),
   d("Карбоплатин", "AUC 3", "в/в", None, "каждые 4 недели")], refs=(8,71,72), special="# off-label")
R("C1", GL, ["химиотерапия"], "Темозоломид + Цисплатин",
  [d("Темозоломид", "150 мг/м²", "внутрь", "дни 1–5"),
   d("Цисплатин", "20 мг/м²", "в/в", "дни 1–5")], refs=(71,72), special="# off-label")
R("C1", GL, ["химиотерапия"], "Темозоломид 7/7",
  [d("Темозоломид", "75–150 мг/м²", "внутрь", "дни курса 1–8 и 15–22", "каждые 28 дней")],
  refs=(76,85), special="# off-label")
R("C1", GL, ["химиотерапия", "таргетная терапия"], "Темозоломид + Бевацизумаб",
  [d("Темозоломид", "150–200 мг/м²", "внутрь", "дни 1–5", "каждые 4 недели"),
   d("Бевацизумаб", "5–10 мг/кг", "в/в", "дни 1, 15", "каждые 4 недели")], refs=(71,72))
R("C1a", GL, ["химиотерапия", "таргетная терапия"], "Темозоломид + Бевацизумаб (неоперабельные глиомы)",
  [d("Темозоломид", "150–200 мг/м²", "внутрь", "дни 1–5", "каждые 4 недели"),
   d("Бевацизумаб", "5–10 мг/кг", "в/в", "дни 1, 15", "каждые 4 недели")],
  refs=(71,83,84), stage="неоперабельные глиомы, диффузные глиомы ствола мозга, распространённые диффузные интрамедуллярные глиомы")
R("C1a", GL, ["таргетная терапия"], "Бевацизумаб (монотерапия)",
  [d("Бевацизумаб", "5–10 мг/кг", "в/в", "дни 1, 15", "каждые 4 недели")],
  refs=(71,83,84), stage="неоперабельные глиомы, диффузные глиомы ствола мозга, распространённые диффузные интрамедуллярные глиомы")
R("C2", RL, ["химиотерапия", "таргетная терапия"], "Бевацизумаб + Карбоплатин",
  [d("Бевацизумаб", "10 мг/кг", "в/в", "каждые 2 недели", "каждые 2 недели"),
   d("Карбоплатин", "AUC 4–6", "в/в", None, "каждые 4 недели")], refs=(86,))
R("C2", RL, ["химиотерапия", "таргетная терапия"], "Бевацизумаб + Этопозид",
  [d("Бевацизумаб", "5 мг/кг", "в/в", "каждые 2 недели", "каждые 2 недели"),
   d("Этопозид", "80 мг/м²", "в/в", "дни 1–5", "каждые 3–4 недели")], refs=(71,72), special="# off-label")
R("C1", "ХЛТ на фоне лучевой терапии при распространённых неоперабельных глиомах", ["химиолучевая терапия", "таргетная терапия"], "Бевацизумаб на фоне ЛТ",
  [d("Бевацизумаб", "5–10 мг/кг", "в/в", "каждые 2 недели", "каждые 2 недели")],
  refs=(80,), stage="распространённые неоперабельные глиомы grade 3–4 или большая остаточная опухоль после удаления глиом grade 3–4 с большим перифокальным отёком",
  special="# off-label; на фоне лучевой терапии (см. раздел 3.2)")
R("C1", GL, ["таргетная терапия"], "Дабрафениб + Траметиниб",
  [d("Дабрафениб", "150 мг 2 раза в день", "внутрь", "ежедневно"),
   d("Траметиниб", "2 мг 1 раз в день", "внутрь", "ежедневно")],
  refs=(71,72), biom=["мутация BRAF"],
  special="# off-label; только при выявленной мутации BRAF; вопрос решается онкологическим консилиумом (при мутации V600 BRAF)")
R("C1", GL, ["таргетная терапия"], "Вемурафениб + Кобиметиниб",
  [d("Вемурафениб", "960 мг 2 раза в день", "внутрь", "ежедневно"),
   d("Кобиметиниб", "60 мг", "внутрь", "дни 1–21", "каждые 28 дней")],
  refs=(71,72), biom=["мутация BRAF"],
  special="# off-label; только при выявленной мутации BRAF; вопрос решается онкологическим консилиумом (при мутации V600 BRAF)")
# --- Рецидивы глиом (C2) ---
R("C2", RL, ["таргетная терапия", "химиотерапия"], "Бевацизумаб + Иринотекан",
  [d("Бевацизумаб", "5–10 мг/кг", "в/в", "дни 1, 15", "каждые 28 дней"),
   d("Иринотекан", "125–200 мг/м²", "в/в", "дни 1, 15", "каждые 28 дней")], refs=(26,71,72))
R("C2", RL, ["таргетная терапия", "химиотерапия"], "Бевацизумаб + Ломустин (90 мг/м²)",
  [d("Бевацизумаб", "5–10 мг/кг", "в/в", "дни 1, 15, 29", "каждые 6 недель"),
   d("Ломустин", "90 мг/м²", "в/в", "1-й день", "каждые 6 недель")], refs=(25,2,71))
R("C2", RL, ["таргетная терапия", "химиотерапия"], "Бевацизумаб + Кармустин",
  [d("Бевацизумаб", "10 мг/кг", "в/в", "дни 1, 15, 29", "каждые 6 недель"),
   d("Кармустин", "80 мг/м²", "в/в капельно", "1-й день", "каждые 6 недель")], refs=(88,))
R("C2", RL, ["таргетная терапия", "химиотерапия"], "Бевацизумаб + Ломустин (40 мг/м²)",
  [d("Бевацизумаб", "5–10 мг/кг", "в/в", "дни 1, 15", "каждые 6 недель"),
   d("Ломустин", "40 мг/м²", "в/в", "дни 1, 8, 15, 22", "каждые 6 недель")], refs=(71,72), special="# off-label")
R("C2", RL, ["таргетная терапия"], "Бевацизумаб (монотерапия при рецидиве)",
  [d("Бевацизумаб", "5–10 мг/кг", "в/в", "дни 1, 15", "каждые 28 дней")], refs=(71,72), special="# off-label")
R("C2", RL, ["химиотерапия", "таргетная терапия"], "Темозоломид + Бевацизумаб (при рецидиве)",
  [d("Темозоломид", "150–200 мг/м²", "внутрь", "дни 1–5", "каждые 4 недели"),
   d("Бевацизумаб", "5–10 мг/кг", "в/в", "дни 1, 15", "каждые 4 недели")], refs=(71,72))
R("C2", "ХЛТ на фоне повторной ЛТ при рецидиве глиом", ["химиолучевая терапия", "таргетная терапия"], "Бевацизумаб на фоне ЛТ (рецидив)",
  [d("Бевацизумаб", "5–10 мг/кг", "в/в", "каждые 2 недели", "каждые 2 недели")],
  refs=(48,71,81), stage="рецидивы глиом grade 3–4 с большим перифокальным отёком",
  special="# off-label; на фоне лучевой терапии (см. раздел 3.2)")
# --- Первичная лимфома ЦНС ---
LM = "первичная лимфома головного мозга"
R("C3", LM, ["химиотерапия", "иммунотерапия"], "Высокодозный метотрексат ± ритуксимаб",
  [d("Метотрексат", "3–8 г/м²", "в/в", "1-й день", "каждые 3 недели"),
   d("Ритуксимаб", "375 мг/м²", "в/в", None, "каждые 3 недели")],
  refs=(8,28,71),
  special="только в стационарных условиях гематологического отделения или отделения химиотерапии; контроль уровня метотрексата в крови после введения; в 1-й линии — возраст ≤65 лет, индекс Карновского >50, сохранностью функций печени и почек")
R("C3", LM, ["химиотерапия", "иммунотерапия"], "Темозоломид + Ритуксимаб",
  [d("Темозоломид", "150 мг/м²", "внутрь", "дни 1–5", "каждые 28 дней"),
   d("Ритуксимаб", "375 мг/м²", "в/в", None, "каждые 3 недели")], refs=(72,))
R("C3", LM, ["химиотерапия"], "Темозоломид (монотерапия)",
  [d("Темозоломид", "150–200 мг/м²", "внутрь", "дни 1–5", "каждые 28 дней")], refs=(72,),
  special="у пациентов пожилого возраста и/или с низким функциональным статусом (ИК ≤60) — опция первой линии с оценкой лечения после 2 курсов")
# --- Герминогенные опухоли ---
GE = "первичные герминативно-клеточные опухоли ЦНС"
R("C4", GE, ["химиотерапия"], "Цисплатин + Этопозид (PE)",
  [d("Цисплатин", "25 мг/м²", "в/в", "дни 1–4", "каждые 21–28 дней"),
   d("Этопозид", "80 мг/м²", "в/в", "дни 1–4", "каждые 21–28 дней")],
  refs=(13,78), biom=["АФП/ХГЧ отрицательные"], special="# off-label; дозы из Приложения Б, рис. 9 (4 цикла); далее ЛТ")
NG = "первичные негерминомные герминативно-клеточные опухоли ЦНС"
R("C5", NG, ["химиотерапия"], "Цисплатин + Этопозид (PE)",
  [d("Цисплатин", "25 мг/м²", "в/в", "дни 1–4", "каждые 21 день"),
   d("Этопозид", "80 мг/м²", "в/в", "дни 1–4", "каждые 21 день")], refs=(13,18,78), special="# off-label")
R("C5", NG, ["химиотерапия"], "PEI (цисплатин + этопозид + ифосфамид)",
  [d("Цисплатин", "20 мг/м²", "в/в", "дни 1–5", "каждые 3–4 недели"),
   d("Этопозид", "80 мг/м²", "в/в", "дни 1–5", "каждые 3–4 недели"),
   d("Ифосфамид (+ месна)", "1500 мг/м²", "в/в", "1-й, 3-й, 5-й дни", "каждые 3–4 недели")],
  refs=(13,18,78), special="# off-label")
R("C5", NG, ["химиотерапия"], "Цисплатин + Этопозид + Циклофосфамид",
  [d("Цисплатин", "20 мг/м²", "в/в", "дни 1–4", "каждые 4–6 недель"),
   d("Этопозид", "80 мг/м²", "в/в", "дни 1–4", "каждые 4–6 недель"),
   d("Циклофосфамид", "600 мг/м²", "в/в", "4-й день", "каждые 4–6 недель", 6)],
  refs=(13,18,78), special="# off-label")
MB = "медуллобластома, пинеобластома, пинеоцитома с промежуточной дифференцировкой"
R("C6", MB, ["химиотерапия"], "Цисплатин + Этопозид + Циклофосфамид",
  [d("Цисплатин", "25 мг/м²", "в/в", "дни 1–4", "каждые 4–6 недель"),
   d("Этопозид", "80 мг/м²", "в/в", "дни 1–4", "каждые 4–6 недель"),
   d("Циклофосфамид", "600 мг/м²", "в/в", "4-й день", "каждые 4–6 недель", 6)], refs=(8,71),
  special="адъювантно после ЛТ (КСО 35 Гр + буст до 55 Гр, Приложение Б, рис. 11)")
ME = "рецидив анапластической менингиомы / агрессивное течение иных морфологических типов менингиом"
R("C7", ME, ["таргетная терапия"], "Бевацизумаб + Сунитиниб",
  [d("Бевацизумаб", "5 мг/кг", "в/в"),
   d("Сунитиниб", "50 мг", "внутрь", "1–4 неделя, затем 2 недели перерыв", "каждые 6 недель")],
  refs=(71,), special="# off-label; опция")
R("C7", ME, ["таргетная терапия"], "Октреотид + Эверолимус",
  [d("Октреотид", "30 мг", "внутримышечно", None, "каждые 28 дней"),
   d("Эверолимус", "10 мг/сут", "внутрь", "ежедневно")], uur="C", udd=4, refs=(71,89),
  special="# off-label")
RN = "постлучевые реакции и лучевой некроз"
R("C8", RN, ["таргетная терапия"], "Бевацизумаб",
  [d("Бевацизумаб", "7,5 мг/кг", "в/в", None, "каждые 3 недели")], uur="C", udd=4, refs=(80,),
  special="# off-label")

rows = [r for r in rows if r]

with open(f"output-cohort/{DOC}.cohorts.json", "w") as f:
    json.dump(cohorts, f, ensure_ascii=False, indent=1)
with open(f"output-cohort/{DOC}.regimens.json", "w") as f:
    json.dump(rows, f, ensure_ascii=False, indent=1)

for c in cohorts:
    audit.cohort(DOC, c)
for r in rows:
    audit.regimen(DOC, r)
audit.event(DOC, "phase2-done", f"{len(rows)} regimens, {len(cohorts)} cohorts")
print(f"{DOC}: {len(cohorts)} cohorts, {len(rows)} regimens written")
