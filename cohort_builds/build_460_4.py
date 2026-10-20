# -*- coding: utf-8 -*-
"""Build cohorts + medication regimens for doc 460_4 (рак тела матки и саркомы матки)."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit  # noqa: E402

DOC = "460_4"

DISEASE = {
    "name": "Злокачественные новообразования тела матки и саркомы матки",
    "icd10": "C54 (C54.0–C54.9), C55 (матка неуточненной локализации); D07.0 — карцинома эндометрия in situ",
    "histology_type": "карциномы эндометрия: эндометриоидная аденокарцинома (наиболее частая), серозный, светлоклеточный, муцинозный рак, карциносаркома; саркомы матки: лейомиосаркома, эндометриальная стромальная саркома, недифференцированная саркома матки",
}

GCSF = ("по показаниям первичная или вторичная профилактика нейтропении Г-КСФ: филграстим 5 мкг/кг п/к через 24–72 ч после ХТ либо эмпэгфилграстим 7,5 мг п/к однократно")

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
        "source": {"page": None, "section": "3.4", "table": None,
                   "references": refs or [], "citation": cite},
        "special_conditions": special,
        "maintenance_therapy": maint,
    }

cohorts = [
    {"cohort_id": "C1", "disease": DISEASE,
     "stage": "РТМ III–IV стадий и неэндометриоидный РТМ всех стадий (кроме муцинозного) после циторедуктивной операции",
     "resectability": "оперированный (циторедуктивная операция)", "clinical_situation": "адъювантная/системная ХТ",
     "ecog": None, "biomarkers": ["HER2/neu-статус (для серозного РТМ)", "MSI/MMR-статус"],
     "treatment_stages": ["6 курсов ХТ; начинать не позднее 4 недель после операции"], "source": {"section": "3.4"}},
    {"cohort_id": "C2", "disease": DISEASE,
     "stage": "прогрессирование/диссеминация РТМ (первичная распространённость)",
     "resectability": None, "clinical_situation": "1-я линия ХТ прогрессирования",
     "ecog": None, "biomarkers": ["HER2/neu (серозный подтип)", "MSI/MMR"],
     "treatment_stages": ["6 курсов ХТ или до прогрессирования/непереносимой токсичности; комбинации на основе платины и таксанов"], "source": {"section": "3.4"}},
    {"cohort_id": "C3", "disease": DISEASE,
     "stage": "рецидив высокодифференцированной эндометриоидной аденокарциномы РТМ при малых объёмах опухоли и индолентном течении",
     "resectability": None, "clinical_situation": "гормональная терапия рецидива",
     "ecog": None, "biomarkers": ["рецепторы стероидных гормонов (гормонопозитивный РТМ)"],
     "treatment_stages": ["гормональная терапия до прогрессирования или непереносимой токсичности"], "source": {"section": "3.4"}},
    {"cohort_id": "C4", "disease": DISEASE,
     "stage": "лейомиосаркома матки высокой степени злокачественности, эндометриальная стромальная саркома матки высокой степени злокачественности и недифференцированная саркома матки всех стадий",
     "resectability": None, "clinical_situation": "ХТ сарком матки",
     "ecog": None, "biomarkers": [],
     "treatment_stages": ["ХТ (после радикального хирургического лечения или при диссеминации)"], "source": {"section": "3.4"}},
    {"cohort_id": "C5", "disease": DISEASE,
     "stage": "диссеминированные формы эндометриальной стромальной саркомы матки низкой степени злокачественности и гормонопозитивная лейомиосаркома матки",
     "resectability": None, "clinical_situation": "гормональная терапия сарком матки",
     "ecog": None, "biomarkers": ["гормонопозитивность (рецепторы стероидных гормонов)"],
     "treatment_stages": ["гормональная терапия до прогрессирования или непереносимой токсичности"], "source": {"section": "3.4"}},
    {"cohort_id": "C6", "disease": DISEASE,
     "stage": "прогрессирование РТМ после 1-й линии ХТ",
     "resectability": None, "clinical_situation": "2-я линия ХТ",
     "ecog": None, "biomarkers": ["MSI-H/dMMR", "все гистологические типы, кроме карциносаркомы (для пембролизумаб+ленватиниб)"],
     "treatment_stages": ["6 курсов ХТ или до прогрессирования/непереносимой токсичности; при рецидиве >6 мес после первичного лечения возможен повтор 1-й линии"], "source": {"section": "3.4"}},
    {"cohort_id": "C7", "disease": DISEASE,
     "stage": "прогрессирование лейомиосаркомы, эндометриальной стромальной саркомы матки высокой степени злокачественности и недифференцированной саркомы матки",
     "resectability": None, "clinical_situation": "терапия прогрессирования сарком матки",
     "ecog": None, "biomarkers": ["pan-NTRK перестройка гена NTRK (NTRK-ингибиторы)"],
     "treatment_stages": ["монохимиотерапия или неиспользованные режимы 1-й линии"], "source": {"section": "3.4"}},
]

R = []
# ---------- C1: адъювантная ХТ ----------
adj_line = "адъювантная/системная химиотерапия (РТМ III–IV и неэндометриоидный РТМ)"
adj_stage = "РТМ III–IV стадий; неэндометриоидный РТМ всех стадий (кроме муцинозного), после циторедуктивной операции"
R += [
    base("C1", adj_line, ["химиотерапия"], "Паклитаксел + карбоплатин",
         [drug("Паклитаксел", "175 мг/м²", "в/в", "1-й день", "каждые 3 недели", 6),
          drug("Карбоплатин", "AUC 5–6", "в/в", "1-й день", "каждые 3 недели", 6)],
         adj_stage, uur="C", udd=5, refs=["64", "146"],
         cite="Michener C.M., Peterson G., Kulp B. et al. Carboplatin plus paclitaxel in the treatment of advanced or recurrent endometrial carcinoma. J Cancer Res Clin Oncol 2005;131(9):58",
         special="# off-label (** ЖНВЛП у паклитаксела); " + GCSF),
    base("C1", adj_line, ["химиотерапия"], "Паклитаксел + цисплатин",
         [drug("Паклитаксел", "175 мг/м²", "в/в", "1-й день", "каждые 3 недели", 6),
          drug("Цисплатин", "60–75 мг/м²", "в/в", "1-й день", "каждые 3 недели", 6)],
         adj_stage, uur="C", udd=5, refs=["62", "65", "66", "146", "193"],
         cite="Nomura H., Aoki D., Michimae H. et al. Effect of taxane plus platinum regimens vs doxorubicin plus cisplatin as adjuvant chemotherapy for endometrial cancer at a high risk of progression",
         special="# off-label (** ЖНВЛП); " + GCSF),
]

# ---------- C2: 1L прогрессирования РТМ ----------
l1_line = "1-я линия ХТ прогрессирования РТМ"
l1_stage = "прогрессирование/диссеминация РТМ"
R += [
    base("C2", l1_line, ["химиотерапия"], "Паклитаксел + цисплатин",
         [drug("Паклитаксел", "175 мг/м²", "в/в", "3 ч, 1-й день", "каждые 3 недели", "6 курсов или до прогрессирования/непереносимой токсичности"),
          drug("Цисплатин", "60 или 75 мг/м²", "в/в", "2 ч, 1-й день", "каждые 3 недели", "6 курсов или до прогрессирования/непереносимой токсичности")],
         l1_stage, uur="C", udd=2, refs=["65", "66", "114"],
         cite="Dimopoulos M.A., Papadimitriou C.A., Georgoulias V. et al. Paclitaxel and cisplatin in advanced or recurrent carcinoma of the endometrium: long-term results of a phase II multicenter study",
         special="# off-label (** ЖНВЛП); схема выбора — комбинация на основе платины и таксана; " + GCSF),
    base("C2", l1_line, ["химиотерапия"], "Паклитаксел + карбоплатин",
         [drug("Паклитаксел", "175 мг/м²", "в/в", "3 ч, 1-й день", "каждые 3 недели", "6 курсов или до прогрессирования/непереносимой токсичности"),
          drug("Карбоплатин", "AUC 5–6", "в/в", "1 ч, 1-й день", "каждые 3 недели", "6 курсов или до прогрессирования/непереносимой токсичности")],
         l1_stage, uur="C", udd=2, refs=["64", "70", "114"],
         cite="Michener C.M., Peterson G., Kulp B. et al. Carboplatin plus paclitaxel in the treatment of advanced or recurrent endometrial carcinoma. J Cancer Res Clin Oncol 2005;131(9):58",
         special="# off-label (** ЖНВЛП); схема выбора — комбинация на основе платины и таксана; " + GCSF),
    base("C2", l1_line, ["химиотерапия"], "Доксорубицин + цисплатин",
         [drug("Доксорубицин", "50–60 мг/м²", "в/в", "1-й день", "каждые 3 недели"),
          drug("Цисплатин", "50–75 мг/м²", "в/в", "1-й день", "каждые 3 недели")],
         l1_stage, uur="C", udd=2, refs=["62", "63", "146"],
         cite="Fleming G.F., Filiaci V.L., Bentley R.C. et al. Phase III randomized trial of doxorubicin + cisplatin versus doxorubicin + 24-h paclitaxel + filgrastim in endometrial carcinoma",
         special="** ЖНВЛП у доксорубицина"),
    base("C2", l1_line, ["химиотерапия", "таргетная терапия"], "Паклитаксел + карбоплатин + трастузумаб",
         [drug("Паклитаксел", "175 мг/м²", "в/в", "3 ч, 1-й день", "каждые 3 недели"),
          drug("Карбоплатин", "AUC 5–6", "в/в", "1 ч, 1-й день", "каждые 3 недели"),
          drug("Трастузумаб", "8 мг/кг в 1-е введение, далее 6 мг/кг", "в/в", "30–90 мин", "каждые 3 недели")],
         l1_stage, bio=["HER2/neu-позитивный серозный рак эндометрия"],
         uur="C", udd=2, refs=["61", "146"],
         cite="Fader A.N., Roque D.M., Siegel E. et al. Randomized phase II trial of carboplatin-paclitaxel versus carboplatin-paclitaxel-trastuzumab in uterine serous carcinomas that overexpress HER2/neu",
         special="** ЖНВЛП; только для пациенток с HER2/neu-позитивным серозным РТМ; " + GCSF),
    base("C2", l1_line, ["химиотерапия", "иммунотерапия"], "Паклитаксел + карбоплатин + пембролизумаб",
         [drug("Паклитаксел", "175 мг/м²", "в/в", "3 ч, 1-й день", "каждые 3 недели"),
          drug("Карбоплатин", "AUC 5–6", "в/в", "1 ч, 1-й день", "каждые 3 недели"),
          drug("Пембролизумаб", "200 мг или 400 мг", "в/в", "капельно 30 мин; 200 мг каждые 3 нед или 400 мг каждые 6 нед", "каждые 3 или 6 недель", "до 2 лет либо до прогрессирования/непереносимой токсичности")],
         l1_stage, bio=["MSI/нарушения MMR в опухоли"],
         uur="C", udd=2, refs=["186", "146", "193"],
         cite="Eskander R.N., Sill M.W. et al. Pembrolizumab plus Chemotherapy in Advanced Endometrial Cancer. N Engl J Med 2023;388(23):2159-2170",
         special="** ЖНВЛП; назначается в течение 2 лет либо до прогрессирования/непереносимой токсичности; " + GCSF),
]

# ---------- C3: гормональная терапия рецидива РТМ ----------
hormone_drug = lambda inn, dose, refs: base(
    "C3", "гормональная терапия рецидива РТМ", ["гормональная терапия"], f"{inn} монотерапия",
    [drug(inn, dose, "внутрь", "ежедневно", "ежедневно", "до прогрессирования или непереносимой токсичности")],
    "рецидив высокодифференцированной эндометриоидной аденокарциномы РТМ, малые объёмы опухоли, индолентное течение",
    bio=["рецепторы стероидных гормонов"], uur="B", udd=2, refs=refs, cite=None,
    special="** ЖНВЛП у части препаратов; цитация [146] не разрешается по списку литературы (номер пропущен в документе)")
hormone_drug.__name__ = "x"
def hrow(inn, dose, refs, extra_cite=None):
    r = hormone_drug(inn, dose, refs)
    if extra_cite:
        r["source"]["citation"] = extra_cite
        r["special_conditions"] = "** ЖНВЛП у части препаратов"
    return r
R += [
    hrow("Медроксипрогестерон", "500 мг/сут", ["146"]),
    hrow("Тамоксифен", "20 мг 1 раз в сутки", ["146"]),
    hrow("Летрозол", "2,5 мг/сут", ["81"], "Barker L.C., Brand I.R., Crawford S.M. Sustained effect of the aromatase inhibitors anastrozole and letrozole on endometrial thickness in patients with endometrial hyperplasia"),
    hrow("Анастрозол", "1 мг/сут", ["81"], "Barker L.C., Brand I.R., Crawford S.M. Sustained effect of the aromatase inhibitors anastrozole and letrozole on endometrial thickness in patients with endometrial hyperplasia"),
    hrow("Эксеместан", "25 мг/сут", ["82"], "Lindemann K., Malander S., Christensen R.D. et al. Examestane in advanced or recurrent endometrial carcinoma: a prospective phase II study by the Nordic Society of Gynecologic Oncology"),
]

# ---------- C4: ХТ сарком матки ----------
sar_stage = "лейомиосаркома / ЭСС высокой степени ЗО / недифференцированная саркома матки"
R += [
    base("C4", "химиотерапия сарком матки", ["химиотерапия"], "Доксорубицин монотерапия",
         [drug("Доксорубицин", "60–75 мг/м²", "в/в струйно", None, "каждые 3 недели")],
         sar_stage, uur="C", udd=2, refs=["89"],
         cite="Judson I., Verweij J., Gelderblom H. et al. Doxorubicin alone versus intensified doxorubicin plus ifosfamide for first-line treatment of advanced or metastatic soft-tissue sarcoma",
         special="** ЖНВЛП; режим предпочтителен для лейомиосаркомы матки, возможно назначение ослабленным пациенткам"),
    base("C4", "химиотерапия сарком матки", ["химиотерапия"], "Гемцитабин + доцетаксел",
         [drug("Гемцитабин", "900 мг/м² (после ЛТ малого таза/ранее проведённой ХТ возможна стартовая редукция до 675 мг/м²)", "в/в", "90 мин, 1-й и 8-й дни"),
          drug("Доцетаксел", "100 мг/м² (редукция до 75 мг/м²)", "в/в", "1 ч, 8-й день")],
         sar_stage, uur="C", udd=2, refs=["90"],
         cite="Hensley M.L., Maki R., Venkatraman E. et al. Gemcitabine and docetaxel in patients with unresectable leiomyosarcoma: results of a phase II trial. J Clin Oncol 2002",
         special="# off-label (** ЖНВЛП); филграстим 150 мкг/м² п/к с 9-го по 15-й дни или эмпэгфилграстим 7,5 мг п/к однократно"),
    base("C4", "химиотерапия сарком матки", ["химиотерапия"], "Доксорубицин + ифосфамид (+ месна)",
         [drug("Доксорубицин", "75 мг/м²", "в/в", "72-часовая инфузия"),
          drug("Ифосфамид", "2500 мг/м²/сут", "в/в", "3-часовая инфузия, 1–4-й дни", "каждые 3 недели"),
          drug("Месна", "из расчёта 100% от дозы ифосфамида", "в/в", "одновременно с ифосфамидом, 1–4 дни", "каждые 3 недели")],
         sar_stage, uur="C", udd=2, refs=["84", "146"],
         cite="Sutton G., Blessing J.A., Malfetano J.H. Ifosfamide and doxorubicin in the treatment of advanced leiomyosarcomas of the uterus: a Gynecologic Oncology Group study",
         special="** ЖНВЛП у месны; филграстим 5 мкг/кг п/к 5–15 дни либо эмпэгфилграстим 7,5 мг п/к однократно"),
    base("C4", "химиотерапия сарком матки", ["химиотерапия"], "Доксорубицин + дакарбазин",
         [drug("Доксорубицин", "60 мг/м²", "в/в", "1-й день", "каждые 3 недели"),
          drug("Дакарбазин", "750 мг/м²", "в/в", "96-часовая инфузия (растворяется вместе с доксорубицином)", "каждые 3 недели")],
         sar_stage, uur="C", udd=2, refs=["85"],
         cite="Zalupski M., Metch B., Balcerzak S. et al. Phase III comparison of doxorubicin and dacarbazine given by bolus versus infusion in patients with soft-tissue sarcomas",
         special="# off-label (** ЖНВЛП у дакарбазина)"),
]

# ---------- C5: гормональная терапия сарком ----------
def s_horm(inn, dose, route, schedule, refs):
    return base("C5", "гормональная терапия сарком матки (диссеминированные формы)", ["гормональная терапия"],
                f"{inn} монотерапия",
                [drug(inn, dose, route, schedule, None, "до прогрессирования или непереносимой токсичности")],
                "диссеминированная ЭСС низкой степени злокачественности / гормонопозитивная лейомиосаркома матки",
                bio=["гормонопозитивность"], uur="B", udd=2, refs=refs, cite=None,
                special=f"** ЖНВЛП у части препаратов; цитацию [{refs[0]}] не удалось разрешить по библиографии" if refs == ["146"] else "** ЖНВЛП у части препаратов")
R += [
    s_horm("Летрозол", "2,5 мг/сут", "внутрь", "ежедневно", ["77"]),
    s_horm("Анастрозол", "1 мг/сут", "внутрь", "ежедневно", ["77"]),
    s_horm("Эксеместан", "25 мг/сут", "внутрь", "ежедневно", ["82"]),
    s_horm("Медроксипрогестерон", "500 мг/сут", "внутрь", "ежедневно", ["146"]),
    s_horm("Гозерелин", "3,6 мг", "внутримышечно", "1 раз в 28 дней", ["77"]),
    s_horm("Бусерелин", "3,75 мг", "внутримышечно", "1 раз в 28 дней", ["146"]),
    s_horm("Лейпрорелин", "3,75 мг", "внутримышечно", "1 раз в 28 дней", ["77"]),
]

# ---------- C6: 2L РТМ ----------
l2_line = "2-я линия ХТ прогрессирования РТМ"
l2_stage = "прогрессирование РТМ после 1-й линии ХТ"
unres146 = "цитация [146] не разрешается по списку литературы (номер пропущен в документе)"
R += [
    base("C6", l2_line, ["иммунотерапия"], "Пембролизумаб монотерапия",
         [drug("Пембролизумаб", "200 мг или 400 мг", "в/в", "капельно 30 мин; 200 мг каждые 3 нед или 400 мг каждые 6 нед", "каждые 3 или 6 недель", "6 курсов или до прогрессирования/непереносимой токсичности")],
         l2_stage, bio=["высокий уровень микросателлитной нестабильности (MSI-H), включая нарушения системы репарации ДНК (dMMR) в опухоли"],
         uur="C", udd=3, refs=["99", "146"],
         cite="Marabelle A., Le D.T., Ascierto P.A. et al. Efficacy of pembrolizumab in patients with noncolorectal high microsatellite instability/mismatch repair-deficient cancer",
         special="** ЖНВЛП; только при MSI-H/dMMR"),
    base("C6", l2_line, ["иммунотерапия", "таргетная терапия"], "Пембролизумаб + ленватиниб",
         [drug("Пембролизумаб", "200 мг или 400 мг", "в/в", "капельно 30 мин; 200 мг каждые 3 нед или 400 мг каждые 6 нед", "каждые 3 или 6 недель", "до прогрессирования/непереносимой токсичности"),
          drug("Ленватиниб", "20 мг 1 раз в сутки", "внутрь", "ежедневно", "ежедневно", "до прогрессирования/непереносимой токсичности")],
         l2_stage, bio=["отсутствие MSI-H/dMMR в опухоли", "все гистологические типы, кроме карциносаркомы"],
         uur="C", udd=3, refs=["100", "146"],
         cite="Makker V., Rasco D., Vogelzang N.J. et al. Lenvatinib plus pembrolizumab in patients with advanced endometrial cancer: an interim analysis of a multicentre, open-label, single-arm, phase 2 trial",
         special="** ЖНВЛП; при отсутствии высокого уровня MSI-H/dMMR"),
    base("C6", l2_line, ["химиотерапия"], "Топотекан монотерапия",
         [drug("Топотекан", "1,0–1,25 мг/м²", "в/в", "1–5-й дни", "каждые 3 недели", "до прогрессирования/непереносимой токсичности")],
         l2_stage, uur="C", udd=3, refs=["91"],
         cite="Miller D.S., Blessing J.A., Lentz S.S., Waggoner S.E. A phase II trial of topotecan in patients with advanced, persistent, or recurrent endometrial carcinoma",
         special="# off-label; " + GCSF),
    base("C6", l2_line, ["химиотерапия"], "Паклитаксел монотерапия",
         [drug("Паклитаксел", "135 мг/м² в 1-й день или 60–80 мг/м² в 1, 8 и 15-й дни", "в/в", None, "каждые 3 недели", "до прогрессирования/непереносимой токсичности")],
         l2_stage, uur="C", udd=3, refs=["95", "96", "97", "98", "146"],
         cite="Lincoln S., Blessing J.A., Lee R.B., Rocereto T.F. Activity of paclitaxel as second-line chemotherapy in endometrial carcinoma: a Gynecologic Oncology Group study",
         special="** ЖНВЛП; если ранее проводилась ДЛТ — редукция дозы на 20%"),
    base("C6", l2_line, ["химиотерапия"], "Оксалиплатин монотерапия",
         [drug("Оксалиплатин", "130 мг/м²", "в/в", "2 ч", "каждые 3 недели", "до прогрессирования/непереносимой токсичности")],
         l2_stage, uur="C", udd=3, refs=["94"],
         cite="Fracasso P.M., Blessing J.A., Molpus K.L. et al. Phase II study of oxaliplatin as second-line chemotherapy in endometrial carcinoma: a Gynecologic Oncology Group study",
         special="# off-label; если ранее проводилась ДЛТ — редукция дозы на 20% (общее правило для паклитаксела/ифосфамида/гемцитабина)"),
    base("C6", l2_line, ["химиотерапия"], "Доксорубицин пегилированный липосомальный",
         [drug("Доксорубицин (пегилированный липосомальный)", "40–50 мг/м²", "в/в", None, "каждые 4 недели", "до прогрессирования/непереносимой токсичности")],
         l2_stage, uur="C", udd=3, refs=["93", "102", "146"],
         cite="Escobar P.F., Markman M., Zanotti K. et al. Phase 2 trial of pegylated liposomal doxorubicin in advanced endometrial cancer. J Cancer Res Clin Oncol 2003;129(11):65",
         special="# off-label"),
    base("C6", l2_line, ["химиотерапия"], "Доксорубицин монотерапия",
         [drug("Доксорубицин", "50 мг/м²", "в/в", None, "каждые 4 недели", "до прогрессирования/непереносимой токсичности")],
         l2_stage, uur="C", udd=3, refs=["146"], cite=None,
         special="** ЖНВЛП; " + unres146),
    base("C6", l2_line, ["химиотерапия"], "Доцетаксел монотерапия",
         [drug("Доцетаксел", "75 мг/м²", "в/в", None, "каждые 3 недели", "до прогрессирования/непереносимой токсичности")],
         l2_stage, uur="C", udd=3, refs=["146"], cite=None,
         special="** ЖНВЛП; " + unres146),
    base("C6", l2_line, ["таргетная терапия"], "Бевацизумаб монотерапия",
         [drug("Бевацизумаб", "7,5 мг/кг или 15 мг/кг", "в/в", None, "каждые 3 недели", "до прогрессирования/непереносимой токсичности")],
         l2_stage, uur="C", udd=3, refs=["92", "146"],
         cite="Dizon D.S. Treatment options for advanced endometrial carcinoma. Gynecol Oncol 2010;117(2):373-81",
         special="** ЖНВЛП; # off-label"),
    base("C6", l2_line, ["химиотерапия"], "Гемцитабин монотерапия",
         [drug("Гемцитабин", "800 мг/м²", "в/в", "1, 8, 15-й дни", "каждые 4 недели", "до прогрессирования/непереносимой токсичности")],
         l2_stage, uur="C", udd=3, refs=["146"], cite=None,
         special="** ЖНВЛП; # off-label; " + unres146),
]

# ---------- C7: прогрессирование сарком ----------
sarc_line = "терапия прогрессирования сарком матки"
sarc_stage = "прогрессирование лейомиосаркомы / ЭСС высокой степени ЗО / недифференцированной саркомы матки"
sarc_cond_prog = "применяют при прогрессировании на фоне цитостатической терапии"
R += [
    base("C7", sarc_line, ["химиотерапия"], "Дакарбазин монотерапия",
         [drug("Дакарбазин", "1200 мг/м²", "в/в", "20–30 мин", "каждые 3 недели", 8)],
         sarc_stage, uur="C", udd=2, refs=["110"],
         cite="Blay J.Y., Bauer S. et al. Eribulin versus dacarbazine in patients with leiomyosarcoma: subgroup analysis from a phase 3, open-label, randomised study",
         special="# off-label"),
    base("C7", sarc_line, ["химиотерапия"], "Гемцитабин монотерапия",
         [drug("Гемцитабин", "1000 мг/м²", "в/в", "1, 8, 15-й дни", "каждые 4 недели")],
         sarc_stage, uur="C", udd=2, refs=["86", "87", "111", "112"],
         cite="Garcia-Del-Muro X., Lopez-Pousa A., Maurel J. et al. Randomized phase II study comparing gemcitabine plus dacarbazine versus dacarbazine alone in patients with previously treated soft tissue sarcoma",
         special="** ЖНВЛП; # off-label"),
    base("C7", sarc_line, ["химиотерапия"], "Гемцитабин + дакарбазин",
         [drug("Гемцитабин", "1800 мг/м² (скорость инфузии 10 мг/м²/мин или в течение 3 часов)", "в/в", "капельно, 1-й день", "каждые 14 дней"),
          drug("Дакарбазин", "500 мг/м²", "в/в", "капельно, 1-й день", "каждые 14 дней")],
         sarc_stage, uur="C", udd=2, refs=["188"],
         cite="García-Del-Muro X., López-Pousa A. et al. Spanish Group for Research on Sarcomas. Randomized phase II study comparing gemcitabine plus dacarbazine versus dacarbazine alone",
         special="** ЖНВЛП; # off-label"),
    base("C7", sarc_line, ["химиотерапия"], "Эпирубицин монотерапия",
         [drug("Эпирубицин", "75 мг/м²", "в/в струйно", None, "каждые 3 недели")],
         sarc_stage, uur="C", udd=2, refs=["103", "112", "146"],
         cite="Mouridsen H.T., Bastholt L., Somers R. et al. Adriamycin versus epirubicin in advanced soft tissue sarcomas. A randomized phase II/phase III study of the EORTC Soft Tissue and Bone Sarcoma Group",
         special="# off-label"),
    base("C7", sarc_line, ["химиотерапия"], "Доксорубицин монотерапия",
         [drug("Доксорубицин", "50–60 мг/м²", "в/в", "1 ч", "каждые 3 недели")],
         sarc_stage, uur="C", udd=2, refs=["113"],
         cite="Temkin S.M., Fleming G. Current treatment of metastatic endometrial cancer. Cancer Control 2009;16(1):38",
         special="** ЖНВЛП"),
    base("C7", sarc_line, ["таргетная терапия"], "Пазопаниб монотерапия",
         [drug("Пазопаниб", "800 мг/сут", "внутрь", "ежедневно", "ежедневно", "до прогрессирования/непереносимой токсичности")],
         sarc_stage, uur="C", udd=2, refs=["114", "146"],
         cite="van der Graaf W.T., Blay J.Y., Chawla S.P. et al. Pazopanib for metastatic soft-tissue sarcoma (PALETTE): a randomised, double-blind, placebo-controlled phase 3 trial",
         special="** ЖНВЛП; применяется при прогрессировании на цитостатической терапии"),
    base("C7", sarc_line, ["химиотерапия"], "Темозоломид монотерапия",
         [drug("Темозоломид", "50–75 мг/м²/сут внутрь в течение 6 из 8 недель, или 150–300 мг/сут внутрь в 1–5-й дни", "внутрь", "6 из 8 недель непрерывно, либо 1–5-й дни", "каждые 4 недели (для схемы 1–5 дни)")],
         sarc_stage, uur="C", udd=2, refs=["115"],
         cite="Anderson S., Aghajanian C. Temozolomide in uterine leiomyosarcomas. Gynecol Oncol 2005;98(1):99-103",
         special="** ЖНВЛП; # off-label; применяется при прогрессировании на фоне цитостатической терапии"),
    base("C7", sarc_line, ["химиотерапия"], "Эрибулин монотерапия",
         [drug("Эрибулин", "1,4 мг/м²", "в/в", "2–5 мин, 1-й и 8-й дни", "каждые 3 недели")],
         sarc_stage, uur="C", udd=2, refs=["110"],
         cite="Blay J.Y., Bauer S. et al. Eribulin versus dacarbazine in patients with leiomyosarcoma: subgroup analysis from a phase 3, open-label, randomised study",
         special="** ЖНВЛП; применяется при прогрессировании на фоне цитостатической терапии"),
    base("C7", sarc_line, ["химиотерапия"], "Трабектедин монотерапия",
         [drug("Трабектедин", "1,5 мг/м²", "в/в", "24-часовая инфузия", "каждые 3 недели")],
         sarc_stage, uur="C", udd=2, refs=["114", "116", "117"],
         cite="Morgan J.A., Cesne A.L., Chawla S.M. et al. Randomized phase II study of trabectedin in patients with liposarcoma and leiomyosarcoma after failure of prior anthracycline",
         special="при лейомиосаркоме матки ранее должны применяться антрациклины"),
    base("C7", sarc_line, ["химиотерапия"], "Доцетаксел еженедельный (36 мг/м²)",
         [drug("Доцетаксел", "36 мг/м²", "в/в", "1 ч, 1, 8, 15-й дни", "каждые 4 недели")],
         sarc_stage, uur="C", udd=2, refs=["109", "146"],
         cite="Garcia A.A., Blessing J.A., Nolte S., Mannel R.S. A phase II evaluation of weekly docetaxel in the treatment of recurrent or persistent endometrial carcinoma",
         special="** ЖНВЛП; # off-label"),
    base("C7", sarc_line, ["химиотерапия"], "Винорелбин монотерапия",
         [drug("Винорелбин", "30 мг/м²", "в/в", "1-й и 8-й дни", "каждые 3 недели")],
         sarc_stage, uur="C", udd=2, refs=["146", "147"],
         cite=None,
         special="** ЖНВЛП; # off-label; " + unres146),
]

audit.event(DOC, "phase2-start", "460_4 рак тела матки и саркомы матки: cohort-first extraction")
audit.read_block(DOC, "460_4.md", 398, 493, "§3.4 Лекарственное лечение: адъювантная ХТ РТМ, 1L/2L прогрессирования, гормонотерапия, ХТ сарком")
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
