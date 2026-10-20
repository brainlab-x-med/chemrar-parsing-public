# Build 889_1 (Хронический миелоидный лейкоз, BCR::ABL1+) — cohorts + medication regimens
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit

DOC = "889_1"
DISEASE = {
    "name": "Хронический миелоидный лейкоз (ХМЛ), Ph-положительный",
    "icd10": "C92.1",
    "histology_type": "миелопролиферативное новообразование из полипотентной гемопоэтической клетки с химерным геном BCR::ABL1 [t(9;22)(q34;q11), филадельфийская хромосома]",
}

audit.event(DOC, "phase2-start", "§3 Лечение L229-523 + таблицы доз 4, 5, 13 + Список литературы")
audit.read_block(DOC, f"{DOC}.md", 256, 523, "§3.1 ИТК у взрослых (табл.4-5), циторедукция, интерферон; §3.2 алло-ТГСК; §3.3 терапия детей (табл.13)")

cohorts = [
    {"cohort_id": "C1", "disease": DISEASE, "stage": "Хроническая фаза (ХФ)",
     "resectability": None,
     "clinical_situation": "Взрослые, впервые диагностированный ХМЛ в ХФ — 1-я линия терапии ИТК",
     "ecog": None, "biomarkers": ["BCR::ABL1+ (t(9;22))", "мутации киназного домена BCR::ABL1 (выбор ИТК при смене линии)"],
     "treatment_stages": ["1-я линия"], "parent": None, "source": {"section": "3.1.2"}},
    {"cohort_id": "C2", "disease": DISEASE, "stage": "Фаза акселерации (ФА)",
     "resectability": None,
     "clinical_situation": "Взрослые: иматиниб как препарат 1-й линии; 2-я и последующие линии — ИТК2",
     "ecog": None, "biomarkers": [], "treatment_stages": ["1-я линия", "2-я и последующие линии"], "parent": None,
     "source": {"section": "3.1.2/3.1.3"}},
    {"cohort_id": "C3", "disease": DISEASE, "stage": "Бластный криз (БК)",
     "resectability": None,
     "clinical_situation": "Взрослые: иматиниб монотерапией и в комбинации с другими противоопухолевыми препаратами; дазатиниб/бозутиниб во 2-х и последующих линиях; полихимиотерапия по схемам ОЛ в комбинации с ИТК + алло-ТГСК после достижения ремиссии",
     "ecog": None, "biomarkers": ["фенотип бластов (лимфоидный/миелоидный)"], "treatment_stages": ["1-я линия", "2-я и последующие линии", "полихимиотерапия + ИТК", "алло-ТГСК"], "parent": None,
     "source": {"section": "3.1.2/3.1.9"}},
    {"cohort_id": "C4", "disease": DISEASE, "stage": "Любая фаза",
     "resectability": None,
     "clinical_situation": "Взрослые, резистентность/непереносимость ИТК2 или мутация T315I: понатиниб (ХФ/ФА/БК) и асциминиб (ХФ, неудача ≥2 ИТК или T315I); при неудаче ≥2 линий — другой ИТК или алло-ТГСК",
     "ecog": None, "biomarkers": ["мутация T315I в гене BCR::ABL1"],
     "treatment_stages": ["2-я и последующие линии"], "parent": None,
     "source": {"section": "3.1.3/3.1.8"}},
    {"cohort_id": "C5", "disease": DISEASE, "stage": None,
     "resectability": None,
     "clinical_situation": "Циторедуктивная/цитостатическая терапия: до верификации диагноза и старта ИТК, при отсутствии гематологического ответа на все ИТК, невозможности иной терапии (паллиативно)",
     "ecog": None, "biomarkers": [], "treatment_stages": ["циторедуктивная терапия"], "parent": None,
     "source": {"section": "3.1.9"}},
    {"cohort_id": "C6", "disease": DISEASE, "stage": "ХФ",
     "resectability": None,
     "clinical_situation": "Особые случаи: беременность либо непереносимость всех доступных ИТК (взрослые, ХФ) — препараты интерферона альфа-2b",
     "ecog": None, "biomarkers": [], "treatment_stages": ["терапия особых случаев"], "parent": None,
     "source": {"section": "3.1.10"}},
    {"cohort_id": "C7", "disease": DISEASE, "stage": "ХФ (дети)",
     "resectability": None,
     "clinical_situation": "Дети: 1-я линия — иматиниб (>2 лет), нилотиниб или дазатиниб (>3 лет) в режиме монотерапии",
     "ecog": None, "biomarkers": [], "treatment_stages": ["1-я линия"], "parent": None,
     "source": {"section": "3.3"}},
    {"cohort_id": "C8", "disease": DISEASE, "stage": "ФА или БК (дети)",
     "resectability": None,
     "clinical_situation": "Дети, впервые диагностированные в ФА: лечение ИТК2; в БК: ИТК2 в сочетании с ХТ по линейной принадлежности бластов (при лимфоидном БК предпочтителен дазатиниб — проникновение в ЦНС); далее алло-ТГСК",
     "ecog": None, "biomarkers": ["линейная принадлежность бластных клеток"], "treatment_stages": ["1-я линия", "ХТ + ИТК2", "алло-ТГСК"],
     "parent": None, "source": {"section": "3.3"}},
]

CITES = {
    "18": "Hoffmann V.S. et al. Systematic review and meta-analysis of standard-dose imatinib vs. high-dose imatinib",
    "20": "Talpaz M. et al. Imatinib induces durable hematologic and cytogenetic responses in patients with accelerated phase chronic myeloid leukemia",
    "25": "Hochhaus A. et al. Long-term benefits and risks of frontline nilotinib vs imatinib for chronic myeloid leukemia",
    "26": "Cortes J. et al. Final 5-Year Study Results of DASISION: The Dasatinib Versus Imatinib Study in Treatment-Naive Chronic Myeloid Leukemia Patients",
    "32": "Shah N.P. et al. Dasatinib in imatinib-resistant or -intolerant chronic-phase, chronic myeloid leukemia patients",
    "34": "Giles F.J. et al. Nilotinib in imatinib-resistant or imatinib-intolerant patients with chronic myeloid leukemia",
    "37": "Gambacorti-Passerini C. et al. Bosutinib efficacy and safety in chronic phase chronic myeloid leukemia after imatinib resistance or intolerance",
    "100": "Jorge E. Cortes et al. Bosutinib vs imatinib for newly diagnosed chronic myeloid leukemia in the BFORE trial",
    "62": "Oki Y. et al. Phase II study of low-dose decitabine in combination with imatinib mesylate in patients with CML",
    "67": "Talpaz M., Hehlmann R., Quintás-Cardama A. et al. Re-emergence of interferon-α in the treatment of chronic myeloid leukemia",
    "107": "Cortes J.E. et al. Ponatinib efficacy and safety in Philadelphia chromosome–positive leukemia: final 5-year results",
    "108": "Cortes J. et al. Ponatinib dose-ranging study in chronic-phase chronic myeloid leukemia: a randomized, open-label study",
    "109": "Hochhaus A. et al. Efficacy and Safety Results from ASCEMBL, a Multicenter, Open-Label, Phase 3 Study of Asciminib",
    "110": "Cortes J.E. et al. Asciminib, a first-in-class STAMP inhibitor, provides durable molecular response in patients with CML",
    "117": "Suttorp M, Schulze P, Glauche I, Göhring G, von Neuhoff N, et al. Front-line imatinib treatment in children and adolescents with chronic myeloid leukemia",
    "120": "Hijiya N, Maschan A, Rizzari C, Shimada H, Dufour et al. The long-term efficacy and safety of nilotinib in pediatric patients with Ph+ chronic myeloid leukemia",
    "124": "Hijiya N., Maschan A., Rizzari C., Shimada H., Dufour C., Goto H., Sosothikul D. et al. A phase 2 study of nilotinib in pediatric patients with Ph+ CML (2021)",
    "128": "Suttorp M., Metzler M. (2021). Side Effects and Sequelae of Treatment for Chronic Myeloid Leukemia in Childhood and Adolescence",
}


def cite(refs):
    return CITES.get(refs[0]) if refs else None


def row(cid, line_stage, name, drugs, refs, uur, udd, section, stage=None, special="", biom=None):
    if not stage:
        stage = "Фаза ХМЛ не указана в привязке к режиму (стадии по фазам: ХФ/ФА/БК)"
    return {
        "cohort_id": cid, "disease": DISEASE,
        "treatment": {"line_stage": line_stage, "therapy_type": ["таргетная терапия"], "regimen_name": name},
        "drugs": drugs,
        "indications": {"stage": stage, "ecog": None, "biomarkers": biom or []},
        "evidence": {"uur": uur, "udd": udd},
        "source": {"page": None, "section": section, "table": None, "references": refs, "citation": cite(refs)},
        "special_conditions": special, "maintenance_therapy": None,
    }


rows = [
    row("C1", "1-я линия, взрослые, ХФ", "#Иматиниб (монотерапия, ИТК1)",
        [{"inn": "Иматиниб", "dose": "400 мг/сут (стартовая); повышение до 600 мг/сут (+1) и 800 мг/сут (+2); снижение до 300 мг/сут при токсичности", "route": "внутрь", "schedule": "однократно во время еды, запивая полным стаканом воды", "cycle_frequency": "ежедневно", "max_cycles": "до прогрессирования / непрерывная терапия"}],
        ["18", "19"], "A", 1, "3.1.2",
        special="Абсолютных противопоказаний не зарегистрировано; осторожно при низкой ФВ сердца и низкой СКФ; при хронической токсичности 1-2 ст. возможно длительное снижение дозы при сохранении БМО"),
    row("C2", "1-я линия, взрослые, ФА и БК", "#Иматиниб (монотерапия; при БК также в комбинации с другими противоопухолевыми препаратами)",
        [{"inn": "Иматиниб", "dose": "600 мг/сут (стартовая для ФА и БК); повышение до 800 мг/сут; снижение до 400 мг/сут", "route": "внутрь", "schedule": "однократно во время еды", "cycle_frequency": "ежедневно", "max_cycles": "до прогрессирования"}],
        ["20"], "B", 2, "3.1.2"),
    row("C1", "1-я линия, взрослые, ХФ", "#Нилотиниб (монотерапия, ИТК2)",
        [{"inn": "Нилотиниб", "dose": "600 мг/сут (300 мг × 2 раза в сутки); при токсичности — 400 мг 1 раз в сутки", "route": "внутрь", "schedule": "2 раза в сутки с интервалом ~12 часов, строго натощак (не ранее чем через 2 ч после еды; пища не ранее чем через 1 ч после приема)", "cycle_frequency": "ежедневно", "max_cycles": "до прогрессирования"}],
        ["25"], "A", 2, "3.1.2",
        special="Строгие противопоказания в 1-й линии: ИБС, цереброваскулярные болезни, окклюзионные заболевания периферических артерий в анамнезе; повышенный риск при артериальной гипертензии, гиперхолестеринемии, сахарном диабете; мониторинг сердечно-сосудистой системы"),
    row("C1", "1-я линия, взрослые, ХФ", "#Дазатиниб (монотерапия, ИТК2)",
        [{"inn": "Дазатиниб", "dose": "100 мг/сут (при токсичности — 50 мг 1 раз в сутки)", "route": "внутрь", "schedule": "1 раз в сутки", "cycle_frequency": "ежедневно", "max_cycles": "до прогрессирования"}],
        ["26"], "B", 2, "3.1.2",
        special="Повышенный риск плевральных выпотов (до 37%) и редкой легочной артериальной гипертензии; строгие противопоказания в 1-й линии — плевро-пульмональные или перикардиальные заболевания в анамнезе"),
    row("C1", "1-я линия, взрослые, ХФ", "#Бозутиниб (монотерапия, ИТК2)",
        [{"inn": "Бозутиниб", "dose": "400 мг/сут (при нежелательных явлениях — 300 мг 1 раз в сутки)", "route": "внутрь", "schedule": "1 раз в сутки", "cycle_frequency": "ежедневно", "max_cycles": "до прогрессирования"}],
        ["100"], "B", 2, "3.1.2",
        special="Преходящая диарея ~30% пациентов; возможна транзиторная трансаминаземия; осторожно при тяжелом нарушении функции печени и почек"),
    row("C4", "2-я и последующие линии, взрослые (резистентность/непереносимость предшествующей терапии ИТК)", "#Нилотиниб (монотерапия)",
        [{"inn": "Нилотиниб", "dose": "800 мг/сут (400 мг × 2 раза в сутки); при токсичности — 400 мг 1 раз в сутки", "route": "внутрь", "schedule": "2 раза в сутки натощак", "cycle_frequency": "ежедневно", "max_cycles": "до прогрессирования"}],
        ["34"], "C", 4, "3.1.3",
        stage="ХФ и ФА",
        biom=["мутации киназного домена BCR::ABL1 (F317L/V/I/C, T315A, V299L чувствительны к нилотинибу)"]),
    row("C4", "2-я и последующие линии, взрослые (резистентность/непереносимость)", "#Дазатиниб (монотерапия)",
        [{"inn": "Дазатиниб", "dose": "100 мг/сут для ХФ; 140 мг/сут для ФА и БК (при токсичности — 50/100 мг соответственно)", "route": "внутрь", "schedule": "1 раз в сутки", "cycle_frequency": "ежедневно", "max_cycles": "до прогрессирования"}],
        ["32"], "B", 2, "3.1.3",
        stage="ХФ, ФА и БК",
        biom=["мутации Y253H, E255V/K, F359V/I/C чувствительны к дазатинибу"]),
    row("C4", "2-я и последующие линии, взрослые (резистентность/непереносимость)", "#Бозутиниб (монотерапия)",
        [{"inn": "Бозутиниб", "dose": "500 мг/сут (стартовая для 2+ линий); при токсичности — 400 мг или 300 мг 1 раз в сутки", "route": "внутрь", "schedule": "1 раз в сутки", "cycle_frequency": "ежедневно", "max_cycles": "до прогрессирования"}],
        ["37"], "C", 4, "3.1.3",
        stage="ХФ, ФА и БК"),
    row("C4", "Терапия после неудачи ИТК2 / при мутации T315I, взрослые (ХФ, ФА, БК)", "#Понатиниб (ИТК3)",
        [{"inn": "Понатиниб", "dose": "45 мг/сут (стартовая); при достижении ПЦО возможно снижение до 15 мг/сут; при факторах сердечно-сосудистого риска без T315I стартовая 30 мг или 15 мг/сут", "route": "внутрь", "schedule": "1 раз в сутки", "cycle_frequency": "ежедневно", "max_cycles": "до прогрессирования"}],
        ["107", "108"], "B", 2, "3.1.3",
        biom=["мутация T315I в гене BCR::ABL1"],
        special="# off-label (не зарегистрирован в РФ на момент КР); сердечно-сосудистые НЯ (артериальные окклюзии/венозные тромбозы) ~30%, дозозависимы; осторожно при атеросклеротическом поражении сосудов и тромбозах в анамнезе"),
    row("C4", "Терапия при резистентности/непереносимости ≥2 ИТК / при мутации T315I, взрослые, ХФ", "#Асциминиб (STAMP-ингибитор)",
        [{"inn": "Асциминиб", "dose": "80 мг/сут (без T315I; 80 мг 1 раз в сутки или 40 мг × 2 раза в сутки); при мутации T315I — 400 мг/сут (200 мг × 2 раза в сутки); коррекция: до 40 мг/сут (без T315I) или 160 мг × 2 раза в сутки (с T315I)", "route": "внутрь", "schedule": "1 раз в сутки или 2 раза в сутки через ~12 часов, примерно в одно время", "cycle_frequency": "ежедневно", "max_cycles": "до прогрессирования"}],
        ["109", "110"], "B", 2, "3.1.3",
        biom=["мутация T315I в гене BCR::ABL1"],
        special="# off-label; при T315I с факторами сердечно-сосудистого риска асциминиб предпочтительнее понатиниба"),
    row("C5", "Циторедуктивная и цитостатическая терапия", "#Гидроксикарбамид (моноциторедукция)",
        [{"inn": "Гидроксикарбамид", "dose": "20–30 мг/кг/сут (с учетом показателей анализа крови)", "route": "внутрь", "schedule": "регулярный ежедневный прием (при отмене уровень лейкоцитов быстро увеличивается); контроль гемограммы еженедельно", "cycle_frequency": "ежедневно", "max_cycles": None}],
        ["62"], "C", 4, "3.1.9",
        stage=None,
        special="Также применяется меркаптопурин**; при синдроме лизиса опухоли — гидратация до 2–2,5 л/м² и аллопуринол 300–600 мг/сут; при лейкостазе — лейкаферез",
        ),
    row("C3", "Полихимиотерапия при БК (в комбинации с наиболее эффективным ИТК)", "Полихимиотерапия по схемам лечения острых лейкозов (по фенотипу бластов) + ИТК",
        [{"inn": "Не конкретизировано (схемы ОЛ по линейной принадлежности бластов: лимфоидный/миелоидный/смешанный)", "dose": None, "route": None, "schedule": None, "cycle_frequency": None, "max_cycles": None},
         {"inn": "ИТК (наиболее эффективный для конкретного пациента)", "dose": "см. соответствующие режимы ИТК", "route": "внутрь", "schedule": "в комбинации с ХТ; возможна монотерапия ИТК при невозможности сочетанной терапии", "cycle_frequency": "ежедневно", "max_cycles": None}],
        ["62", "63"], "C", 4, "3.1.9",
        stage="Бластный криз",
        special="ГЭП: конкретные схемы ХТ отсылают к клиническим рекомендациям по острым лейкозам (дозы в данной КР не приведены); алло-ТГСК только после достижения гематологической ремиссии БК"),
    row("C6", "Терапия особых случаев (беременность; непереносимость всех доступных ИТК)", "#Интерферон альфа-2b (монотерапия)",
        [{"inn": "Интерферон альфа-2b", "dose": "от 3 млн МЕ через день до 6 млн МЕ ежедневно", "route": "п/к", "schedule": "по указанной шкале дозирования", "cycle_frequency": "через день — ежедневно", "max_cycles": None}],
        ["67"], "C", 4, "3.1.10",
        special="# off-label; эффективность при ФА и БК не доказана"),
    row("C7", "1-я линия, дети, ХФ", "#Иматиниб (монотерапия, дети >2 лет)",
        [{"inn": "Иматиниб", "dose": "260–340 мг/м² × 1 раз в день (максимум 600 мг)", "route": "внутрь", "schedule": "1 раз в день (допустим прием в разведенном виде — вода или яблочный сок)", "cycle_frequency": "ежедневно", "max_cycles": "длительная терапия"}],
        ["117"], "C", 4, "3.3",
        special="Существенное НЯ у детей — задержка роста (особенно в препубертатном периоде); риск гипотиреоза и эндокринной дисфункции"),
    row("C7", "1-я линия, дети, ХФ", "#Нилотиниб (монотерапия, дети)",
        [{"inn": "Нилотиниб", "dose": "230 мг/м² × 2 раза в день (максимум 400 мг на прием)", "route": "внутрь", "schedule": "2 раза в день натощак", "cycle_frequency": "ежедневно", "max_cycles": "длительная терапия"}],
        ["120"], "C", 4, "3.3",
        special="Прием дважды в день натощак может представлять проблемы применения в возрастной группе до 18 лет"),
    row("C7", "1-я линия, дети, ХФ", "#Дазатиниб (монотерапия, дети >3 лет)",
        [{"inn": "Дазатиниб", "dose": "40 мг (вес 10–20 кг), 60 мг (20–30 кг), 70 мг (30–45 кг); максимум 100 мг при весе ≥45 кг", "route": "внутрь", "schedule": "1 раз в день", "cycle_frequency": "ежедневно", "max_cycles": "длительная терапия"}],
        ["117"], "C", 4, "3.3"),
    row("C8", "1-я линия, дети, впервые диагностированные в ФА", "#Нилотиниб или #Дазатиниб (ИТК2)",
        [{"inn": "Нилотиниб", "dose": "230 мг/м² × 2 раза в сутки (макс. 400 мг × 2 раза в сутки)", "route": "внутрь", "schedule": "2 раза в сутки натощак", "cycle_frequency": "ежедневно", "max_cycles": "длительная терапия"},
         {"inn": "Дазатиниб", "dose": "по Таблице 13: 40–70 мг по массе тела (макс. 100 мг при весе ≥45 кг)", "route": "внутрь", "schedule": "1 раз в день", "cycle_frequency": "ежедневно", "max_cycles": "длительная терапия"}],
        ["124"], "C", 5, "3.3",
        special="Коррекция дозы по инструкции; при недостижении оптимального ответа — кандидат на алло-ТГСК и бридж-терапию ИТК3"),
]
# fix the accidental double-paren on асциминиб special
for r in rows:
    if r["treatment"]["regimen_name"].startswith("#Асциминиб"):
        r["special_conditions"] = r["special_conditions"].rstrip(")")

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
