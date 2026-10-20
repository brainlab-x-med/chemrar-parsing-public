# -*- coding: utf-8 -*-
"""Build cohorts + medication regimens for doc 497_2 (мезотелиома плевры, брюшины и других локализаций)."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit  # noqa: E402

DOC = "497_2"

DISEASE = {
    "name": "Мезотелиома плевры, брюшины и других локализаций",
    "icd10": "C45 (C45.0 плевра, C45.1 брюшина, C45.2 перикард, C45.7/C45.9 другие и неуточнённые локализации)",
    "histology_type": "эпителиоидный, саркоматоидный и смешанный (бифазный) гистологические подтипы",
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
    {"cohort_id": "C1", "disease": DISEASE,
     "stage": "нерезектабельная/распространённая мезотелиома (IIIB–IV стадии для мезотелиомы плевры), ранняя стадия при невозможности операции, смешанный или саркоматоидный подтип",
     "resectability": "нерезектабельный либо операция невозможна",
     "clinical_situation": "1-я линия лекарственного лечения",
     "ecog": None,
     "biomarkers": ["PD-L1 (>1% — преимущество ниволумаб+ипилимумаб)", "гистотип: неэпителиоидный (приоритет ИТ) / эпителиоидный"],
     "treatment_stages": ["6 курсов ХТ с последующим динамическим наблюдением; смена режима только при доказанном прогрессировании или непереносимости"],
     "source": {"section": "3.3"}},
    {"cohort_id": "C2", "disease": DISEASE,
     "stage": "прогрессирование после 1-й линии (раннее прогрессирование <6 мес или непереносимость)",
     "resectability": None, "clinical_situation": "2-я и последующие линии",
     "ecog": None,
     "biomarkers": ["MSI-H (мезотелиома брюшины, для пембролизумаба 2–3Л)"],
     "treatment_stages": ["режимы 2–3 линий, ранее не применявшиеся; реиндукция 1-й линии при прогрессировании ≥6 мес после последнего курса"],
     "source": {"section": "3.3"}},
    {"cohort_id": "C3", "disease": DISEASE,
     "stage": "эпителиоидная мезотелиома плевры (тримодальная терапия)",
     "resectability": None, "clinical_situation": "неоадъювантная/адъювантная химиотерапия в рамках комбинированного лечения",
     "ecog": None, "biomarkers": ["эпителиоидный гистотип"],
     "treatment_stages": ["2–4 курса предоперационной ХТ → хирургия → послеоперационная ЛТ; адъювантная ХТ после пульмонэктомии при N1; до/после операции возможно 4–6 циклов ХТ"],
     "source": {"section": "3.3"}},
]

JNVLP = "** ЖНВЛП; "
R = []

# ---- C1: 1L ----
pem_pt = [drug("Пеметрексед", "500 мг/м²", "в/в", "1-й день", "каждые 21 день", 6),
          drug("Цисплатин", "75 мг/м²", "в/в", "1-й день", "каждые 21 день", 6)]
R += [
    base("C1", "1-я линия (оптимальный режим)", ["химиотерапия"], "PemPt (пеметрексед + цисплатин)",
         pem_pt, "нерезектабельная/распространённая мезотелиома (IIIB–IV); ранняя стадия при невозможности операции",
         uur="A", udd=2, refs=["89"], cite="Vogelzang N.J., Rusthoven J.J., Symanowski J. et al. Phase III study of pemetrexed in combination with cisplatin versus cisplatin alone in patients with malignant pleural mesothelioma",
         special=JNVLP + "# off-label у цисплатина; эффективность поддерживающей терапии пеметрекседом не доказана"),
    base("C1", "1-я линия (альтернативный режим)", ["химиотерапия"], "PemCarb (пеметрексед + карбоплатин)",
         [drug("Пеметрексед", "500 мг/м²", "в/в", "1-й день", "каждые 21 день", 6),
          drug("Карбоплатин", "AUC 5 (фактическая доза рассчитывается индивидуально по креатинину накануне лечения)", "в/в", "1-й день", "каждые 21 день", 6)],
         "нерезектабельная/распространённая мезотелиома (IIIB–IV)", uur="A", udd=3, refs=["90", "141"],
         cite="Castagneto B., Bota M., Aitini E. et al. Phase II study of pemetrexed in combination with carboplatin in patients with malignant pleural mesothelioma. Ann Oncol 2008;19:370–373",
         special=JNVLP),
    base("C1", "1-я линия (альтернативный режим)", ["химиотерапия"], "GemPt (гемцитабин + цисплатин)",
         [drug("Гемцитабин", "1000–1250 мг/м²", "в/в", "1, 8 (15)-й дни", "каждые 21 день", 6),
          drug("Цисплатин", "75 мг/м²", "в/в", "1-й день", "каждые 21 день", 6)],
         "нерезектабельная/распространённая мезотелиома (IIIB–IV)", uur="B", udd=3, refs=["91", "92"],
         cite="Nowak A.K., Byrne M.J., Willianson R. et al. A multicentre phase II study of cisplatin and gemcitabine for malignant mesothelioma. Br J Cancer 2002;87:491–496",
         special=JNVLP),
    base("C1", "1-я линия", ["химиотерапия", "таргетная терапия"], "PemPt + бевацизумаб",
         pem_pt[:-1] + [drug("Цисплатин", "75 мг/м²", "в/в", "1-й день", "каждые 21 день", 6),
                        drug("Бевацизумаб", "15 мг/кг", "в/в", "1-й день", "каждые 21 день", 6)],
         "нерезектабельная/распространённая мезотелиома (IIIB–IV)", uur="A", udd=2, refs=["93", "94"],
         cite="Zalcman G., Mazieres J., Margery J. et al. Bevacizumab for newly diagnosed pleural mesothelioma in the Mesothelioma Avastin Cisplatin Pemetrexed Study (MAPS): a randomised, controlled, open-label phase 3 trial",
         special=JNVLP + "# off-label; MAPS: улучшение ВБП и ОВ vs пеметрексед+цисплатин, но увеличение токсичности; добавление к гемцитабин+цисплатин преимуществ не показало",
         maint="После 6 курсов тройной комбинации — поддерживающая терапия бевацизумабом каждые 3 недели до прогрессирования или непереносимой токсичности"),
    base("C1", "1-я линия", ["химиотерапия", "таргетная терапия"], "PemCarb + бевацизумаб",
         [drug("Пеметрексед", "500 мг/м²", "в/в", "1-й день", "каждые 21 день", 6),
          drug("Карбоплатин", "AUC 5 (индивидуальный расчёт по креатинину)", "в/в", "1-й день", "каждые 21 день", 6),
          drug("Бевацизумаб", "15 мг/кг", "в/в", "1-й день", "каждые 21 день", 6)],
         "нерезектабельная/распространённая мезотелиома (IIIB–IV)", uur="A", udd=4, refs=["95"],
         cite="Ceresoli G.L. et al. Phase II study of pemetrexed and carboplatin plus bevasizumab as first-line therapy in malignant pleural mesothelioma. Br J Cancer 2013;109:552-558",
         special=JNVLP,
         maint="После 6 курсов тройной комбинации — поддерживающая терапия бевацизумабом каждые 3 недели до прогрессирования или непереносимой токсичности"),
    base("C1", "1-я линия (иммунотерапия)", ["иммунотерапия"], "Ниволумаб + ипилимумаб (Nivo/Ipi)",
         [drug("Ниволумаб", "360 мг (допустимо 240 мг каждые 14 дней или 3 мг/кг каждые 14 дней)", "в/в", "1-й день каждые 3 нед", "каждые 3 или 2 недели", "максимум 2 года"),
          drug("Ипилимумаб", "1 мг/кг", "в/в", "1-й день каждые 6 нед", "каждые 6 недель")],
         "нерезектабельная мезотелиома плевры", bio=["приоритет при неэпителиоидном (саркоматоидном/бифазном) гистотипе", "PD-L1 >1% (преимущество ИТ: мОВ 18,0 против 13,3 мес)"],
         uur="A", udd=2, refs=["96"],
         cite="Baas P., Scherpereel A., Nowak A. et al. First-line nivolumab plus ipilimumab in unresectable malignant pleural mesothelioma (CheckMate 743): a multicentre, randomised phase 3 trial",
         special=JNVLP + "; особенно предпочтительна для саркоматоидного варианта опухоли"),
    base("C1", "1-я линия (иммунохимиотерапия)", ["химиотерапия", "иммунотерапия"], "PemPt (+PemCarb) + пембролизумаб",
         [drug("Пеметрексед", "500 мг/м²", "в/в", "1-й день", "каждые 21 день", 6),
          drug("Цисплатин", "75 мг/м² (или карбоплатин AUC 5)", "в/в", "1-й день", "каждые 21 день", 6),
          drug("Пембролизумаб", "200 мг", "в/в", "1-й день", "каждые 21 день")],
         "эпителиоидная мезотелиома плевры (KEYNOTE-483)", bio=["эпителиоидный вариант опухоли"],
         uur="A", udd=2, refs=["103", "104"],
         cite="Chu Q., Perrone F., Greillier L. et al. Pembrolizumab plus chemotherapy versus chemotherapy in untreated advanced pleural mesothelioma in Canada, Italy, and France: a phase 3, open-label trial (KEYNOTE-483)",
         special=JNVLP + "# off-label; KEYNOTE-483: статистически значимое улучшение ОВ (17,3 vs 16,1 мес)",
         maint="После 6 курсов тройной комбинации — поддерживающая терапия пембролизумабом каждые 3 недели до прогрессирования или непереносимой токсичности"),
]

# ---- C2: 2L+ ----
R += [
    base("C2", "2-я линия (при невозможности применения соединений платины)", ["химиотерапия"], "Гемцитабин монотерапия",
         [drug("Гемцитабин", "1000–1250 мг/м²", "в/в", "1-й и 8-й дни", "каждые 21 день", 6)],
         "прогрессирование после 1-й линии", uur="B", udd=3, refs=["98", "99"],
         cite="Van Meerbeeck J.P. et al. A phase II study of gemcitabine in patients with malignant pleural mesothelioma (EORTC Lung Cancer Cooperative Group)",
         special=JNVLP + "# off-label"),
    base("C2", "2-я линия (при невозможности применения соединений платины)", ["химиотерапия"], "Пеметрексед монотерапия",
         [drug("Пеметрексед", "500 мг/м²", "в/в", "1-й день", "каждые 21 день", 6)],
         "прогрессирование после 1-й линии", uur="B", udd=3, refs=["100"],
         cite="Taylor P. et al. Single-agent pemetrexed for chemonaive and pretreated patients with malignant pleural mesothelioma: results of an International Expanded Access Program",
         special=JNVLP),
    base("C2", "2–3-я линии", ["химиотерапия"], "Винорелбин монотерапия",
         [drug("Винорелбин", "25 или 30 мг/м²", "в/в", "1 раз в неделю", "еженедельно", 6)],
         "прогрессирование после 1-й и 2-й линий", uur="B", udd=3, refs=["99", "101", "102"],
         cite="Zauderer M.G., Kass S.L., Woo K. et al. Vinorelbine and gemcitabine as second- or third-line therapy for malignant pleural mesothelioma. Lung Cancer 2014;84:271-274",
         special=JNVLP + "# off-label"),
    base("C2", "2–3-я линия при мезотелиоме брюшины", ["иммунотерапия"], "Пембролизумаб монотерапия (MSI-H)",
         [drug("Пембролизумаб", "200 мг", "в/в", "капельно, каждые 3 недели", "каждые 3 недели")],
         "мезотелиома брюшины", bio=["MSI-H (встречается в 1–2% случаев мезотелиомы брюшины)"],
         uur="C", udd=4, refs=["105", "106"],
         cite="Popat S., Cunoni-Fontecedro A., Polydoropoulou V. et al. A multicenter randomized phase III trial comparing pembrolizumab vs single agent chemotherapy for advanced pre-treated malignant mesothelioma",
         special=JNVLP + "; зарегистрирован в РФ для солидных опухолей при MSI-high; у больных без MSI-H преимуществ перед ХТ не показал"),
    base("C2", "2–3-я линии", ["иммунотерапия"], "Ниволумаб ± ипилимумаб (если комбинация не применялась в 1-й линии)",
         [drug("Ниволумаб", "3 мг/кг (также изучалась дозировка 240 мг)", "в/в", "капельно каждые 14 дней", "каждые 2 недели", "до прогрессирования/непереносимой токсичности, но не более 2 лет"),
          drug("Ипилимумаб", "1 мг/кг", "в/в", "капельно каждые 6 недель", "каждые 6 недель", None)],
         "прогрессирование после 1-й линии", uur="A", udd=2, refs=["107", "108", "109", "110", "111"], cite=None,
         special=JNVLP + "; цитацию [107] не удалось однозначно сопоставить со списком литературы"),
]

# ---- C3: периоперационная ----
R.append(base("C3", "неоадъювантная/адъювантная химиотерапия в составе тримодальной терапии", ["химиотерапия"],
              "Пеметрексед + цисплатин/карбоплатин (периоперационно, 2–4 курса предоперационной ХТ; всего до 6 циклов до/после операции)",
              [drug("Пеметрексед", "500 мг/м²", "в/в", "1-й день", "каждые 21 день", "2–4 курса предоперационно; всего до 6 циклов"),
               drug("Цисплатин", "75 мг/м² (или карбоплатин AUC 5)", "в/в", "1-й день", "каждые 21 день")],
              "эпителиоидная мезотелиома плевры (планируемая хирургическая циторедукция + ЛТ)",
              uur="C", udd=5, refs=["112", "113"], cite=None,
              special=JNVLP + "# off-label; таргетная терапия бевацизумабом и иммунотерапия в неоадъювантном режиме не используются; цитацию [112] не удалось однозначно сопоставить со списком литературы"))

audit.event(DOC, "phase2-start", "497_2 мезотелиома: cohort-first extraction")
audit.read_block(DOC, "497_2.md", 354, 404, "§3.3 Лекарственное лечение + таблица 3 схем")
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
