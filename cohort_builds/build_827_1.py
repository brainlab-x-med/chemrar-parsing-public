# Build 827_1 (Макроглобулинемия Вальденстрема) — cohorts + medication regimens
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit

DOC = "827_1"
DISEASE = {
    "name": "Макроглобулинемия Вальденстрема (лимфоплазмацитарная лимфома)",
    "icd10": "C88.0",
    "histology_type": "лимфоплазмацитарная лимфома с секрецией моноклонального IgM (панель плазмоцитоидных лимфоцитов в костном мозге)",
}

audit.event(DOC, "phase2-start", "§3 Лечение L167-275 + Приложение А3.1 режимы ЛТ L496-571 + Список литературы")
audit.read_block(DOC, f"{DOC}.md", 167, 275, "§3.1-3.4: показания, 1-я линия, поддерживающая терапия, рецидивы")
audit.read_block(DOC, f"{DOC}.md", 496, 571, "Приложение А3.1: дозы ритуксимаб/RBD/RB/RBBd/R-EPOCH+ибрутиниб/RCD/CP-R/FCR/BTK-ингибиторы")

cohorts = [
    {"cohort_id": "C1", "disease": DISEASE,
     "stage": None,
     "resectability": None,
     "clinical_situation": "Впервые диагностированная МВ, требующая терапии (симптомная: анемия Hb ≤10 г/дл, тромбоцитопения ≤100×10⁹/л, IgM >50 г/л, гипервязкость, нейропатия, амилоидоз и др.); тлеющая (бессимптомная) МВ терапии не подлежит",
     "ecog": None, "biomarkers": ["мутация MYD88 (предиктор ответа на ингибиторы BTK)", "моноклональный IgM"],
     "treatment_stages": ["индукционная терапия"], "parent": None, "source": {"section": "3.2"}},
    {"cohort_id": "C1a", "disease": DISEASE, "stage": None,
     "resectability": None,
     "clinical_situation": "Синдром гипервязкости, криоглобулинемия, холодовая агглютининемия или необходима быстрая редукция опухоли (плазмаферез перед системной терапией)",
     "ecog": None, "biomarkers": [], "treatment_stages": ["индукционная терапия"], "parent": "C1",
     "source": {"section": "3.2"}},
    {"cohort_id": "C1b", "disease": DISEASE, "stage": None,
     "resectability": None,
     "clinical_situation": "Цитопении (особенно тромбоцитопения), умеренная/тяжелая органомегалия или массивная лимфаденопатия",
     "ecog": None, "biomarkers": [], "treatment_stages": ["индукционная терапия"], "parent": "C1",
     "source": {"section": "3.2"}},
    {"cohort_id": "C1c", "disease": DISEASE, "stage": None,
     "resectability": None,
     "clinical_situation": "Низкий уровень моноклонального белка, медленно прогрессирующая болезнь, сопутствующая патология; либо изолированная периферическая нейропатия (IgM к анти-MAG) без иных симптомов",
     "ecog": None, "biomarkers": [], "treatment_stages": ["индукционная терапия"], "parent": "C1",
     "source": {"section": "3.2"}},
    {"cohort_id": "C1d", "disease": DISEASE, "stage": None,
     "resectability": None,
     "clinical_situation": "Периферическая нейропатия, связанная с парапротеином (избегать нейротоксичных бортезомиба и винкристина)",
     "ecog": None, "biomarkers": [], "treatment_stages": ["индукционная терапия"], "parent": "C1",
     "source": {"section": "3.2"}},
    {"cohort_id": "C1e", "disease": DISEASE, "stage": None,
     "resectability": None,
     "clinical_situation": "<65 лет, высокий/промежуточный риск по IPSSWM/Revised IPSSWM (возможна высокодозная консолидация с поддержкой ауто-СКК)",
     "ecog": None, "biomarkers": [], "treatment_stages": ["интенсифицированная индукция", "ВДХТ с ауто-ТГСК"], "parent": "C1",
     "source": {"section": "3.2"}},
    {"cohort_id": "C1f", "disease": DISEASE, "stage": None,
     "resectability": None,
     "clinical_situation": ">65 лет, высокий/промежуточный риск по IPSSWM/Revised IPSSWM",
     "ecog": None, "biomarkers": [], "treatment_stages": ["индукционная терапия"], "parent": "C1",
     "source": {"section": "3.2"}},
    {"cohort_id": "C2", "disease": DISEASE, "stage": None,
     "resectability": None,
     "clinical_situation": "Рецидив/рефрактерная МВ: при позднем рецидиве (>12 мес) возможно возобновление прежней терапии, при раннем — смена программы на препараты других групп",
     "ecog": None, "biomarkers": [], "treatment_stages": ["терапия рецидивов"], "parent": None,
     "source": {"section": "3.4"}},
]

CITES = {
    "4": "Gertz MA. Waldenström macroglobulinemia: 2023 update on diagnosis, risk stratification, and management // Am J Hematol. 2023;98(2):348—358",
    "11": "Kumar S.K. et al. Waldenström Macroglobulinemia/ Lymphoplasmacytic Lymphoma // NCCN Clinical Practice Guidelines in Oncology (NCCN Guidelines®). 2020",
    "24": "Sarosiek S, Sermer D, Branagan AR, Treon SP, Castillo JJ. Zanubrutinib for the treatment of adults with Waldenstrom macroglobulinemia // Expert Rev Anticancer Ther. 2022;22(5):471-478",
    "23": "Owen RG, McCarthy H, Rule S, et al. Acalabrutinib monotherapy in patients with Waldenstrom macroglobulinemia: a single-arm, multicentre, phase 2 study // Haematologica. 2020;7(2):e112-e121",
    "31": "Dimopoulos M.A. et al. Predictive factors for response to rituximab in Waldenstrom's macroglobulinemia // Clin. Lymphoma. 2005. Vol. 5, № 4. P. 270–272",
    "32": "Dimopoulos M.A. et al. Primary treatment of Waldenström macroglobulinemia with dexamethasone, rituximab, and cyclophosphamide // J. Clin. Oncol. 2007. Vol. 25, № 22. P. 3344–3349",
    "34": "Paludo J. et al. Bendamustine and rituximab (BR) versus dexamethasone, rituximab, and cyclophosphamide (DRC) in patients with Waldenström macroglobulinemia // Ann. Hematol. 2018. Vol. 97, № 8. P. 1417–1425",
    "36": "Leukothea Ioakimidis, Christopher J. Patterson et al. Comparative outcomes following CP-R, CVP-R, and CHOP-R in Waldenstrom macroglobulinemia // Clin Lymphoma Myeloma. 2009;9(1):62-6",
    "37": "Treon S.P. et al. Bendamustine therapy in patients with relapsed or refractory Waldenström's macroglobulinemia // Clinical Lymphoma, Myeloma and Leukemia. 2011. Vol. 11, № 1. P. 133–135",
    "38": "Treon S.P. et al. Primary therapy of Waldenström macroglobulinemia with bortezomib, dexamethasone, and rituximab: WMCTG clinical trial 05-180 // J. Clin. Oncol. 2009. Vol. 27, № 23. P. 3830–3835",
    "39": "Tedeschi A, Benevolo G, Varettoni M et al. Fludarabine plus cyclophosphamide and rituximab in Waldenstrom macroglobulinemia: An effective but myelosuppressive regimen // Cancer. 2012;118(2):434—443",
    "40": "Kyle R.A. et al. Waldenstrom's macroglobulinaemia: A prospective study comparing daily intermittent oral chlorambucil // Br. J. Haematol. 2000. Vol. 108, № 4. P. 737–742",
    "41": "Treon S.P. et al. Ibrutinib monotherapy in symptomatic, treatment-naïve patients with Waldenström macroglobulinemia // J. Clin. Oncol. 2018. Vol. 36, № 27. P. 2755–2761",
    "42": "Migkou M, Fotiou D, Gavriatopoulou M, Dimopoulos MA. Ibrutinib plus rituximab for the treatment of adult patients with Waldenstrom's macroglobulinemia: a safety evaluation // Expert Opin Drug Saf. 2021;20(9):987-995",
    "44": "Алгоритмы диагностики и протоколы лечения заболеваний системы крови под редакцией Е.Н. Паровичниковой. 2024, том 2, стр. 174–203",
    "45": "Грачёв А.Е., Грибанова Е.О., Рыжко В.В., Гальцева И.В. и др. Терапия Макроглобулинемии Вальденстрема у пациентов моложе 65 лет с факторами неблагоприятного прогноза // Гематология и трансфузиология. Приложение 69.2.2024. С. 32",
    "46": "Грачёв А.Е., Грибанова Е.О., Рыжко В.В., Гальцева И.В. и др. Интенсификация терапии макроглобулинемии Вальденстрема высокого риска для пациентов старше 65 лет // Гематология и трансфузиология. Приложение 69.2.2024. С. 201",
    "47": "Грачёв А.Е., Грибанова Е.О., Рыжко В.В., Гальцева И.В. и др. Трансформация Макроглобулинемии Вальденстрема в ДБККЛ – новый взгляд на терапию // Гематология и трансфузиология. Приложение 69.2.2024. С. 202",
    "49": "Treon S.P. et al. Maintenance Rituximab is associated with improved clinical outcome in rituximab naïve patients with Waldenstrom Macroglobulinaemia who respond to a rituximab-containing regimen // Br. J. Haematol. 2011. Vol. 154, № 3. P. 357–362",
}


def cite(refs):
    return CITES.get(refs[0]) if refs else None


def row(cid, line_stage, name, drugs, refs, uur, udd, section, table="Приложение А3.1. Режимы лекарственного лечения МВ",
        special="", maint=None):
    return {
        "cohort_id": cid,
        "disease": DISEASE,
        "treatment": {"line_stage": line_stage, "therapy_type": ["химиотерапия", "иммунотерапия"], "regimen_name": name},
        "drugs": drugs,
        "indications": {"stage": "Симптомная МВ (стадии не применимы; стратификация по IPSSWM/Revised IPSSWM)", "ecog": None, "biomarkers": []},
        "evidence": {"uur": uur, "udd": udd},
        "source": {"page": None, "section": section, "table": table, "references": refs, "citation": cite(refs)},
        "special_conditions": special,
        "maintenance_therapy": maint,
    }


rows = [
    row("C1c", "1-я линия (низкий уровень моноклонального белка, медленно прогрессирующая болезнь, сопутствующая патология; изолированная IgM-нейропатия)",
        "Монотерапия #ритуксимабом", [{"inn": "Ритуксимаб", "dose": "375 мг/м²", "route": "в/в капельно", "schedule": "1 раз в неделю в течение 4 недель", "cycle_frequency": "курс повторяют через 12 недель", "max_cycles": None}],
        ["31", "36"], "C", 5, "3.2"),
    row("C1a", "1-я линия, синдром гипервязкости/необходимость быстрой редукции опухоли", "RBD (#ритуксимаб/#бортезомиб/#дексаметазон)",
        [{"inn": "Ритуксимаб", "dose": "375 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день (лечение возобновляется на 22-й день)", "max_cycles": "4–6 курсов"},
         {"inn": "Бортезомиб", "dose": "1,3 мг/м²", "route": "п/к", "schedule": "дни 1, 4, 8, 11", "cycle_frequency": "цикл 21 день", "max_cycles": "4–6 курсов"},
         {"inn": "Дексаметазон", "dose": "40 мг", "route": "в/в", "schedule": "дни 1, 4, 8, 11", "cycle_frequency": "цикл 21 день", "max_cycles": "4–6 курсов"}],
        ["38"], "C", 4, "3.2",
        special="Программа выбора при синдроме гипервязкости; перед введением ритуксимаба при IgM ≥50 г/л целесообразен плазмаферез (профилактика феномена «вспышки» парапротеина)"),
    row("C2", "Терапия рецидивов", "RBD (#ритуксимаб/#бортезомиб/#дексаметазон)",
        [{"inn": "Ритуксимаб", "dose": "375 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": "4–6 курсов"},
         {"inn": "Бортезомиб", "dose": "1,3 мг/м²", "route": "п/к", "schedule": "дни 1, 4, 8, 11", "cycle_frequency": "цикл 21 день", "max_cycles": "4–6 курсов"},
         {"inn": "Дексаметазон", "dose": "40 мг", "route": "в/в", "schedule": "дни 1, 4, 8, 11", "cycle_frequency": "цикл 21 день", "max_cycles": "4–6 курсов"}],
        ["4", "11"], "C", 5, "3.4"),
    row("C1b", "1-я линия (цитопении, органомегалия, массивная лимфаденопатия)", "RB (#ритуксимаб/#бендамустин)",
        [{"inn": "Ритуксимаб", "dose": "375 мг/м²", "route": "в/в", "schedule": "день 0", "cycle_frequency": "цикл 28 дней (лечение возобновляется на 28-й день)", "max_cycles": "4–6 курсов"},
         {"inn": "Бендамустин", "dose": "90 мг/м²", "route": "в/в", "schedule": "дни 1, 2", "cycle_frequency": "цикл 28 дней", "max_cycles": "4–6 курсов"}],
        ["34"], "C", 5, "3.2",
        special="Для схемы RB уровень убедительности рекомендаций C (УДД 5); основной выбор при цитопениях вместе с RCD"),
    row("C1b", "1-я линия (цитопении, органомегалия, массивная лимфаденопатия); эффективна также при нейропатии", "RCD (#ритуксимаб/#циклофосфамид/#дексаметазон)",
        [{"inn": "Ритуксимаб", "dose": "375 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день (лечение возобновляется на 22-й день)", "max_cycles": 6},
         {"inn": "Циклофосфамид", "dose": "100 мг/м²", "route": "внутрь 2 раза в день", "schedule": "дни 1–5", "cycle_frequency": "цикл 21 день", "max_cycles": 6},
         {"inn": "Дексаметазон", "dose": "20 мг", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": 6}],
        ["32", "34"], "C", 4, "3.2"),
    row("C1d", "1-я линия (IgM-ассоциированная периферическая полинейропатия)", "CP-R (#циклофосфамид/#преднизолон/#ритуксимаб)",
        [{"inn": "Ритуксимаб", "dose": "375 мг/м²", "route": "в/в", "schedule": "день 1 курса", "cycle_frequency": "цикл 21 день (лечение возобновляется на 22-й день)", "max_cycles": "4–6 курсов"},
         {"inn": "Циклофосфамид", "dose": "1000 мг/м² (доза может быть уменьшена по клинической ситуации)", "route": "в/в", "schedule": "день 1 курса", "cycle_frequency": "цикл 21 день", "max_cycles": "4–6 курсов"},
         {"inn": "Преднизолон", "dose": "100 мг", "route": "внутрь", "schedule": "дни 1–5", "cycle_frequency": "цикл 21 день", "max_cycles": "4–6 курсов"}],
        ["36"], "C", 5, "3.2",
        special="При тяжелой нейропатии применять комбинации CP-R и RCD для более выраженного снижения парапротеина; избегать схем с бортезомибом и винкристином"),
    row("C1e", "1-я линия, генерализованные формы", "FCR (#флударабин/#циклофосфамид/#ритуксимаб)",
        [{"inn": "Ритуксимаб", "dose": "375 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 28 дней (лечение возобновляется на 29-й день)", "max_cycles": 6},
         {"inn": "Флударабин", "dose": "25 мг/м²", "route": "в/в", "schedule": "дни 2–4", "cycle_frequency": "цикл 28 дней", "max_cycles": 6},
         {"inn": "Циклофосфамид", "dose": "250 мг/м²", "route": "в/в", "schedule": "дни 2–4", "cycle_frequency": "цикл 28 дней", "max_cycles": 6}],
        ["39"], "C", 4, "3.2",
        special="# off-label (флударабин); миелосупрессия/иммуносупрессия, риск вторичных ОМЛ/МДС и трансформации; аналоги пуринов не рекомендованы как стартовая терапия молодых пациентов (мешают сбору ГСК)"),
    row("C1e", "1-я линия, <65 лет, высокий/промежуточный риск IPSSWM, интенсификация (ротирующие курсы)", "R-EPOCH + ибрутиниб / R-BAC + ибрутиниб",
        [{"inn": "Ритуксимаб", "dose": "375 мг/м²", "route": "в/в", "schedule": "день 0 каждого курса", "cycle_frequency": "R-EPOCH цикл 21 день, затем R-BAC на 22-й день, снова R-EPOCH на 29-й день", "max_cycles": 4},
         {"inn": "Винкристин (курс R-EPOCH)", "dose": "0,4 мг/м²/сут", "route": "в/в непрерывная 96-часовая инфузия", "schedule": "дни 1–4", "cycle_frequency": "по ротации", "max_cycles": 2},
         {"inn": "Циклофосфамид (курс R-EPOCH)", "dose": "750 мг/м²/сут", "route": "в/в", "schedule": "день 5", "cycle_frequency": "по ротации", "max_cycles": 2},
         {"inn": "Преднизолон (курс R-EPOCH)", "dose": "60 мг/м²/сут", "route": "в/в", "schedule": "дни 1–5", "cycle_frequency": "по ротации", "max_cycles": 2},
         {"inn": "Ибрутиниб", "dose": "420 мг/сут", "route": "внутрь", "schedule": "ежедневно, дни 0–14 каждого курса", "cycle_frequency": "ежедневно внутри курса", "max_cycles": None},
         {"inn": "Бендамустин (курс R-BAC)", "dose": "90 мг/м²", "route": "в/в", "schedule": "дни 1, 2", "cycle_frequency": "по ротации", "max_cycles": 2},
         {"inn": "Цитарабин (курс R-BAC)", "dose": "500 мг/м²", "route": "в/в", "schedule": "дни 1, 2, 3", "cycle_frequency": "по ротации", "max_cycles": 2}],
        ["44", "45"], "C", 5, "3.2",
        special="После 4-го курса (второго R-BAC) — мобилизация и сбор ауто-СКК; далее высокодозная консолидация по программе CEAM или Даратумумаб+CEAM с поддержкой ауто-ТГСК (дозы консолидации в данной КР не приведены — см. протокол НМИЦ гематологии)"),
    row("C1e", "1-я линия, <65 лет с гистологической крупноклеточной трансформацией (ротирующие курсы)", "R-EPOCH + ибрутиниб + #венетоклакс / R-BAC + ибрутиниб + #венетоклакс",
        [{"inn": "Ритуксимаб", "dose": "375 мг/м²", "route": "в/в", "schedule": "день 0 каждого курса", "cycle_frequency": "R-EPOCH цикл 21 день, затем R-BAC на 22-й день, снова R-EPOCH на 29-й день", "max_cycles": 4},
         {"inn": "Винкристин (курс R-EPOCH)", "dose": "0,4 мг/м²/сут", "route": "в/в непрерывная 96-часовая инфузия", "schedule": "дни 1–4", "cycle_frequency": "по ротации", "max_cycles": 2},
         {"inn": "Циклофосфамид (курс R-EPOCH)", "dose": "750 мг/м²/сут", "route": "в/в", "schedule": "день 5", "cycle_frequency": "по ротации", "max_cycles": 2},
         {"inn": "Преднизолон (курс R-EPOCH)", "dose": "60 мг/м²/сут", "route": "в/в", "schedule": "дни 1–5", "cycle_frequency": "по ротации", "max_cycles": 2},
         {"inn": "Ибрутиниб", "dose": "420 мг/сут", "route": "внутрь", "schedule": "ежедневно, дни 0–14 каждого курса", "cycle_frequency": "ежедневно внутри курса", "max_cycles": None},
         {"inn": "Венетоклакс", "dose": "400 мг/сут", "route": "внутрь", "schedule": "ежедневно, дни 0–14 каждого курса", "cycle_frequency": "ежедневно внутри курса", "max_cycles": None},
         {"inn": "Бендамустин (курс R-BAC)", "dose": "90 мг/м²", "route": "в/в", "schedule": "дни 1, 2", "cycle_frequency": "по ротации", "max_cycles": 2},
         {"inn": "Цитарабин (курс R-BAC)", "dose": "500 мг/м²", "route": "в/в", "schedule": "дни 1, 2, 3", "cycle_frequency": "по ротации", "max_cycles": 2}],
        ["44", "47"], "C", 5, "3.2",
        special="# off-label (венетоклакс); всего 4 курса иммунохимиотерапии по ротирующей схеме; далее высокодозная консолидация CEAM или Даратумумаб+CEAM с поддержкой ауто-ТГСК (дозы в данной КР не приведены)"),
    row("C1f", "1-я линия, >65 лет, высокий/промежуточный риск IPSSWM", "RBBd (#ритуксимаб/#бортезомиб/#бендамустин/#дексаметазон)",
        [{"inn": "Ритуксимаб", "dose": "375 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 18–21 день (перерыв между курсами 7–10 дней)", "max_cycles": "4–6 курсов"},
         {"inn": "Бортезомиб", "dose": "1,3 мг/м²", "route": "п/к", "schedule": "дни 1, 4, 8, 11", "cycle_frequency": "цикл 18–21 день", "max_cycles": "4–6 курсов"},
         {"inn": "Бендамустин", "dose": "90 мг/м²", "route": "в/в", "schedule": "дни 1, 2", "cycle_frequency": "цикл 18–21 день", "max_cycles": "4–6 курсов"},
         {"inn": "Дексаметазон", "dose": "20 мг", "route": "в/в или внутрь", "schedule": "дни 1, 4, 8, 11", "cycle_frequency": "цикл 18–21 день", "max_cycles": "4–6 курсов"}],
        ["44", "46"], "C", 5, "3.2"),
    row("C1", "Поддерживающая терапия после ответа на индукционную ритуксимаб-содержащую программу", "Поддерживающая терапия #ритуксимабом",
        [{"inn": "Ритуксимаб", "dose": "375 мг/м²", "route": "в/в", "schedule": "1 введение", "cycle_frequency": "каждые 3 месяца", "max_cycles": "в течение 2 лет"}],
        ["49"], "C", 3, "3.3",
        maint="Ритуксимаб 375 мг/м² каждые 3 месяца в течение 2 лет (после ПО/ОХЧО на ритуксимаб-содержащую индукцию); увеличивает инфекционные осложнения",
        special="Вопрос о поддерживающей терапии обсуждается; назначается пациентам с ПО или ОХЧО после индукции"),
    row("C2", "Терапия рецидивов", "RB (#ритуксимаб/#бендамустин)",
        [{"inn": "Ритуксимаб", "dose": "375 мг/м²", "route": "в/в", "schedule": "день 0", "cycle_frequency": "цикл 28 дней", "max_cycles": "4–6 курсов"},
         {"inn": "Бендамустин", "dose": "90 мг/м²", "route": "в/в", "schedule": "дни 1, 2", "cycle_frequency": "цикл 28 дней", "max_cycles": "4–6 курсов"}],
        ["37"], "C", 4, "3.4",
        special="Наиболее эффективен при рецидивах/рефрактерности бендамустин в сочетании с ритуксимабом (эффект 83,3%, медиана ВБП 13,2 мес.)"),
    row("C2", "Терапия рецидивов", "FCR (#флударабин/#циклофосфамид/#ритуксимаб) / FR",
        [{"inn": "Ритуксимаб", "dose": "375 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 28 дней", "max_cycles": 6},
         {"inn": "Флударабин", "dose": "25 мг/м²", "route": "в/в", "schedule": "дни 2–4", "cycle_frequency": "цикл 28 дней", "max_cycles": 6},
         {"inn": "Циклофосфамид", "dose": "250 мг/м²", "route": "в/в", "schedule": "дни 2–4", "cycle_frequency": "цикл 28 дней", "max_cycles": 6}],
        ["11", "39"], "C", 4, "3.4",
        special="# off-label (флударабин); рекомендуется 4-дневное введение флударабина и ограничение числа курсов до 4 из-за длительных цитопений; вариант FR (флударабин + ритуксимаб без циклофосфамида)"),
    row("C2", "Терапия рецидивов", "Ибрутиниб + #ритуксимаб (IB)",
        [{"inn": "Ибрутиниб", "dose": "420 мг", "route": "внутрь", "schedule": "ежедневно", "cycle_frequency": "ежедневно", "max_cycles": "до прогрессирования или развития непереносимой токсичности"},
         {"inn": "Ритуксимаб", "dose": "375 мг/м²", "route": "в/в", "schedule": "в 1-й день 1, 2, 3, 4 и 17, 18, 19, 20 недель терапии", "cycle_frequency": "еженедельно в указанные недели", "max_cycles": "до прогрессирования (8 введений за 20 недель)"}],
        ["4", "42"], "C", 4, "3.4"),
    row("C2", "Терапия рецидивов (ингибитор BTK)", "Терапия #занубрутинибом",
        [{"inn": "Занубрутиниб", "dose": "160 мг", "route": "внутрь каждые 12 часов", "schedule": "ежедневно", "cycle_frequency": "ежедневно", "max_cycles": "до прогрессирования или развития токсичности"}],
        ["24"], "C", 4, "3.2/А3.1",
        special="Привязка к конкретной линии в тексте КР явно не задана; применяется как ингибитор BTK при МВ (аналог ибрутиниба)"),
    row("C2", "Терапия рецидивов (ингибитор BTK)", "Монотерапия #акалабрутинибом",
        [{"inn": "Акалабрутиниб", "dose": "100 мг", "route": "внутрь каждые 12 часов", "schedule": "ежедневно", "cycle_frequency": "ежедневно", "max_cycles": "до прогрессирования или развития токсичности"}],
        ["23"], "C", 4, "3.2/А3.1",
        special="Привязка к конкретной линии в тексте КР явно не задана; применяется как ингибитор BTK при МВ (аналог ибрутиниба)"),
    row("C1", "1-я линия, альтернатива у пожилых/коморбидных", "Монотерапия #хлорамбуцилом",
        [{"inn": "Хлорамбуцил", "dose": "0,1 мг/кг", "route": "внутрь", "schedule": "длительно под контролем клинического анализа крови до фазы плато", "cycle_frequency": "ежедневно (непрерывный прием)", "max_cycles": "до фазы плато"}],
        ["40"], "C", 5, "3.2/А3.1",
        special="Не рекомендуется начинать терапию молодых пациентов с хлорамбуцила (как и с аналогов пуринов) — препятствует адекватному сбору ГСК при возможной ВДХТ с ТГСК в дальнейшем"),
]

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
