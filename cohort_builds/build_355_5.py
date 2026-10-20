# -*- coding: utf-8 -*-
"""Build cohorts + medication regimens for doc 355_5 (рак поджелудочной железы, C25)."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit  # noqa: E402

DOC = "355_5"

DISEASE = {
    "name": "Злокачественное новообразование поджелудочной железы (рак поджелудочной железы, РПЖ)",
    "icd10": "C25 (C25.0–C25.9)",
    "histology_type": "протоковая аденокарцинома (~85–95% экзокринных новообразований ПЖ) и её редкие микроскопические варианты",
}

def drug(inn, dose, route, schedule, cycle_frequency=None, max_cycles=None):
    return {"inn": inn, "dose": dose, "route": route, "schedule": schedule,
            "cycle_frequency": cycle_frequency, "max_cycles": max_cycles}

def base(cid, line, ttype, name, drugs, stage, ecog=None, bio=None, uur=None, udd=None,
         section="3.2", refs=None, cite=None, special="", maint=None):
    return {
        "cohort_id": cid, "disease": DISEASE,
        "treatment": {"line_stage": line, "therapy_type": ttype, "regimen_name": name},
        "drugs": drugs,
        "indications": {"stage": stage, "ecog": ecog, "biomarkers": bio or []},
        "evidence": {"uur": uur, "udd": udd},
        "source": {"page": None, "section": section, "table": None,
                   "references": refs or [], "citation": cite},
        "special_conditions": special,
        "maintenance_therapy": maint,
    }

JNVLP = "** ЖНВЛП; "

cohorts = [
    {"cohort_id": "C1", "disease": DISEASE,
     "stage": "погранично резектабельный РПЖ (T3–4 N0–1 M0)",
     "resectability": "погранично резектабельный",
     "clinical_situation": "первичный процесс, предоперационная терапия",
     "ecog": None,
     "biomarkers": ["BRCA/PALB2 (влияет на выбор режима: FOLFIRINOX или гемцитабин + соединения платины)"],
     "treatment_stages": ["предоперационная ХТ 12–18 недель с последующей оценкой и операцией при отсутствии отрицательной динамики"],
     "source": {"section": "3.2.1"}},
    {"cohort_id": "C2", "disease": DISEASE,
     "stage": "нерезектабельный РПЖ (T3–4 N0–1 M0), без отдалённых метастазов",
     "resectability": "нерезектабельный",
     "clinical_situation": "индукционная терапия с повторной оценкой резектабельности",
     "ecog": None,
     "biomarkers": ["BRCA/PALB2 (выбор режима как при погранично резектабельном)"],
     "treatment_stages": ["индукционная ХТ 12–24 недели; далее продолжение режима либо поддерживающая ХТ; суммарно ≥6 мес (возможно до прогрессирования)"],
     "source": {"section": "3.2.1"}},
    {"cohort_id": "C3", "disease": DISEASE,
     "stage": "I–III стадии (T1–3 N0–1 M0) после удаления карциномы ПЖ",
     "resectability": "радикально оперированный",
     "clinical_situation": "адъювантная терапия",
     "ecog": None,
     "biomarkers": [],
     "treatment_stages": ["адъювантная ХТ в течение 3 мес после операции (оптимально 4–8 нед); длительность 6 мес, если не было предоперационной ХТ"],
     "source": {"section": "3.2.1"}},
    {"cohort_id": "C4", "disease": DISEASE,
     "stage": "метастатический РПЖ (IV стадия)",
     "resectability": None,
     "clinical_situation": "1-я линия системной терапии",
     "ecog": "ECOG 0–1 для FOLFIRINOX; ECOG 0–2 для комбинаций; ECOG 2 для монотерапий",
     "biomarkers": ["патогенная герминальная или биаллельная соматическая мутация BRCA/PALB2 (для платиносодержащих комбинаций)", "герминальная мутация BRCA (для олапариба)"],
     "treatment_stages": ["системная ХТ до прогрессирования по RECIST 1.1 или неприемлемой токсичности; поддерживающая терапия олапарибом/фторпиримидинами"],
     "source": {"section": "3.2.2"}},
    {"cohort_id": "C5", "disease": DISEASE,
     "stage": "прогрессирование после адъювантной ХТ и/или ХТ 1-й линии",
     "resectability": None,
     "clinical_situation": "2-я линия системной терапии",
     "ecog": "ECOG 0–1 (комбинации); ECOG 0–2 (гемцитабин+платина, пембролизумаб); ECOG 1–2 (гемцитабин); ECOG 2 (фторпиримидины)",
     "biomarkers": ["герминальная или соматическая мутация BRCA/PALB2 (для платиносодержащих комбинаций 2L)", "MSI/dMMR (для пембролизумаба)"],
     "treatment_stages": ["ХТ 2-й линии до прогрессирования/неприемлемой токсичности; при прогрессировании >6 мес после предыдущей ХТ возможно возобновление той же схемы"],
     "source": {"section": "3.2.2"}},
    {"cohort_id": "C6", "disease": DISEASE,
     "stage": "изолированный локорегионарный рецидив после хирургического лечения либо продолженный рост первичной нерезектабельной опухоли после ХТ, без отдалённых метастазов",
     "resectability": "нерезектабельный/нерецидивируемый резектабельно",
     "clinical_situation": "местный рецидив/прогрессирование",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["хирургия (ререзекция), либо химиолучевая терапия, либо ХТ 3–4 мес + стереотаксическая ЛТ"],
     "source": {"section": "3.2.2"}},
]

R = []
# ---------- C1: предоперационная ХТ погранично резектабельного РПЖ ----------
pre_stage = "погранично резектабельный РПЖ (T3–4 N0–1 M0)"
pre_cond = JNVLP + "# off-label у компонентов; длительность предоперационной ХТ 12–18 недель"
R += [
    base("C1", "предоперационная (неоадъювантная) химиотерапия", ["химиотерапия"], "mFOLFIRINOX",
         [drug("Оксалиплатин", "85 мг/м²", "в/в", "120 мин"), drug("Иринотекан", "150 мг/м²", "в/в", "90 мин"),
          drug("Кальция фолинат", "400 мг/м²", "в/в", "120 мин"),
          drug("Фторурацил", "2400 мг/м²", "в/в", "инфузия в течение 46 часов", "каждые 2 недели", 12)],
         pre_stage, bio=["BRCA/PALB2: предпочтителен при наличии мутаций"],
         uur="C", udd=5, refs=["64"],
         cite="Базин И., Покатаев И. Место химиотерапии в лечении локализованного рака поджелудочной железы // Злокачественные опухоли. 2016. Vol. 21, № 4 (спецвыпуск 1). P. 20–25",
         special=pre_cond),
    base("C1", "предоперационная (неоадъювантная) химиотерапия", ["химиотерапия"], "Гемцитабин + паклитаксел + альбумин",
         [drug("Паклитаксел + альбумин", None, "в/в", None, None, None), drug("Гемцитабин", None, "в/в", None, None, None)],
         pre_stage, uur="C", udd=5, refs=["64"],
         cite="Базин И., Покатаев И. Место химиотерапии в лечении локализованного рака поджелудочной железы // Злокачественные опухоли. 2016. Vol. 21, № 4 (спецвыпуск 1). P. 20–25",
         special=JNVLP + "# off-label; дозы не приведены в разделе о предоперационной ХТ (см. режимы метастатического РПЖ, таблица 4)"),
]
R.append(base("C1", "предоперационная (неоадъювантная) химиотерапия", ["химиотерапия"], "Гемцитабин + соединения платины",
              [drug("Гемцитабин", None, "в/в", None, None, None), drug("Соединения платины (цисплатин/оксалиплатин)", None, "в/в", None, None, None)],
              pre_stage, bio=["мутации в генах BRCA или PALB2"],
              uur="C", udd=5, refs=["64"],
              cite="Базин И., Покатаев И. Место химиотерапии в лечении локализованного рака поджелудочной железы // Злокачественные опухоли. 2016. Vol. 21, № 4 (спецвыпуск 1). P. 20–25",
              special=JNVLP + "# off-label; оптимальный вариант при мутациях BRCA/PALB2; конкретные дозы в разделе не приведены"))

# ---------- C2: индукционная ХТ нерезектабельного РПЖ ----------
ind_cite = ("Базин И., Покатаев И. Место химиотерапии в лечении локализованного рака поджелудочной железы. 2016. "
            "Vol. 21, № 4(спецвыпуск 1). P. 20–25; Massucco P. et al. Ann Surg Oncol 2006; Kunzmann V. et al. NEOLAP Ann Oncol 2019; Rombouts S.J. et al. Ann Surg Oncol 2016")
ind_refs = ["64", "66-68"]
R += [
    base("C2", "индукционная терапия (местнораспространённый процесс)", ["химиотерапия"], "FOLFIRINOX",
         [drug("Оксалиплатин", "85 мг/м²", "в/в", "120 мин"), drug("Иринотекан", "180 мг/м²", "в/в", "90 мин"),
          drug("Кальция фолинат", "400 мг/м²", "в/в", "120 мин"),
          drug("Фторурацил", "400 мг/м² болюс + 2400 мг/м² инфузия 46 ч", "в/в", "болюс затем инфузия в течение 46 часов", "каждые 2 недели", "до прогрессирования/неприемлемой токсичности")],
         "нерезектабельный РПЖ (T3–4 N0–1 M0)", bio=["BRCA/PALB2: предпочтителен при наличии мутаций"],
         uur="C", udd=4, refs=ind_refs, cite=ind_cite,
         special=JNVLP + "# off-label; длительность индукции 12–24 недели; суммарно с поддерживающим этапом ≥6 мес (возможно до прогрессирования)"),
    base("C2", "индукционная терапия (местнораспространённый процесс)", ["химиотерапия"], "Гемцитабин + паклитаксел + альбумин",
         [drug("Паклитаксел + альбумин", "125 мг/м²", "в/в", "капельно 30 минут, 1, 8, 15 дни 28-дневного цикла", "28-дневный цикл", "до прогрессирования/неприемлемой токсичности"),
          drug("Гемцитабин", "1000 мг/м²", "в/в", "капельно 30 минут, 1, 8, 15 дни 28-дневного цикла", "28-дневный цикл", "до прогрессирования/неприемлемой токсичности")],
         "нерезектабельный РПЖ (T3–4 N0–1 M0)",
         uur="C", udd=4, refs=ind_refs, cite=ind_cite,
         special=JNVLP + "# off-label; дозировка приведена по аналогии с таблицей 4 (метастатический РПЖ)"),
    base("C2", "поддерживающая химиотерапия после индукции", ["химиотерапия"], "Фторурацил/капецитабин монотерапия (поддерживающая)",
         [drug("Фторурацил", None, "в/в", None, None, None), drug("Капецитабин", None, "внутрь", None, None, None)],
         "нерезектабельный РПЖ (T3–4 N0–1 M0)", uur="C", udd=4, refs=ind_refs, cite=ind_cite,
         special="# off-label; например, монотерапия фторурацилом/капецитабином, если пациент получал FOLFIRINOX; суммарная ХТ ≥6 мес, возможно до прогрессирования; доказательств преимущества перед продолжением режима нет",
         maint="Продолжение начатого режима либо монотерапия фторурацилом/капецитабином; общая длительность ХТ не менее 6 месяцев"),
]

# ---------- C3: адъювантная ХТ ----------
adj_stage = "I–III стадии (T1–3 N0–1 M0) после радикальной операции"
adj_note = JNVLP + "# off-label у компонентов; начало в течение 3 мес после операции (оптимально 4–8 нед)"
R += [
    base("C3", "адъювантная химиотерапия", ["химиотерапия"], "mFOLFIRINOX",
         [drug("Оксалиплатин", "85 мг/м²", "в/в", "120 мин"), drug("Иринотекан", "150 мг/м²", "в/в", "90 мин"),
          drug("Кальция фолинат", "400 мг/м²", "в/в", "120 мин"),
          drug("Фторурацил", "2400 мг/м²", "в/в", "инфузия в течение 46 часов", "каждые 2 недели", 12)],
         adj_stage, ecog="ECOG 0–1, без серьёзных осложнений хирургического лечения и сопутствующих заболеваний",
         uur="A", udd=1, refs=["72", "74-76"], cite="Conroy T. et al. FOLFIRINOX or Gemcitabine as Adjuvant Therapy for Pancreatic Cancer // New England Journal of Medicine. 2018. Vol. 379, № 25. P. 2395–2406",
         special=adj_note + "; наиболее предпочтительный режим; возможна редукция доз (минимальные: иринотекан 120 мг/м², оксалиплатин 60 мг/м², фторурацил 1800 мг/м²); профилактика нейтропении филграстимом 5 мкг/кг п/к или пэгфилграстимом 6 мг п/к однократно, эмпэгфилграстимом 7,5 мг п/к"),
    base("C3", "адъювантная химиотерапия", ["химиотерапия"], "GEMCAP",
         [drug("Гемцитабин", "1000 мг/м²", "в/в", "капельно 30 мин, 1-й, 8-й и 15-й дни", "каждые 4 недели", 6),
          drug("Капецитабин", "1660 мг/м²", "внутрь", "ежедневно с 1-го по 21-й день", "каждые 4 недели", 6)],
         adj_stage, uur="A", udd=1, refs=["72", "74-76"], cite="Neoptolemos J.P. et al. Comparison of adjuvant gemcitabine and capecitabine with gemcitabine monotherapy in patients with resected pancreatic cancer (ESPAC-4): a multicentre, open-label, randomised, phase 3 trial // The Lancet. 2017. Vol. 389, № 10073. P. 1011–1024",
         special=adj_note + "; предпочтительный режим при невозможности mFOLFIRINOX; польза сомнительна при R1-статусе",
         ),
    base("C3", "адъювантная химиотерапия", ["химиотерапия"], "Гемцитабин монотерапия (минимальный объем)",
         [drug("Гемцитабин", "1000 мг/м²", "в/в", "капельно 30 мин, 1-й, 8-й и 15-й дни", "каждые 4 недели", 6)],
         adj_stage, uur="A", udd=1, refs=["78"], cite="Oettle H. et al. Adjuvant Chemotherapy With Gemcitabine vs Observation in Patients Undergoing Curative-Intent Resection of Pancreatic Cancer // JAMA. 2007. Vol. 297, № 3. P. 267–277",
         special=adj_note),
    base("C3", "адъювантная химиотерапия", ["химиотерапия"], "Капецитабин монотерапия (минимальный объем)",
         [drug("Капецитабин", "2000–2500 мг/м²/сут", "внутрь", "с 1-го по 14-й день", "каждые 3 недели", 8)],
         adj_stage, uur="A", udd=1, refs=["79", "80"], cite="Neoptolemos J.P. et al. A Randomized Trial of Chemoradiotherapy and Chemotherapy after Resection of Pancreatic Cancer // N Engl J Med. 2004. Vol. 350, № 12. P. 1200–1210",
         special=adj_note),
    base("C3", "адъювантная химиотерапия", ["химиотерапия"], "Фторурацил + кальция фолинат (минимальный объем)",
         [drug("Фторурацил", "425 мг/м²", "в/в", "болюс, с 1-го по 5-й дни", "каждые 4 недели", 6),
          drug("Кальция фолинат", "20 мг/м²", "в/в", "болюс, с 1-го по 5-й дни", "каждые 4 недели", 6)],
         adj_stage, uur="A", udd=1, refs=["79"], cite="Neoptolemos J.P. et al. A Randomized Trial of Chemoradiotherapy and Chemotherapy after Resection of Pancreatic Cancer // N Engl J Med. 2004. Vol. 350, № 12. P. 1200–1210",
         special=adj_note + "; при дефектуре фолината кальция возможна его замена на фиксированную дозу 50 мг/сут или исключение"),
]
# fix table field on adjuvant rows
for r in R[-5:]:
    r["source"]["table"] = "Таблица 3. Режимы адъювантной химиотерапии при раке поджелудочной железы"

# ---------- C4: 1L метастатический ----------
m_stage = "метастатический РПЖ (IV стадия)"
tbl4 = "Таблица 4. Химиотерапия I линии рака поджелудочной железы"
met_until = "до прогрессирования по RECIST 1.1 или неприемлемой токсичности"
R += [
    base("C4", "1-я линия (метастатический процесс)", ["химиотерапия"], "FOLFIRINOX",
         [drug("Оксалиплатин", "85 мг/м²", "в/в", "120 мин"), drug("Иринотекан", "180 мг/м²", "в/в", "90 мин"),
          drug("Кальция фолинат", "400 мг/м²", "в/в", "120 мин"),
          drug("Фторурацил", "400 мг/м² болюс + 2400 мг/м² инфузия 46 ч", "в/в", "болюс затем инфузия в течение 46 часов", "интервал между циклами 14 дней", met_until)],
         m_stage, ecog="ECOG 0–1; билирубин <1,5×ВГН", uur="B", udd=1, refs=["86"],
         cite="Conroy T. et al. FOLFIRINOX versus Gemcitabine for Metastatic Pancreatic Cancer // N Engl J Med. 2011. Vol. 364, № 19. P. 1817–1825",
         special=JNVLP + "# off-label у компонентов; требования: отсутствие серьёзных осложнений/сопутствующих заболеваний, центральный венозный доступ, инфузомат; возможна модификация (редукция фторурацила до 320/2000 мг/м², иринотекана до 150 мг/м², оксалиплатина до 65 мг/м², первичная профилактика КСФ); после 8 курсов возможен переход на поддерживающую терапию фторурацилом/капецитабином или FOLFIRI до прогрессирования",
         maint="После 8 курсов FOLFIRINOX возможна поддерживающая терапия фторурацилом/капецитабином или режим FOLFIRI до прогрессирования"),
    base("C4", "1-я линия (метастатический процесс)", ["химиотерапия"], "Гемцитабин + паклитаксел + альбумин",
         [drug("Паклитаксел + альбумин", "125 мг/м²", "в/в", "капельно 30 минут, 1, 8, 15 дни 28-дневного цикла", "28-дневный цикл", met_until),
          drug("Гемцитабин", "1000 мг/м²", "в/в", "капельно 30 минут, 1, 8, 15 дни 28-дневного цикла", "28-дневный цикл", met_until)],
         m_stage, ecog="ECOG 0–2; билирубин <1,5×ВГН", uur="B", udd=1, refs=["85"],
         cite="Von Hoff D.D. et al. Increased Survival in Pancreatic Cancer with nab-Paclitaxel plus Gemcitabine // N Engl J Med. 2013. Vol. 369, № 18. P. 1691–1703",
         special=JNVLP + "# off-label у компонентов"),
    base("C4", "1-я линия (метастатический процесс)", ["химиотерапия"], "Гемцитабин + цисплатин",
         [drug("Гемцитабин", "1000 мг/м²", "в/в", "капельно, 1, 8 дни 21-дневного курса", "21-дневный курс", met_until),
          drug("Цисплатин", "50–75 мг/м²", "в/в", "капельно, 1-й день 21-дневного курса", "21-дневный курс", met_until)],
         m_stage, ecog="ECOG 0–2; билирубин <1,5×ВГН",
         bio=["патогенная герминальная или биаллельная соматическая мутация BRCA или PALB2"],
         uur="B", udd=1, refs=["87"],
         cite="Inal A. et al. Gemcitabine Alone versus combination of Gemcitabine and Cisplatin for the Treatment of Patients with Locally Advanced and/or Metastatic Pancreatic Carcinoma // neo. 2012. Vol. 59, № 03. P. 297–301",
         special=JNVLP + "# off-label у компонентов; препараты платины к гемцитабину не добавляются при отсутствии мутаций BRCA/PALB2"),
    base("C4", "1-я линия (метастатический процесс)", ["химиотерапия"], "Гемцитабин + оксалиплатин (GEMOX)",
         [drug("Гемцитабин", "1000 мг/м²", "в/в", "капельно", None, met_until),
          drug("Оксалиплатин", "100 мг/м²", "в/в", "капельно 120 минут", "каждые 2 недели", met_until)],
         m_stage, ecog="ECOG 0–2; билирубин <1,5×ВГН",
         bio=["патогенная герминальная или биаллельная соматическая мутация BRCA или PALB2"],
         uur="B", udd=1, refs=["88"],
         cite="Louvet C. et al. Gemcitabine in Combination With Oxaliplatin Compared With Gemcitabine Alone in Locally Advanced or Metastatic Pancreatic Cancer: Results of a GERCOR and GISCAD Phase III Trial // JCO. 2005. Vol. 23, № 15. P. 3509–3516",
         special=JNVLP + "# off-label у компонентов; только при мутациях BRCA/PALB2"),
    base("C4", "1-я линия (метастатический процесс)", ["химиотерапия"], "Гемцитабин монотерапия",
         [drug("Гемцитабин", "1000 мг/м²", "в/в", "капельно 30 минут 1 раз в неделю в течение 7 недель с последующим недельным перерывом, далее 1, 8, 15 дни 28-дневного курса", "28-дневный курс", met_until)],
         m_stage, ecog="ECOG 2; билирубин <3×ВГН", uur="B", udd=1, refs=["83"],
         cite="Burris H.A. et al. Improvements in survival and clinical benefit with gemcitabine as first-line therapy for patients with advanced pancreas cancer: a randomized trial // JCO. 1997. Vol. 15, № 6. P. 2403–2413",
         special=JNVLP + "# off-label; при противопоказаниях к вышеперечисленным режимам"),
    base("C4", "1-я линия (метастатический процесс)", ["химиотерапия"], "Капецитабин монотерапия",
         [drug("Капецитабин", "2000–2500 мг/м²", "внутрь", "в 1–14-й дни 21-дневного курса", "21-дневный курс", met_until)],
         m_stage, ecog="ECOG 2 балла; билирубин <3×ВГН", uur="B", udd=1, refs=["80", "89", "90"],
         cite="Cartwright T.H. et al. Phase II Study of Oral Capecitabine in Patients With Advanced or Metastatic Pancreatic Cancer // JCO. 2002. Vol. 20, № 1. P. 160–164",
         special=JNVLP + "# off-label; при противопоказаниях к вышеперечисленным режимам, включая монотерапию гемцитабином"),
    base("C4", "поддерживающая терапия 1-й линии (после ≥16 недель платиносодержащей ХТ)", ["таргетная терапия"], "Олапариб (поддерживающая терапия)",
         [drug("Олапариб", "300 мг 2 раза в сутки", "внутрь", "ежедневно", "ежедневно", met_until)],
         m_stage, ecog="ECOG 0–2; билирубин <1,5×ВГН",
         bio=["патогенная герминальная мутация BRCA", "отсутствие прогрессирования после ≥16 недель платиносодержащей ХТ 1-й линии"],
         uur="C", udd=2, refs=["91"],
         cite="Golan T. et al. Maintenance Olaparib for Germline BRCA-Mutated Metastatic Pancreatic Cancer // N Engl J Med. 2019. Vol. 381, № 4. P. 317–327",
         special="** ЖНВЛП; начать не позже 8 недель от даты последнего курса ХТ; допустим более поздний переход, в т.ч. на фоне эффекта при поддерживающей ХТ фторпиримидинами/FOLFIRI; как самостоятельное лечение (не поддерживающее) не рекомендуется; увеличения ОЖ vs плацебо не продемонстрировано",
         maint="Поддерживающая терапия олапарибом 300 мг 2 раза в сутки внутрь до прогрессирования заболевания или непереносимой токсичности"),
]
ol = R[-1]
for r in R[-7:]:
    r["source"]["table"] = tbl4

# ---------- C5: 2L ----------
s_stage = "прогрессирование после адъювантной ХТ и/или ХТ 1-й линии (удовлетворительное состояние)"
tbl5 = "Таблица 5. Химиотерапия II линии рака поджелудочной железы"
gem_nabp2l = dict(refs=["100"], cite="Mita N. et al. Second-Line Gemcitabine Plus Nab-Paclitaxel for Patients with Unresectable Advanced Pancreatic Cancer after First-Line FOLFIRINOX Failure // JCM. 2019. Vol. 8, № 6. P. 761")
plat2l_refs = ["101"]; plat2l_cite = "Heinemann V. et al. Gemcitabine and cisplatin in the treatment of advanced or metastatic pancreatic cancer // Annals of Oncology. 2000. Vol. 11, № 11. P. 1399–1403"
gox2l_refs = ["102", "103"]; gox2l_cite = "Demols A. et al. Gemcitabine and oxaliplatin (GEMOX) in gemcitabine refractory advanced pancreatic adenocarcinoma: a phase II study // Br J Cancer. 2006. Vol. 94, № 4. P. 481–485"
R += [
    base("C5", "2-я линия", ["химиотерапия"], "Гемцитабин + паклитаксел + альбумин",
         [drug("Паклитаксел + альбумин", "100–125 мг/м²", "в/в", "капельно 30 минут, 1, 8, 15 дни 28-дневного цикла", "28-дневный цикл", met_until),
          drug("Гемцитабин", "750–1000 мг/м²", "в/в", "капельно 30 минут, 1, 8, 15 дни 28-дневного цикла", "28-дневный цикл", met_until)],
         s_stage, ecog="ECOG 0–1; билирубин <1,5×ВГН; ранее не использовались гемцитабин и паклитаксел+альбумин",
         uur="B", udd=3, **gem_nabp2l),
    base("C5", "2-я линия", ["химиотерапия"], "Гемцитабин + цисплатин",
         [drug("Гемцитабин", "1000 мг/м²", "в/в", "капельно, 1, 8, 15 дни 28-дневного курса", "28-дневный курс", met_until),
          drug("Цисплатин", "50 мг/м²", "в/в", "капельно, 1, 15 дни 28-дневного курса", "28-дневный курс", met_until)],
         s_stage, ecog="ECOG 0–2; билирубин <1,5×ВГН; ранее не использовались гемцитабин и соединения платины",
         bio=["герминальная или соматическая мутация BRCA или PALB2"],
         uur="B", udd=3, refs=plat2l_refs, cite=plat2l_cite),
    base("C5", "2-я линия", ["химиотерапия"], "Гемцитабин + оксалиплатин (GEMOX)",
         [drug("Гемцитабин", "1000 мг/м²", "в/в", "капельно", None, met_until),
          drug("Оксалиплатин", "85–100 мг/м²", "в/в", "капельно", "каждые 2 недели", met_until)],
         s_stage, ecog="ECOG 0–2; билирубин <1,5×ВГН; ранее не использовались гемцитабин и соединения платины",
         bio=["герминальная или соматическая мутация BRCA или PALB2"],
         uur="B", udd=3, refs=gox2l_refs, cite=gox2l_cite),
    base("C5", "2-я линия", ["химиотерапия"], "Гемцитабин монотерапия",
         [drug("Гемцитабин", "1000 мг/м² (возможна редукция до 750 мг/м²)", "в/в", "капельно 30 минут, 1, 8, 15 дни 28-дневного курса", "28-дневный курс", met_until)],
         s_stage, ecog="ECOG 1–2; билирубин <3×ВГН; ранее не использовался гемцитабин",
         uur="B", udd=3, refs=["104", "105"],
         cite="Viaud J. et al. Gemcitabine as second-line chemotherapy after Folfirinox failure in advanced pancreatic adenocarcinoma: A retrospective study // Digestive and Liver Disease. 2017. Vol. 49, № 6. P. 692–696"),
    base("C5", "2-я линия", ["химиотерапия"], "mFOLFIRINOX",
         [drug("Оксалиплатин", "60–85 мг/м²", "в/в", "120 мин"), drug("Иринотекан", "120–180 мг/м²", "в/в", "90 мин"),
          drug("Кальция фолинат", "400 мг/м²", "в/в", "120 мин"),
          drug("Фторурацил", "2000–2400 мг/м²", "в/в", "инфузия в течение 46 часов", "интервал между циклами 14 дней", met_until)],
         s_stage, ecog="ECOG 0–1; билирубин <1,5×ВГН; ранее использовался гемцитабин",
         uur="B", udd=3, refs=["106", "107"],
         cite="Chung M.J. et al. Multicenter phase II trial of modified FOLFIRINOX in gemcitabine-refractory pancreatic cancer // WJGO. 2018. Vol. 10, № 12. P. 505–515"),
    base("C5", "2-я линия", ["химиотерапия"], "FOLFOX",
         [drug("Оксалиплатин", "85 мг/м²", "в/в", "120 мин"), drug("Кальция фолинат", "400 мг/м²", "в/в", "120 мин"),
          drug("Фторурацил", "400 мг/м² болюс + 2400 мг/м² инфузия 46 ч", "в/в", "болюс затем инфузия в течение 46 часов", "интервал между циклами 14 дней", met_until)],
         s_stage, ecog="ECOG 0–1; билирубин <1,5×ВГН; ранее использовался гемцитабин",
         uur="B", udd=3, refs=["108"],
         cite="Zaanan A. et al. FOLFOX as second-line chemotherapy in patients with pretreated metastatic pancreatic cancer from the FIRGEM study // BMC cancer. 2014. Vol. 14. P. 441"),
    base("C5", "2-я линия", ["химиотерапия"], "XELOX",
         [drug("Оксалиплатин", "130 мг/м²", "в/в", "120 мин, день 1", "21-дневный цикл", met_until),
          drug("Капецитабин", "2000 мг/м² в сутки", "внутрь", "1–14 дни 21-дневного цикла", "21-дневный цикл", met_until)],
         s_stage, ecog="ECOG 0–1; билирубин <1,5×ВГН; ранее использовался гемцитабин",
         uur="B", udd=3, refs=["109"],
         cite="Berk V. et al. XELOX versus FOLFOX4 as Second Line Chemotherapy in Advanced Pancreatic Cancer // HGE. 2012"),
    base("C5", "2-я линия", ["химиотерапия"], "FOLFIRI.3",
         [drug("Иринотекан", "70–90 мг/м²", "в/в", "60 мин в день 1; повторно 70–90 мг/м² 60 мин в день 3 после окончания инфузии фторурацила", "интервал между циклами 14 дней", met_until),
          drug("Кальция фолинат", "400 мг/м²", "в/в", "120 мин в день 1", "интервал между циклами 14 дней", met_until),
          drug("Фторурацил", "2000 мг/м²", "в/в", "инфузия в течение 46 часов", "интервал между циклами 14 дней", met_until)],
         s_stage, ecog="ECOG 0–1; билирубин <1,5×ВГН; ранее использовался гемцитабин",
         uur="B", udd=3, refs=["110", "111"],
         cite="Yoo C. et al. A randomised phase II study of modified FOLFIRI.3 vs modified FOLFOX as second-line therapy in patients with gemcitabine-refractory advanced pancreatic cancer // Br J Cancer. 2009. Vol. 101, № 10. P. 1658–1663"),
    base("C5", "2-я линия", ["химиотерапия"], "CAPIRI",
         [drug("Иринотекан", "200 мг/м²", "в/в", "90 мин в день 1", "21-дневный цикл", met_until),
          drug("Капецитабин", "1600–2000 мг/м²", "внутрь", "1–14 дни 21-дневного цикла", "21-дневный цикл", met_until)],
         s_stage, ecog="ECOG 0–1; билирубин <1,5×ВГН; ранее использовался гемцитабин",
         uur="B", udd=3, refs=["112"],
         cite="Cereda S. et al. XELIRI or FOLFIRI as Salvage Therapy in Advanced Pancreatic Cancer // Anticancer Research. 2010. Vol. 30, № 11. P. 4785–4790"),
    base("C5", "2-я линия", ["химиотерапия"], "OFF",
         [drug("Оксалиплатин", "85 мг/м²", "в/в", "120 мин, в 8, 22 дни", "43-дневный цикл", met_until),
          drug("Кальция фолинат", "200 мг/м²", "в/в", "30 мин, в 1, 8, 15, 22 дни", "43-дневный цикл", met_until),
          drug("Фторурацил", "2000 мг/м²", "в/в", "инфузия в течение 24 часов, в 1, 8, 15, 22 дни", "43-дневный цикл", met_until)],
         s_stage, ecog="ECOG 0–1; билирубин <1,5×ВГН; ранее использовался гемцитабин",
         uur="B", udd=3, refs=["113"],
         cite="Pelzer U. et al. Best supportive care (BSC) versus oxaliplatin, folinic acid and 5-fluorouracil (OFF) plus BSC in patients for second-line advanced pancreatic cancer: A phase III-study from the German CONKO-study group // European Journal of Cancer. 2011. Vol. 47, № 11. P. 1676–1681"),
    base("C5", "2-я линия", ["иммунотерапия"], "Пембролизумаб монотерапия",
         [drug("Пембролизумаб", "200 мг", "в/в", "30 мин, 1 раз в 3 недели", "каждые 3 недели", met_until)],
         s_stage, ecog="ECOG 0–2",
         bio=["микросателлитная нестабильность в опухоли (MSI) или дефицит системы репарации неспаренных оснований (dMMR)"],
         uur="B", udd=3, refs=["45", "114"],
         cite="Le D.T. et al. Mismatch repair deficiency predicts response of solid tumors to PD-1 blockade // Science. 2017. Vol. 357, № 6349. P. 409–413",
         special="** ЖНВЛП; только при MSI/dMMR"),
    base("C5", "2-я линия", ["химиотерапия"], "Капецитабин монотерапия",
         [drug("Капецитабин", "2500 мг/м² (возможна редукция до 2000 мг/м²) в сутки", "внутрь", "1–14 дни 21-дневного цикла", "21-дневный цикл", met_until)],
         s_stage, ecog="ECOG 2; билирубин <3×ВГН; ранее использовался гемцитабин",
         uur="B", udd=3, refs=["119", "120"],
         cite="Park S.J., Lee M.A. Oral chemotherapy as second-line treatment option for gemcitabine-refractory advanced pancreatic cancer with poor performance status // JCO. 2019. Vol. 37, № 4_suppl. P. 405–405"),
    base("C5", "2-я линия", ["химиотерапия"], "Фторурацил + кальция фолинат",
         [drug("Фторурацил", "375–425 мг/м²", "в/в", "болюс, 1–5 дни 28-дневного цикла", "28-дневный цикл", met_until),
          drug("Кальция фолинат", "20 мг/м²", "в/в", "болюс, 1–5 дни 28-дневного цикла", "28-дневный цикл", met_until)],
         s_stage, ecog="ECOG 2; билирубин <3×ВГН; ранее использовался гемцитабин",
         uur="B", udd=3, refs=["121", "122"],
         cite="Neoptolemos J.P. et al. Adjuvant Chemotherapy With Fluorouracil Plus Folinic Acid vs Gemcitabine Following Pancreatic Cancer Resection: A Randomized Controlled Trial // JAMA. 2010. Vol. 304, № 10. P. 1073"),
]
for r in R[-13:]:
    if not r["source"].get("table"):
        r["source"]["table"] = tbl5

# ---------- C6: локорегионарный рецидив — ХЛТ с капецитабином ----------
R.append(base("C6", "лечение изолированного локорегионарного рецидива/продолженного роста первичной опухоли", ["химиолучевая терапия (ХЛТ)"], "Химиолучевая терапия с капецитабином",
              [drug("Капецитабин", "830 мг/м² 2 раза в сутки", "внутрь", "ежедневно в дни лучевой терапии (ЛТ до СОД 54,4 Гр за 28 фракций)", "в дни ЛТ", "в течение лучевой терапии")],
              "изолированный локорегионарный рецидив после хирургического лечения либо продолженный рост первичной нерезектабельной опухоли без отдалённых метастазов",
              uur="C", udd=5, refs=["143", "144"],
              cite="Balaban E.P. et al. Locally Advanced, Unresectable Pancreatic Cancer: American Society of Clinical Oncology Clinical Practice Guideline // JCO. 2016. Vol. 34, № 22. P. 2654–2668",
              special="** ЖНВЛП; # off-label у компонентов; альтернатива — 3–4 мес ХТ с последующей стереотаксической ЛТ (3 фракции СОД 30–45 Гр или 5 фракций СОД 25–45 Гр)",
              ))

audit.event(DOC, "phase2-start", "355_5 рак поджелудочной железы: cohort-first extraction")
audit.read_block(DOC, "355_5.md", 1172, 1270, "§3.2 Консервативное лечение: 3.2.1 периоперационная/адъювантная (таблица 3), 3.2.2 метастатический (таблицы 4-5, ХЛТ)")
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
    for k in ("section", "references", "citation", "table"):
        filled.setdefault(f"source.{k}", []).append(bool(r["source"].get(k)))

print(f"{DOC}: {len(R)} rows, {len(cohorts)} cohorts")
for k, v in filled.items():
    print(f"  {k}: {sum(v)}/{len(v)}")
