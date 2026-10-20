# Build 893_1 (Опухоли невыявленной первичной локализации, ОНПЛ) — cohorts + medication regimens
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit

DOC = "893_1"
DISEASE = {
    "name": "Опухоль с невыявленной первичной локализацией (ОНПЛ)",
    "icd10": "C76–C80 (метастатическая опухоль без выявленного первичного очага)",
    "histology_type": "аденокарцинома, низкодифференцированная/недифференцированная карцинома, плоскоклеточный рак, нейроэндокринная карцинома, меланома, саркома (по морфологии метастаза)",
}

audit.event(DOC, "phase2-start", "§3 Лечение L274-433 + Таблицы 1-3 режимов ХТ + Список литературы")
audit.read_block(DOC, f"{DOC}.md", 274, 433, "§3: подтипы ОНПЛ и режимы терапии (табл.1 осевые л/у; табл.2 аденокарцинома; табл.3 плоскоклеточный рак), поддерживающая терапия")

cohorts = [
    {"cohort_id": "C1", "disease": DISEASE,
     "stage": "Метастатическое поражение лимфоузлов осевой локализации (средостенные у пациентов моложе 50 лет, забрюшинные)",
     "resectability": None,
     "clinical_situation": "Низкодифференцированная ОНПЛ с преимущественным поражением лимфоузлов осевой локализации, по течению сходная с герминогенными опухолями неблагоприятной прогностической группы",
     "ecog": None, "biomarkers": [], "treatment_stages": ["лекарственная терапия"], "parent": None,
     "source": {"section": "3, таблица 1"}},
    {"cohort_id": "C2", "disease": DISEASE,
     "stage": "Метастатическая/генерализованная ОНПЛ",
     "resectability": None,
     "clinical_situation": "Аденокарцинома неясной первичной локализации, не относящаяся к специфическим подтипам (лечение по таблице 2); полихимиотерапия оправдана только у пациентов в удовлетворительном состоянии",
     "ecog": None,
     "biomarkers": ["MSI-H", "PD-L1 TPS ≥1%", "TMB-H (≥10 mut/Mb)", "BRAF V600E", "NTRK fusion", "HER2-neu (+++)"],
     "treatment_stages": ["лекарственная терапия"], "parent": None, "source": {"section": "3, таблица 2"}},
    {"cohort_id": "C3", "disease": DISEASE,
     "stage": "Метастатическая/генерализованная ОНПЛ",
     "resectability": None,
     "clinical_situation": "Плоскоклеточный рак неясной первичной локализации, не относящийся к специфическим подтипам (лечение по таблице 3)",
     "ecog": None,
     "biomarkers": ["MSI-H", "PD-L1 TPS ≥1%", "TMB-H (≥10 mut/Mb)", "BRAF V600E", "NTRK fusion"],
     "treatment_stages": ["лекарственная терапия"], "parent": None, "source": {"section": "3, таблица 3"}},
    {"cohort_id": "C4", "disease": DISEASE,
     "stage": "Метастазы в костный мозг",
     "resectability": None,
     "clinical_situation": "ОНПЛ с метастазами в костный мозг, ECOG ≤2: противоопухолевое ЛТ (монохимиотерапия паклитакселом или антрациклинами или фторпиримидинами, еженедельные режимы, гормонотерапия, таргетная терапия) в круглосуточном стационаре; ECOG ≥3 — паллиативная помощь",
     "ecog": "ECOG ≤2", "biomarkers": [], "treatment_stages": ["монохимиотерапия/таргетная терапия"], "parent": None,
     "source": {"section": "3"}},
]

CITES = {
    "21": "Radiation Therapy for Breast Cancer in Men // American Cancer Society (источник ссылки [21] в КР)",
    "30": "Новик А.В., Гладков О.А., Имянитов Е.Н., Копп В.М., Новиков С.Н., Проценко С.А. Практические рекомендации по лекарственному лечению ОНПЛ",
    "31": "Кононенко И.Б., Снеговой А.В., Клясова Г.А. и др. Под ред. Давыдова М.И. Протоколы клинических рекомендаций: профилактика фебрильной нейтропении",
    "49": "Krämer A., Bochtler T., Pauli C., et al. Unknown primary tumours (ESMO Clinical Practice Guidelines)",
    "50": "NCCN Guidelines Version 2.2025 Occult Primary",
    "63": "Salama AKS, Li S, Macrae ER, et al. Dabrafenib and trametinib in patients with tumors with BRAFV600E mutations // J Clin Oncol",
    "64": "Doebele RC, Drilon A, Paz-Ares L, et al. Entrectinib in patients with advanced or metastatic NTRK fusion-positive solid tumours",
    "65": "Eggermont AM, Blank CU, Mandala M, et al. Adjuvant pembrolizumab versus placebo in resected stage III melanoma",
    "66": "Tanizaki J, Yonemori K, Akiyoshi K, et al. Nivolumab for TMB-high tumors",
    "67": "Meric-Bernstam F, Makker V, Oaknin A, et al. Efficacy and safety of trastuzumab deruxtecan in patients with HER2-positive solid tumors",
}


def cite(refs):
    return CITES.get(refs[0]) if refs else None


def row(cid, name, drugs, refs, uur="C", udd=5, special="", biom=None):
    return {
        "cohort_id": cid, "disease": DISEASE,
        "treatment": {"line_stage": "Системная лекарственная терапия метастатической ОНПЛ (линии по клинической ситуации)", "therapy_type": ["химиотерапия"] if not isinstance(drugs, str) else ["химиотерапия"], "regimen_name": name},
        "drugs": drugs,
        "indications": {"stage": "Диссеминированный/метастатический процесс (стадии TNM неприменимы)", "ecog": None, "biomarkers": biom or []},
        "evidence": {"uur": uur, "udd": udd},
        "source": {"page": None, "section": "3", "table": None, "references": refs, "citation": cite(refs)},
        "special_conditions": special, "maintenance_therapy": None,
    }


rows = []
# ---------- Таблица 1: низкодифференцированные ОНПЛ, осевые л/у ----------
T1 = "Таблица 1. Режимы ХТ при низкодифференцированных ОНПЛ с преимущественным поражением лимфоузлов осевой локализации"
for nm, dr, sp in [
    ("PaC (#паклитаксел/#карбоплатин)", [{"inn": "Паклитаксел", "dose": "175 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None},
                                        {"inn": "Карбоплатин", "dose": "AUC-5", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None}], ""),
    ("CarD (#доцетаксел/#карбоплатин)", [{"inn": "Доцетаксел", "dose": "65 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None},
                                         {"inn": "Карбоплатин", "dose": "AUC-6", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None}],
     "Высокий риск (>20%) фебрильной нейтропении — первичная профилактика Г-КСФ (эмпэгфилграстим 7,5 мг п/к через 24–72 ч после ХТ или филграстим 0,5 млн ЕД (5 мкг)/кг/сут п/к)"),
    ("GP (#гемцитабин/#цисплатин)", [{"inn": "Гемцитабин", "dose": "1000–1250 мг/м²", "route": "в/в", "schedule": "дни 1, 8", "cycle_frequency": "цикл 21 день", "max_cycles": None},
                                     {"inn": "Цисплатин", "dose": "75–100 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None}],
     "Возможны альтернативные варианты назначения схемы; для подтипа ОНПЛ, сходного с герминогенными опухолями, замена цисплатина на карбоплатин нежелательна"),
    ("BEP (#блеомицин/#этопозид/#цисплатин)", [{"inn": "Блеомицин", "dose": "30 мг", "route": "в/в", "schedule": "дни 1, 3, 5", "cycle_frequency": "цикл 21 день", "max_cycles": None},
                                               {"inn": "Этопозид", "dose": "100 мг/м²", "route": "в/в", "schedule": "дни 1–5", "cycle_frequency": "цикл 21 день", "max_cycles": None},
                                               {"inn": "Цисплатин", "dose": "20 мг/м²", "route": "в/в", "schedule": "дни 1–5", "cycle_frequency": "цикл 21 день", "max_cycles": None}],
     "Возможны альтернативные варианты назначения; замена цисплатина на карбоплатин нежелательна для герминогеноподобного подтипа"),
    ("EP (#этопозид/#цисплатин)", [{"inn": "Этопозид", "dose": "120 мг/м²", "route": "в/в", "schedule": "дни 1–3", "cycle_frequency": "цикл 21 день", "max_cycles": None},
                                   {"inn": "Цисплатин", "dose": "60–120 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None}],
     "Возможна замена цисплатина на карбоплатин AUC-6 с редукцией дозы этопозида до 100 мг/м² в дни 1–3"),
]:
    rows.append(row("C1", nm, dr, ["30", "50"], special=sp))
    rows[-1]["source"]["table"] = T1

# ---------- Таблица 2: аденокарцинома ----------
T2 = "Таблица 2. Режимы терапии пациентов аденокарциномой неясной первичной локализации"
for nm, dr, sp in [
    ("CarPac (#паклитаксел/#карбоплатин)", [{"inn": "Паклитаксел", "dose": "175 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None},
                                            {"inn": "Карбоплатин", "dose": "AUC 5–6", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None}], ""),
    ("PC (#паклитаксел/#карбоплатин, еженедельный)", [{"inn": "Паклитаксел", "dose": "80 мг/м²", "route": "в/в", "schedule": "дни 1, 8, 15", "cycle_frequency": "цикл 28 дней", "max_cycles": None},
                                                      {"inn": "Карбоплатин", "dose": "AUC-2", "route": "в/в", "schedule": "дни 1, 8, 15", "cycle_frequency": "цикл 28 дней", "max_cycles": None}], ""),
    ("CarD (#доцетаксел/#карбоплатин)", [{"inn": "Доцетаксел", "dose": "65 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None},
                                         {"inn": "Карбоплатин", "dose": "AUC-6", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None}],
     "Высокий риск фебрильной нейтропении — первичная профилактика Г-КСФ (эмпэгфилграстим 7,5 мг п/к через 24–72 ч после ХТ или филграстим 0,5 млн ЕД/кг/сут п/к)"),
    ("GP (#гемцитабин/#цисплатин)", [{"inn": "Гемцитабин", "dose": "1000–1250 мг/м²", "route": "в/в", "schedule": "дни 1, 8", "cycle_frequency": "цикл 21 день", "max_cycles": None},
                                     {"inn": "Цисплатин", "dose": "75 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None}],
     "Возможно разделение дозы цисплатина на дни 1 и 8 в равных долях; возможны другие модификации"),
    ("GD (#гемцитабин/#доцетаксел)", [{"inn": "Гемцитабин", "dose": "1000 мг/м²", "route": "в/в", "schedule": "дни 1, 8", "cycle_frequency": "цикл 21 день", "max_cycles": None},
                                      {"inn": "Доцетаксел", "dose": "75 мг/м²", "route": "в/в", "schedule": "день 8", "cycle_frequency": "цикл 21 день", "max_cycles": None}],
     "Назначение Г-КСФ с 9 по 15 дни"),
    ("mFOLFOX6", [{"inn": "Оксалиплатин", "dose": "85 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 14 дней", "max_cycles": None},
                  {"inn": "Кальция фолинат", "dose": "200 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 14 дней", "max_cycles": None},
                  {"inn": "Фторурацил", "dose": "400 мг/м²", "route": "в/в струйно", "schedule": "день 1", "cycle_frequency": "цикл 14 дней", "max_cycles": None},
                  {"inn": "Фторурацил", "dose": "2400 мг/м²", "route": "в/в инфузия 46–48 ч", "schedule": "день 1", "cycle_frequency": "цикл 14 дней", "max_cycles": None}],
     "Возможно отказаться от болюсного введения фторурацила"),
    ("CapeOx", [{"inn": "Оксалиплатин", "dose": "130 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None},
                {"inn": "Капецитабин", "dose": "850–1000 мг/м²", "route": "внутрь 2 раза в день", "schedule": "дни 1–14", "cycle_frequency": "цикл 21 день", "max_cycles": None}], ""),
    ("FOLFIRI", [{"inn": "Иринотекан", "dose": "180 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 14 дней", "max_cycles": None},
                 {"inn": "Кальция фолинат", "dose": "200 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 14 дней", "max_cycles": None},
                 {"inn": "Фторурацил", "dose": "400 мг/м²", "route": "в/в струйно", "schedule": "день 1", "cycle_frequency": "цикл 14 дней", "max_cycles": None},
                 {"inn": "Фторурацил", "dose": "2400 мг/м²", "route": "в/в инфузия 46–48 ч", "schedule": "день 1", "cycle_frequency": "цикл 14 дней", "max_cycles": None}],
     "Возможно отказаться от болюсного введения фторурацила"),
    ("FOLFIRINOX", [{"inn": "Оксалиплатин", "dose": "85 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 14 дней", "max_cycles": None},
                    {"inn": "Иринотекан", "dose": "180 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 14 дней", "max_cycles": None},
                    {"inn": "Кальция фолинат", "dose": "400 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 14 дней", "max_cycles": None},
                    {"inn": "Фторурацил", "dose": "400 мг/м² болюс + 2400 мг/м² инфузия 46–48 ч", "route": "в/в струйно, затем инфузия", "schedule": "день 1", "cycle_frequency": "цикл 14 дней", "max_cycles": None}],
     "Только для пациентов ECOG 0–1, возраста до 65 лет с предполагаемой первичной локализацией в органах ЖКТ; высокий риск фебрильной нейтропении — первичная профилактика Г-КСФ"),
    ("#Пембролизумаб", [{"inn": "Пембролизумаб", "dose": "2 мг/кг, 200 мг или 400 мг", "route": "в/в", "schedule": "день 1", "cycle_frequency": "каждые 3 недели / каждые 6 недель (для дозы 400 мг)", "max_cycles": None}],
     "# off-label; только при MSI-H в опухолевой ткани; во 2-й или последующих линиях лечения; при TMB-H (≥10 mut/Mb) — 200 мг в/в 1 раз каждые 3 недели"),
    ("#Ниволумаб", [{"inn": "Ниволумаб", "dose": "3 мг/кг или 240 мг (либо 480 мг)", "route": "в/в", "schedule": "день 1", "cycle_frequency": "каждые 14 дней (для 480 мг — каждые 28 дней)", "max_cycles": None}],
     "# off-label; при PD-L1 TPS ≥1% в опухолевой ткани; во 2-й или последующих линиях; при TMB (≥7,75 mut/Mb) — 240 мг в/в каждые 2 недели"),
    ("#Капецитабин (монотерапия)", [{"inn": "Капецитабин", "dose": "850–1250 мг/м²", "route": "внутрь 2 раза в день", "schedule": "дни 1–14", "cycle_frequency": "цикл 21 день", "max_cycles": None}], ""),
]:
    rows.append(row("C2", nm, dr, ["30", "50"], special=sp))
    rows[-1]["source"]["table"] = T2

# Таргетные опции (аденокарцинома, комментарии к табл. 2)
rows.append(row("C2", "#Дабрафиниб + #траметиниб",
                [{"inn": "Дабрафиниб", "dose": "150 мг", "route": "внутрь", "schedule": "2 раза в день", "cycle_frequency": "ежедневно", "max_cycles": None},
                 {"inn": "Траметиниб", "dose": "2 мг", "route": "внутрь", "schedule": "1 раз в день, каждые 4 недели циклом", "cycle_frequency": "ежедневно", "max_cycles": None}],
                ["63"], biom=["мутация BRAF V600E"],
                special="# off-label; для нерезектабельных/метастатических солидных опухолей с мутацией BRAF V600E, прогрессировавших после предшествующего лечения, без эффективных альтернатив"))
rows.append(row("C2", "#Энтректиниб или #ларотректиниб",
                [{"inn": "Энтректиниб", "dose": "600 мг", "route": "внутрь 1 раз в день", "schedule": "ежедневно", "cycle_frequency": "ежедневно", "max_cycles": None},
                 {"inn": "Ларотректиниб", "dose": "100 мг", "route": "внутрь 2 раза в день", "schedule": "ежедневно", "cycle_frequency": "ежедневно", "max_cycles": None}],
                ["64"], biom=["слияние гена NTRK"],
                special="# off-label; только при метастатических солидных опухолях со слиянием NTRK, когда отсутствуют эффективные альтернативные методы"))
rows.append(row("C2", "#Трастузумаб-дерукстекан",
                [{"inn": "Трастузумаб-дерукстекан", "dose": "5,4 мг/кг", "route": "в/в", "schedule": "день 1", "cycle_frequency": "1 раз в 21 день", "max_cycles": None}],
                ["67"], biom=["гиперэкспрессия HER2-neu (+++)"],
                special="# off-label; во 2-й или последующих линиях лечения"))

# ---------- Таблица 3: плоскоклеточный рак ----------
T3 = "Таблица 3. Режимы терапии пациентов плоскоклеточным раком неясной первичной локализации"
for nm, dr, sp in [
    ("PCF (#паклитаксел/#цисплатин/#фторурацил)", [{"inn": "Паклитаксел", "dose": "175 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None},
                                                   {"inn": "Цисплатин", "dose": "100 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None},
                                                   {"inn": "Фторурацил", "dose": "500 мг/м²/сут", "route": "в/в 24-часовая инфузия", "schedule": "дни 1–5", "cycle_frequency": "цикл 21 день", "max_cycles": None}],
     "Рассмотреть назначение Г-КСФ согласно протоколам профилактики фебрильной нейтропении"),
    ("DCF (#доцетаксел/#цисплатин/#фторурацил)", [{"inn": "Доцетаксел", "dose": "75 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None},
                                                  {"inn": "Цисплатин", "dose": "75 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None},
                                                  {"inn": "Фторурацил", "dose": "750 мг/м²/сут", "route": "в/в 24-часовая инфузия", "schedule": "дни 1–5", "cycle_frequency": "цикл 21 день", "max_cycles": None}],
     "Высокий риск фебрильной нейтропении — первичная профилактика Г-КСФ (эмпэгфилграстим 7,5 мг п/к через 24–72 ч после ХТ или филграстим 0,5 млн ЕД/кг/сут п/к)"),
    ("mFOLFOX6", [{"inn": "Оксалиплатин", "dose": "85 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 14 дней", "max_cycles": None},
                  {"inn": "Кальция фолинат", "dose": "200 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 14 дней", "max_cycles": None},
                  {"inn": "Фторурацил", "dose": "400 мг/м² болюс + 2400 мг/м² инфузия 46–48 ч", "route": "в/в струйно, затем инфузия", "schedule": "день 1", "cycle_frequency": "цикл 14 дней", "max_cycles": None}],
     "Возможно отказаться от болюсного введения фторурацила"),
    ("GP (#гемцитабин/#цисплатин)", [{"inn": "Гемцитабин", "dose": "1000–1250 мг/м²", "route": "в/в", "schedule": "дни 1, 8", "cycle_frequency": "цикл 21 день", "max_cycles": None},
                                     {"inn": "Цисплатин", "dose": "75 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None}], ""),
    ("PC (#паклитаксел/#цисплатин)", [{"inn": "Паклитаксел", "dose": "175 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None},
                                     {"inn": "Цисплатин", "dose": "60 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None}], ""),
    ("PF (#цисплатин/#фторурацил)", [{"inn": "Цисплатин", "dose": "20 мг/м²", "route": "в/в", "schedule": "дни 1–5", "cycle_frequency": "цикл 28 дней", "max_cycles": None},
                                     {"inn": "Фторурацил", "dose": "700 мг/м²/сут", "route": "в/в 24-часовая инфузия", "schedule": "дни 1–5", "cycle_frequency": "цикл 28 дней", "max_cycles": None}], ""),
    ("DC (#доцетаксел/#цисплатин)", [{"inn": "Доцетаксел", "dose": "75 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None},
                                     {"inn": "Цисплатин", "dose": "75 мг/м²", "route": "в/в", "schedule": "день 1", "cycle_frequency": "цикл 21 день", "max_cycles": None}], ""),
    ("#Пембролизумаб", [{"inn": "Пембролизумаб", "dose": "2 мг/кг, 200 мг или 400 мг", "route": "в/в", "schedule": "день 1", "cycle_frequency": "каждые 21/42 дня соответственно", "max_cycles": None}],
     "# off-label; только при MSI-H; во 2-й или последующих линиях; при TMB-H (≥10 mut/Mb) — 200 мг в/в каждые 3 недели"),
    ("#Ниволумаб", [{"inn": "Ниволумаб", "dose": "3 мг/кг или 240 мг (либо 480 мг)", "route": "в/в", "schedule": "день 1", "cycle_frequency": "каждые 14 дней (480 мг — каждые 28 дней)", "max_cycles": None}],
     "# off-label; при PD-L1 TPS ≥1%; во 2-й или последующих линиях; при TMB (≥7,75 mut/Mb) — 240 мг в/в каждые 2 недели"),
    ("#Капецитабин (монотерапия)", [{"inn": "Капецитабин", "dose": "850–1250 мг/м²", "route": "внутрь 2 раза в день", "schedule": "дни 1–14", "cycle_frequency": "цикл 21 день", "max_cycles": None}], ""),
    ("#Капецитабин + лучевая терапия (ХЛТ)", [{"inn": "Капецитабин", "dose": "625–825 мг/м²", "route": "внутрь 2 раза в день", "schedule": "с 1-го по 5-й или с 1-го по 7-й дни лучевой терапии", "cycle_frequency": "ежедневно в течение 5 недель ЛТ", "max_cycles": None}],
     "Радиомодифицирующая доза капецитабина; ЛТ еженедельно — 5 недель"),
    ("Roswell Park режим (#кальция фолинат/#фторурацил)", [{"inn": "Кальция фолинат", "dose": "500 мг/м²", "route": "в/в", "schedule": "дни 1, 8, 15, 22, 29, 36", "cycle_frequency": "повтор каждые 8 недель", "max_cycles": None},
                                                           {"inn": "Фторурацил", "dose": "500 мг/м²", "route": "в/в", "schedule": "дни 1, 8, 15, 22, 29, 36", "cycle_frequency": "повтор каждые 8 недель", "max_cycles": None}],
     "Возможно назначение без кальция фолината"),
    ("Инфузионные режимы #фторурацила (с кальция фолинатом)", [{"inn": "Кальция фолинат", "dose": "варианты: 400 мг/м², либо 20 мг/м² еженедельно, либо 500 мг/м² еженедельно", "route": "в/в", "schedule": "день 1 цикла", "cycle_frequency": "повтор каждые 14 дней или еженедельно", "max_cycles": None},
                                                               {"inn": "Фторурацил", "dose": "варианты: 400 мг/м² болюс + 2400 мг/м² 46–48 ч; либо 500 мг/м² болюс еженедельно; либо 2600 мг/м² 24 ч еженедельно", "route": "в/в болюс / инфузия (помпа)", "schedule": "день 1 цикла", "cycle_frequency": "каждые 14 дней или еженедельно", "max_cycles": None}],
     "Возможно назначение без кальция фолината"),
]:
    rows.append(row("C3", nm, dr, ["30", "50"], special=sp))
    rows[-1]["source"]["table"] = T3

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
