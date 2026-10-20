#!/usr/bin/env python3
"""Build 70_2 (Остеосаркома и саркома Юинга, дети) cohorts + regimens."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import json, audit

DOC="70_2"
audit.event(DOC,"phase2-start","70_2 Остеосаркома и саркома Юинга (дети): cohort-first extraction")

DISEASE={
 "name":"Злокачественные новообразования костей и суставных хрящей: остеосаркома, саркома Юинга",
 "icd10":"C40-C41",
 "histology_type":"остеосаркома (высокой степени злокачественности; центральная низкой степени, периостальная/параостальная промежуточной степени), саркома Юинга и другие недифференцированные мелкокруглоклеточные саркомы костей",
}

def d(inn,dose,route,sched=None,freq=None,mx=None):
    return {"inn":inn,"dose":dose,"route":route,"schedule":sched,"cycle_frequency":freq,"max_cycles":mx}

CITE={
 "9":"NCCN Clinical Practice Guidelines in Oncology (NCCN Guidelines) Version 2.2024. National Comprehensive Cancer Network",
 "12":"Валиев А.К., Тепляков В.В., Мусаев Э.Р. и соавт. Практические рекомендации по лечению злокачественных опухолей костей у детей",
 "14":"Casali P.G., Bielack S., Abecassis N., et al. Bone sarcomas: ESMO-PaedCan-EURACAN Clinical Practice Guidelines // Ann Oncol",
 "33":"Алиев М.Д. Злокачественные опухоли костей // Саркомы костей, мягких тканей и опухоли кожи. 2010;2:3–8",
 "34":"Ritter J., Bielack S.S. Osteosarcoma // Ann Oncol. 2010;21:320–325",
 "36":"Marina N.M., Smeland S., Bielack S.S., et al. Comparison of MAPIE versus MAP in patients with a poor response to preoperative chemotherapy... // Lancet Oncol",
 "37":"Whelan J.S., Bielack S.S., Marina N., et al. EURAMOS-1, an international randomised study for osteosarcoma",
 "38":"Ferrari S., Smeland S., Mercuri M., et al. Neoadjuvant chemotherapy with high-dose ifosfamide, high-dose methotrexate...",
 "51":"Gaspar N., Campbell-Hewson Q., Huang J., et al. OLIE, ITCC-082: a Phase II trial of lenvatinib plus ifosfamide/etoposide",
 "52":"Gaspar N., Venkatramani R., Hecker-Nolting S., et al. Lenvatinib in combination with chemotherapy in relapsed/refractory osteosarcoma",
 "53":"Palmerini E., Setola E., Grignani G., et al. High-dose ifosfamide in relapsed/refractory osteosarcoma",
 "54":"Palmerini E., Jones R.L., Marchesi E., et al. Gemcitabine and docetaxel in relapsed/refractory osteosarcoma",
 "55":"Navid F., Willert J.R., McCarville M.B., et al. Combination of gemcitabine and docetaxel in the treatment of children and young adults with refractory bone sarcoma",
 "56":"Song B.S., Seo J., Kim D.H., et al. Gemcitabine and docetaxel for the treatment of children and adolescents with refractory osteosarcoma",
 "57":"Raciborska A., Bilska K. Sorafenib in patients with progressed and refractory bone tumors // Med Oncol. 2018;35",
 "58":"Grignani G., Palmerini E., Dileo P., et al. A phase II trial of sorafenib in relapsed and unresectable high-grade osteosarcoma",
 "59":"Sugiyama M., Arakawa A., Shirakawa N., et al. Regorafenib in pediatric osteosarcoma",
 "60":"Peretz Soroka H., Vora T., Noujaim J., et al. Cabozantinib/regorafenib in bone sarcomas",
 "61":"Davis L.E., Bolejack V., Ryan C.W., et al. Randomized double-blind phase II study of regorafenib in patients with metastatic osteosarcoma",
 "62":"Grier H.E., Krailo M.D., Tarbell N.J., et al. Addition of ifosfamide and etoposide to standard chemotherapy for Ewing's sarcoma",
 "63":"Womer R.B., West D.C., Krailo M.D., et al. Randomized controlled trial of interval-compressed chemotherapy for the treatment of Ewing sarcoma",
 "64":"Brennan B., Kirton L., Marec-Bérard P., et al. Comparison of high-dose chemotherapy with tandem HDCT for localized Ewing sarcoma",
 "65":"Anderton J., Moroz V., Marec-Bérard P., et al. High-dose chemotherapy and autologous haematopoietic stem cell transplantation in Ewing sarcoma",
 "66":"International Randomised Controlled Trial for the Treatment of Newly Diagnosed Ewing's Sarcoma Family of Tumours (Euro-EWING99)",
 "68":"Ladenstein R. et al. Primary disseminated multifocal Ewing sarcoma: Results of the Euro-EWING 99 trial // J Clin Oncol",
 "69":"Tenneti P. et al. Role of high-dose chemotherapy and autologous hematopoietic cell transplantation for children with Ewing sarcoma",
 "70":"Whelan J., Le Deley M.C., Dirksen U., et al. High-dose chemotherapy and blood autologous stem-cell rescue in Ewing sarcoma (EWIG 2008)",
 "71":"Koscielniak E. et al. Results of treatment for soft tissue sarcoma in childhood and adolescence: a final report",
 "73":"Gupta A., Riedel R.F., Shah C., et al. Maintenance therapy in sarcoma",
 "75":"Meyers P.A., Ambati S.R., Slotkin E.K., et al. The addition of cycles of irinotecan/temozolomide",
 "76":"Raciborska A., Bilska K., Rodriguez-Galindo C. Maintenance treatment with trofosfamide in patients with primary refractory Ewing sarcoma",
 "77":"Tamura A., Yamamoto N., Nino N., et al. Pazopanib maintenance therapy after tandem high-dose chemotherapy for disseminated bone sarcomas",
 "78":"Minard-Colin V., Ichante J.L., Nguyen L., et al. Maintenance monthly metronomic cyclophosphamide/vinorelbine",
 "80":"Büyükkapu Bay S., Kebudi R., Görgün O., et al. Vincristine, irinotecan, and temozolomide (VIT) in recurrent/refractory sarcoma",
 "82":"Hunold A., Weddeling N., Paulussen M., et al. Topotecan and cyclophosphamide in patients with refractory or relapsed Ewing tumor",
 "83":"Kushner B.H., Kramer K., Meyers P.A., et al. Pilot study of topotecan and high-dose cyclophosphamide",
 "84":"Saylors R.L. 3rd, Stine K.C., Sullivan J., et al. Cyclophosphamide plus topotecan in children with recurrent or refractory solid tumors",
 "85":"Martin McCabe et al. Phase III assessment of topotecan and cyclophosphamide and high-dose ifosfamide in rEECur",
 "86":"Mori Y., Kinoshita S., Kanamori T., et al. Successful pazopanib treatment",
 "87":"Attia S., Bolejack V., Ganjoo K., et al. A phase II trial of regorafenib in patients with advanced Ewing sarcoma",
 "88":None,
 "89":"Юхта Т.В., Казанцев И.В., Геворгян А.Г. и др. Эффективность высокодозной полихимиотерапии с аутологичной ТГСК",
 "137":"Berrak S.G., Pearson M., Berberoğlu S., et al. High-dose ifosfamide in relapsed pediatric osteosarcoma",
 "144":"International randomized controlled trial of chemotherapy for the treatment of recurrent and primary refractory Ewing sarcoma (rEECur)",
}
def cite(refs):
    r=refs[0]
    return CITE.get(r)

cohorts=[
 {"cohort_id":"C1","disease":DISEASE,"stage":"остеосаркома высокой степени злокачественности (локализованная и метастатическая)","resectability":None,
  "clinical_situation":"Комбинированное лечение: неоадъювантная ПХТ по схеме MAP (блоки AP/M/A), операция на 11-й неделе, адъювантная ПХТ","ecog":None,
  "biomarkers":[],"treatment_stages":["неоадъювантная и адъювантная ПХТ"],"source":{"section":"3.1"}},
 {"cohort_id":"C1a","disease":DISEASE,"stage":"рецидив остеосаркомы или прогрессия заболевания","resectability":None,
  "clinical_situation":"Терапия второй и последующих линий (IE+ленватиниб, HD-I, Gem/Tax, сорафениб, регорафениб, кабозантиниб)","ecog":None,
  "biomarkers":[],"treatment_stages":["2-я и последующие линии"],"source":{"section":"3.1"}},
 {"cohort_id":"C2","disease":DISEASE,"stage":"саркома Юинга и другие недифференцированные мелкокруглоклеточные саркомы костей (локализованная и метастатическая)","resectability":None,
  "clinical_situation":"Интенсивная ПХТ с интервалом 14 дней (альтернирующие курсы VDC/IE), всего 14 курсов; далее VC+IE±ЛТ или VAI+BuMel","ecog":None,
  "biomarkers":["перестройка генов CIC, BCOR, EWSR1-non-ETS (для рабдомиосаркомоподобных)"],"treatment_stages":["индукция","консолидация"],"source":{"section":"3.2"}},
 {"cohort_id":"C2a","parent":"C2","disease":DISEASE,"stage":"локализованная саркома Юинга: первичный очаг >200 см³ либо <200 см³ при патоморфозе 0–3 степени (>10% витальных клеток)","resectability":None,
  "clinical_situation":"Высокодозная ХТ BuMel с последующей аутоТГСК","ecog":None,
  "biomarkers":[],"treatment_stages":["высокодозная ХТ с аутоТГСК"],"source":{"section":"3.2"}},
 {"cohort_id":"C2b","parent":"C2","disease":DISEASE,"stage":"саркома Юинга с инициально выявленными отдалёнными метастазами","resectability":None,
  "clinical_situation":"Поддерживающая терапия циклофосфамид + винорелбин, начиная с 29-й недели, 12 месяцев","ecog":None,
  "biomarkers":[],"treatment_stages":["поддерживающая терапия"],"source":{"section":"3.2"}},
 {"cohort_id":"C2c","parent":"C2","disease":DISEASE,"stage":"рецидив саркомы Юинга или прогрессия заболевания; ранние рецидивы на этапе консолидации — ВДХТ с аутоТГСК","resectability":None,
  "clinical_situation":"Терапия второй и последующих линий (VIT, TC, HD-I, пазопаниб, регорафениб, кабозантиниб)","ecog":None,
  "biomarkers":[],"treatment_stages":["2-я и последующие линии"],"source":{"section":"3.2"}},
]

rows=[]
def R(cid,line,name,drugs,uur="C",udd=5,refs=(),sec="3",table=None,special="",maint=None,**ind):
    st=ind.get("stage",next((c["stage"] for c in cohorts if c["cohort_id"]==cid),None))
    ec=ind.get("ecog",next((c["ecog"] for c in cohorts if c["cohort_id"]==cid),None))
    bm=ind.get("biomarkers",next((c["biomarkers"] for c in cohorts if c["cohort_id"]==cid),[]))
    rows.append({"cohort_id":cid,"disease":DISEASE,
      "treatment":{"line_stage":line,"therapy_type":["химиотерапия"],"regimen_name":name},
      "drugs":drugs,"indications":{"stage":st,"ecog":ec,"biomarkers":bm},
      "evidence":{"uur":uur,"udd":udd},
      "source":{"page":None,"section":sec,"table":table,"references":[str(x) for x in refs],
                "citation":cite([str(x) for x in refs])},
      "special_conditions":special,"maintenance_therapy":maint})

# Остеосаркома
R("C1","неоадъювантный/адъювантный этап схемы MAP — курс AP","AP (доксорубицин + цисплатин)",
  [d("Доксорубицин","37,5 мг/м²/сут (СД = 70 мг/м²)","48-часовая непрерывная в/в инфузия","1–2 сутки курса"),
   d("Цисплатин","40 мг/м²/сут 72-часовая непрерывная инфузия (СД = 120 мг/м²) либо 60 мг/м²/сут 4-часовая инфузия дни 1–2 (СД = 120 мг/м²)","в/в","1–3 сутки курса"),
   d("Маннитол","# off-label; 8 г/м² (20% — 40 мл/м² или 15% — 53 мл/м²)".replace("# off-label; ",""),"в/в медленно","непосредственно перед введением цисплатина; при 24-часовой инфузии цисплатина — каждые 6 часов в дни введения")],
  uur="C",udd=4,refs=(9,12,14,34,35),sec="3.1",table="Схема 1",
  special="# маннитол — off-label; блок проводится на фоне гидратации 3000 мл/м²/сут (диурез >100 мл/ч); при задержке блока >7 дней доза цисплатина снижается на 25%")
R("C1","неоадъювантный/адъювантный этап схемы MAP — курс M","Высокодозный метотрексат (курс M)",
  [d("Метотрексат","12000 мг/м²","в/в капельно за 4 часа","пара метотрексатов на 1-й и 8-й день"),
   d("Кальция фолинат","15 мг/м² каждые 6 часов, начиная с 24 ч от начала инфузии метотрексата (при задержке выведения: (60 мг/м² × L):2 = суточная доза, где L — концентрация метотрексата)","в/в / внутрь","до снижения уровня метотрексата <0,1 мкмоль/л"),
   d("Натрия гидрокарбонат","60 ммоль на 1 литр натрия хлорида или декстрозы 5%","в/в","щелочная гидратация 3000 мл/м²/сут, pH мочи 7–8")],
  uur="C",udd=4,refs=(36,37,38),sec="3.1",table="Схема 1",
  special="контроль концентрации метотрексата крови на 24, 48, 72 ч (верхние границы 8 / 1 / 0,1 мкмоль/л)")
R("C1","адъювантный этап схемы MAP — курс A","Доксорубицин (курс A)",
  [d("Доксорубицин","37,5 мг/м²/сут (СД = 70 мг/м²)","48-часовая непрерывная в/в инфузия","1–2 сутки курса")],
  uur="C",udd=4,refs=(9,12,14),sec="3.1",table="Схема 1",
  special="гидратация 3000 мл/м² за 24 ч до введения, в 1–2 день курса и через 24 ч после; при задержке блока >7 дней доза доксорубицина снижается до 30 мг/м²/сут (СД = 60 мг/м²)")
# Остеосаркома 2L+
OS2="терапия второй и последующих линий при рецидиве/прогрессии остеосаркомы"
R("C1a",OS2,"IE + Ленватиниб",
  [d("Ифосфамид","3000 мг/м²/сут (СД = 9000 мг/м²)","в/в за 3 часа","дни 1–3"),
   d("Этопозид","100 мг/м²/сут (СД = 300 мг/м²)","в/в за 3 часа","дни 1–3"),
   d("Ленватиниб","14 мг/м²/сут","per os","ежедневно, непрерывно до наступления непереносимой токсичности или прогрессии"),
   d("Месна","3000 мг/м²/сут продленной инфузией дни 1–4 + 20% дополнительно болюсно перед каждым введением ифосфамида","в/в","дни 1–4")],
  uur="A",udd=2,refs=(51,52),sec="3.1",special="# ленватиниб — off-label; гидратация ≥3000 мл/м²/сут")
R("C1a",OS2,"HD-I (высокодозный ифосфамид)",
  [d("Ифосфамид","3000 мг/м²/сут (СД = 15000 мг/м²) для пациентов старше 8 лет либо 2000 мг/м²/сут каждые 12 часов, суммарно 7 введений (СД = 14000 мг/м²) для детей старше 6 лет","в/в за 3 часа (или за 2 часа каждые 12 часов)","дни 1–5 (старше 8 лет)"),
   d("Месна","3000 мг/м²/сут продленной инфузией дни 1–5 (+20% болюсно перед введениями) при дозе 3000 мг/м²/сут; 4000 мг/м²/сут дни 1–4 (+20%) при дозе 2000 мг/м²/сут","в/в","параллельно с ифосфамидом")],
  udd=4,refs=(14,53,137),sec="3.1",special="# ифосфамид — off-label")
R("C1a",OS2,"Gem/Tax (гемцитабин + доцетаксел)",
  [d("Гемцитабин","675 или 900 мг/м²/сут (СД = 1350 или 1800 мг/м²)","в/в за 90 минут","1-й и 8-й день","—"),
   d("Доцетаксел","75 или 100 мг/м²/сут (СД = 75 или 100 мг/м²)","в/в за 1 час","8-й день","—")],
  udd=4,refs=(9,14,54,55,56),sec="3.1",special="# гемцитабин, # доцетаксел — off-label; для пациентов старше 8 лет")
R("C1a",OS2,"Сорафениб",
  [d("Сорафениб","400 мг/сут 2 раза в день (старше 15 лет и/или вес более 50 кг); 100 мг 2 раза в день (младше 15 лет, вес 15–20 кг); 200 мг 2 раза в день (младше 15 лет, вес 20–30 кг)","per os","каждые 12 часов, непрерывно до наступления непереносимой токсичности или прогрессии")],
  udd=4,refs=(9,14,57,58),sec="3.1",special="# сорафениб — off-label")
R("C1a",OS2,"Регорафениб",
  [d("Регорафениб","160 мг/сут","per os","непрерывно до наступления непереносимой токсичности или прогрессии")],
  udd=4,refs=(59,60,61),sec="3.1",special="# регорафениб — off-label")
R("C1a",OS2,"Кабозантиниб",
  [d("Кабозантиниб","60 мг/сут","per os","непрерывно до наступления непереносимой токсичности или прогрессии")],
  udd=4,refs=(60,),sec="3.1",special="# кабозантиниб — off-label")
# Саркома Юинга
EWS="интенсивная индукционная/адъювантная ПХТ (альтернирующие курсы VDC/IE, интервал 14 дней)"
R("C2",EWS,"VDC (винкристин + доксорубицин + циклофосфамид)",
  [d("Винкристин","2 мг/м² (не более 2 мг; 0,05 мг/кг для детей 1–3 лет, 0,025 мг/кг младше 1 года)","в/в струйно медленно","день 1"),
   d("Доксорубицин","37,5 мг/м²/сут (для детей <1 года 1,25 мг/кг в день), суммарно 75 мг/м²","в/в капельно продлённой инфузией за 48 часов","дни 1, 2"),
   d("Циклофосфамид","1200 мг/м²","в/в капельно за 1 час","день 1"),
   d("Месна","1200 мг/м² за 24 часа в день введения циклофосфамида + 20% дополнительно болюсно перед введением","в/в","день введения циклофосфамида")],
  uur="C",udd=5,refs=(62,63,66),sec="3.2",table="Схема 2",
  special="курсы в недели 1, 5, 9, 13, 17 (индукция); после кумулятивной дозы антрациклинов 375 мг/м² блок проводится без доксорубицина (VC)")
R("C2",EWS,"IE (ифосфамид + этопозид)",
  [d("Ифосфамид","1800 мг/м²/сут (СД = 9000 мг/м²)","в/в за 1 час","дни 1–5"),
   d("Этопозид","100 мг/м²/сут (СД = 500 мг/м²)","в/в за 2 часа","дни 1–5"),
   d("Месна","2000 мг/м²/сут продленной инфузией дни 1–5 + 20% дополнительно болюсно перед каждым введением ифосфамида","в/в","дни 1–5")],
  uur="C",udd=5,refs=(62,63,66),sec="3.2",table="Схема 2",
  special="курсы в недели 3, 7, 11, 15 (индукция)")
R("C2","адъювантный этап после операции (после кумулятивной дозы антрациклинов 375 мг/м²)","VC (винкристин + циклофосфамид)",
  [d("Винкристин","2 мг/м² (не более 2 мг)","в/в струйно медленно","день 1"),
   d("Циклофосфамид","1200 мг/м² (для детей младше 3 лет 40 мг/кг × 1 в день)","в/в капельно за 1 час","день 1"),
   d("Месна","1200 мг/м² за 24 часа + 20% болюсно перед введением","в/в","день введения циклофосфамида")],
  uur="C",udd=5,refs=(12,17,66),sec="3.2",table="Схема 2")
R("C2a","высокодозная ХТ с аутоТГСК (консолидация)","BuMel (кондиционирование бусульфан + мелфалан)",
  [d("Бусульфан","по массе: <9 кг — 1 мг/кг; 9–<16 кг — 1,2 мг/кг; 16–23 кг — 1,1 мг/кг; >23–34 кг — 0,95 мг/кг; >34 кг — 0,8 мг/кг","в/в за 30 минут","с −7 по −3 день, каждые 6 часов (суммарно 16 введений)"),
   d("Мелфалан","140 мг/м²","в/в за 30 минут","−2 день")],
  uur="C",udd=4,refs=(64,65,66,68,69,70),sec="3.2",table="Схема 4",
  special="# бусульфан, # мелфалан — off-label; кондиционирование перед аутологичной ТГСК")
MT="поддерживающая терапия при инициальных отдалённых метастазах (с 29-й недели)"
R("C2b",MT,"Метрономная поддерживающая терапия: циклофосфамид + винорелбин",
  [d("Циклофосфамид","25 мг/м²/сут","per os","непрерывно с 1 по 28 день каждого курса"),
   d("Винорелбин","25 мг/м²","в/в","дни 1, 8, 15 каждого курса")],
  uur="C",udd=5,refs=(33,71,73,74,75,76,77,78),sec="3.2",
  maint="Циклофосфамид 25 мг/м²/сут per os дни 1–28 + винорелбин 25 мг/м² в/в дни 1, 8, 15, 12 курсов в течение 12 месяцев",
  special="# винорелбин — off-label")
ES2="терапия второй и последующих линий при рецидиве/прогрессии саркомы Юинга"
R("C2c",ES2,"VIT (винкристин + иринотекан + темозоломид)",
  [d("Винкристин","1,5 мг/м²/сут","в/в за 30 минут","день 1"),
   d("Иринотекан","50 мг/м²/сут (СД = 250 мг/м²)","в/в за 1 час","дни 1–5"),
   d("Темозоломид","150 мг/м²/сут (СД = 750 мг/м²)","per os","дни 1–5")],
  udd=4,refs=(80,),sec="3.2",special="# иринотекан, # темозоломид — off-label; для пациентов старше 1 года")
R("C2c",ES2,"TC (топотекан + циклофосфамид)",
  [d("Топотекан","0,75 мг/м²/сут","в/в капельно за 1 час","дни 1–5"),
   d("Циклофосфамид","250 мг/м²/сут","в/в за 1 час","дни 1–5")],
  udd=4,refs=(82,83,84),sec="3.2",special="# топотекан — off-label")
R("C2c",ES2,"HD-I (высокодозный ифосфамид)",
  [d("Ифосфамид","3000 мг/м²/сут (СД = 15000 мг/м²), для пациентов старше 4 лет","в/в за 24 часа","дни 1–5"),
   d("Месна","400 мг/м²/сут продлённой инфузией за 1 час до ифосфамида, затем 3000 мг/м²/сут непрерывно дни 1–5, затем 800 мг/м²/сут после окончания","в/в","дни 1–5")],
  udd=2,refs=(85,144),sec="3.2",special="# ифосфамид — off-label")
R("C2c",ES2,"Пазопаниб",
  [d("Пазопаниб","800 мг/сут","per os","непрерывно до наступления непереносимой токсичности или прогрессии")],
  udd=4,refs=(77,86),sec="3.2",special="# пазопаниб — off-label")
R("C2c",ES2,"Регорафениб",
  [d("Регорафениб","160 мг/сут","per os","непрерывно до наступления непереносимой токсичности или прогрессии")],
  udd=4,refs=(60,87),sec="3.2",special="# регорафениб — off-label")
R("C2c",ES2,"Кабозантиниб",
  [d("Кабозантиниб","60 мг/сут","per os","непрерывно до наступления непереносимой токсичности или прогрессии")],
  udd=4,refs=(60,),sec="3.2",special="# кабозантиниб — off-label")

with open(f"output-cohort/{DOC}.cohorts.json","w") as f: json.dump(cohorts,f,ensure_ascii=False,indent=1)
with open(f"output-cohort/{DOC}.regimens.json","w") as f: json.dump(rows,f,ensure_ascii=False,indent=1)
for c in cohorts: audit.cohort(DOC,c)
for r in rows: audit.regimen(DOC,r)
audit.event(DOC,"phase2-done",f"{len(rows)} regimens, {len(cohorts)} cohorts")
print(f"{DOC}: {len(cohorts)} cohorts, {len(rows)} regimens written")
