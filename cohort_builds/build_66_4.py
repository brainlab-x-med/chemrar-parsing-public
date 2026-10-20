#!/usr/bin/env python3
"""Build 66_4 (Рак носоглотки, дети) cohorts + regimens, audit events."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import json, audit

DOC="66_4"
audit.event(DOC,"phase2-start","66_4 Рак носоглотки (дети): cohort-first extraction")

DISEASE={
 "name":"Рак носоглотки (назофарингеальная карцинома)",
 "icd10":"C11",
 "histology_type":"назофарингеальная карцинома (ВОЗ): I — плоскоклеточный ороговевающий рак; IIа — дифференцированный плоскоклеточный неороговевающий рак; IIb — недифференцированный плоскоклеточный неороговевающий рак; III — недифференцированная карцинома; IV — базалоидный плоскоклеточный рак",
}

def d(inn,dose,route,sched=None,freq=None,mx=None):
    return {"inn":inn,"dose":dose,"route":route,"schedule":sched,"cycle_frequency":freq,"max_cycles":mx}

CITE={
 "10":"Ben-Ami T., Kontny U., Surun A., et al. Nasopharyngeal carcinoma in children and adolescents: The EXPeRT/PARTNER diagnostic and therapeutic recommendations // Pediatric Blood & Cancer. 2021;68(S4):e29018",
 "21":"Ribassin-Majed L., Marguet S., Lee A.W.M., et al. What Is the Best Treatment of Locally Advanced Nasopharyngeal Carcinoma? An Individual Patient Data Network Meta-Analysis // J Clin Oncol. 2017;35(5):498–505",
 "22":"Тюлякова Г.В. и др. Анализ результатов лечения пациентов детского возраста с раком носоглотки: ретроспективное когортное исследование // Онкопедиатрия. 2018;5(4):257–267",
 "23":"Rodriguez-Galindo C., Krailo M.D., Krasin M.J., et al. Treatment of Childhood Nasopharyngeal Carcinoma With Induction Chemotherapy and Concurrent Chemoradiotherapy: COG ARAR0331 Study // J Clin Oncol. 2019;37(35):3369–3376",
 "24":"Casanova M., Bisogno G., Gandola L., et al. A prospective protocol for nasopharyngeal carcinoma in children and adolescents: the Italian Rare Tumors in Pediatric Age (TREP) project // Cancer. 2012;118(10):2718–2725",
 "25":"Buehrlen M., Zwaan C.M., Granzen B., et al. Multimodal treatment, including interferon beta, of nasopharyngeal carcinoma in children and young adults: NPC-2003-GPOH/DCOG // Cancer. 2012;118(19):4892–4900",
 "26":"Жуков Н.В., Рабаева Л.Л. Назофарингеальная карцинома у детей и подростков. Обзор литературы и собственные данные // Вопросы гематологии/онкологии и иммунопатологии в педиатрии. 2022;21(2):66–77",
 "27":"Römer T., Franzen S., Kravets H., et al. Multimodal Treatment of Nasopharyngeal Carcinoma in Children, Adolescents and Young Adults — NPC-2003-GPOH // Cancers. 2022;14(5):1261",
 "28":"Kontny U., Franzen S., Behrends U., et al. Diagnosis and Treatment of Nasopharyngeal Carcinoma in Children and Adolescents – Recommendations of the GPOH-NPC Study Group // Klin Padiatr. 2016;228(3):105–112",
 "29":"Zhang L., Huang Y., Hong S., et al. Gemcitabine plus cisplatin versus fluorouracil plus cisplatin in recurrent or metastatic nasopharyngeal carcinoma: phase 3 trial // Lancet. 2016;388(10054):1883–1892",
 "30":"Zhang Y., Chen L., Hu G.-Q., et al. Gemcitabine and Cisplatin Induction Chemotherapy in Nasopharyngeal Carcinoma // N Engl J Med. 2019;381(12):1124–1135",
 "31":"Liu X., Shen H., Zhang L., et al. Immunotherapy for recurrent or metastatic nasopharyngeal carcinoma // npj Precision Oncology. 2024;8(1):1–9",
 "32":"Yang Y., Qu S., Li J., et al. Camrelizumab versus placebo in combination with gemcitabine and cisplatin as first-line treatment for recurrent or metastatic nasopharyngeal carcinoma (CAPTAIN-1st) // Lancet Oncol. 2021;22(8):1162–1174",
}

cohorts=[
 {"cohort_id":"C1","disease":DISEASE,"stage":"все стадии НФК, режим лечения №1","resectability":None,
  "clinical_situation":"Индукционная ХТ (винбластин+циклофосфамид+доксорубицин+блеомицин) + оксодигидроакридинилацетат натрия + ЛТ + консолидирующая ХТ при ответе","ecog":None,
  "biomarkers":[],"treatment_stages":["индукционная ХТ","ЛТ","консолидация"],"source":{"section":"3.1"}},
 {"cohort_id":"C2a","disease":DISEASE,"stage":"стадии II, III, IVA — режим лечения №2","resectability":None,
  "clinical_situation":"Индукция фторурацил+цисплатин (3 курса) с последующей ХЛТ (цисплатин на фоне ЛТ)","ecog":None,
  "biomarkers":[],"treatment_stages":["индукционная ХТ","химиолучевая терапия"],"source":{"section":"3.2"}},
 {"cohort_id":"C2b","parent":"C2a","disease":DISEASE,"stage":"стадия IVB — режим лечения №2","resectability":None,
  "clinical_situation":"Индукция фторурацил+цисплатин (4 курса) с последующей ХЛТ","ecog":None,
  "biomarkers":[],"treatment_stages":["индукционная ХТ","химиолучевая терапия"],"source":{"section":"3.2"}},
 {"cohort_id":"C3a","disease":DISEASE,"stage":"стадии II, III, IVA — режим лечения №3","resectability":None,
  "clinical_situation":"Индукция гемцитабин+цисплатин (3 курса) с последующей ХЛТ (цисплатин на фоне ЛТ)","ecog":None,
  "biomarkers":[],"treatment_stages":["индукционная ХТ","химиолучевая терапия"],"source":{"section":"3.3"}},
 {"cohort_id":"C3b","disease":DISEASE,"stage":"стадия IVB — режим лечения №3","resectability":None,
  "clinical_situation":"Индукционная химиоиммунотерапия гемцитабин+цисплатин+пембролизумаб (4 курса) с последующей ХЛТ","ecog":None,
  "biomarkers":[],"treatment_stages":["индукционная химиоиммунотерапия","химиолучевая терапия"],"source":{"section":"3.3"}},
 {"cohort_id":"C4","disease":DISEASE,"stage":"стадия I","resectability":None,
  "clinical_situation":"Только ЛТ без индукции; наблюдение без поддерживающей терапии (лекарственных схем нет)","ecog":None,
  "biomarkers":[],"treatment_stages":["ЛТ"],"source":{"section":"3.2"}},
 {"cohort_id":"C5","disease":DISEASE,"stage":"стадии II, III, IVA, IVB после завершения лучевой терапии","resectability":None,
  "clinical_situation":"Поддерживающая терапия интерфероном бета-1b 6 мес","ecog":None,
  "biomarkers":[],"treatment_stages":["поддерживающая терапия"],"source":{"section":"3.4"}},
]

rows=[]
def R(cid,line,rtype,name,drugs,uur="C",udd=5,refs=(),sec="3",table=None,special="",maint=None,**ind):
    st=ind.get("stage",next((c["stage"] for c in cohorts if c["cohort_id"]==cid),None))
    ec=ind.get("ecog",next((c["ecog"] for c in cohorts if c["cohort_id"]==cid),None))
    bm=ind.get("biomarkers",next((c["biomarkers"] for c in cohorts if c["cohort_id"]==cid),[]))
    rows.append({"cohort_id":cid,"disease":DISEASE,
      "treatment":{"line_stage":line,"therapy_type":rtype,"regimen_name":name},
      "drugs":drugs,"indications":{"stage":st,"ecog":ec,"biomarkers":bm},
      "evidence":{"uur":uur,"udd":udd},
      "source":{"page":None,"section":sec,"table":table,"references":[str(x) for x in refs],
                "citation":CITE.get(str(refs[0])) if refs else None},
      "special_conditions":special,"maintenance_therapy":maint})

R("C1","индукционный этап режима №1 (неоадъювантно перед ЛТ)",["химиотерапия"],
  "Винбластин + Циклофосфамид + Доксорубицин + Блеомицин",
  [d("Винбластин","5 мг/м²","внутривенно струйно","дни 1, 8, 15","каждые 21–28 дней",4),
   d("Циклофосфамид","600 мг/м²","в/в инфузия за 1 час","день 1"),
   d("Доксорубицин","20 мг/м²","в/в инфузия за 1 час","дни 1, 8"),
   d("Блеомицин","10 мг/м²","в/в инфузия за 1 час","дни 2, 4")],
  uur="C",udd=4,refs=(21,22),sec="3.1",table="Таблица 2",
  special="# винбластин, # циклофосфамид, # блеомицин — off-label; 4 курса индукции; при суммарной дозе блеомицина 300 мг/м² препарат исключают")
R("C1","на фоне индукционной ПХТ и ЛТ (для улучшения ответа опухоли)",["химиотерапия (иммуностимулирующая/потенцирующая)"],
  "Оксодигидроакридинилацетат натрия",
  [d("Оксодигидроакридинилацетат натрия","5 мг/кг в сутки однократно","в/в","с интервалом 48 часов; курс включает 5–7 инъекций с интервалом 2 недели",
     None,4)],
  uur="C",udd=5,refs=(22,),sec="3.1",
  special="возможно введение с раствором прокаина 0,25–0,5% (2 мл); суммарно 4 курса на фоне первых 4 курсов ПХТ и ЛТ")
R("C1","консолидирующий этап режима №1 (при полном/частичном ответе)",["химиотерапия"],
  "Винбластин + Циклофосфамид + Дактиномицин",
  [d("Винбластин","5 мг/м²","внутривенно струйно","дни 1, 8, 15","каждые 21–28 дней"),
   d("Циклофосфамид","500 мг/м²","в/в инфузия за 1 час","дни 1, 8"),
   d("Дактиномицин","1200 (как указано в документе; максимальная разовая доза 2,5 мг)","внутривенно струйно","день 1","каждые 21–28 дней")],
  uur="C",udd=4,refs=(22,),sec="3.1",table="Таблица 3",
  special="# дактиномицин — off-label; 4 курса консолидации; дактиномицин не вводится во время проведения лучевой терапии")
R("C2a","индукционный этап режима №2",["химиотерапия"],"Фторурацил + Цисплатин",
  [d("Фторурацил","1000 мг/м²","в/в инфузия за 24 часа","дни 1–5","каждые 21–28 дней",3),
   d("Цисплатин","100 мг/м²","в/в инфузия 6 часов","день 1")],
  uur="B",udd=3,refs=(23,24,25,26),sec="3.2",table="Таблица 4",
  special="# фторурацил — off-label; 3 курса индукции для стадий II, III, IVA")
R("C2b","индукционный этап режима №2 (стадия IVB)",["химиотерапия"],"Фторурацил + Цисплатин",
  [d("Фторурацил","1000 мг/м²","в/в инфузия за 24 часа","дни 1–5","каждые 21–28 дней",4),
   d("Цисплатин","100 мг/м²","в/в инфузия 6 часов","день 1")],
  uur="C",udd=4,refs=(26,27),sec="3.2",table="Таблица 4",
  special="# фторурацил — off-label; 4 курса индукции для стадии IVB (профилактика и лечение отдалённых метастазов)")
R("C2a","химиолучевой этап режима №2 (первые и последние 3 дня ЛТ)",["химиолучевая терапия"],"Цисплатин (синхронно с ЛТ)",
  [d("Цисплатин","20 мг/м²","в/в за 1 час","первые 3 и последние 3 дня лучевой терапии")],
  uur="B",udd=3,refs=(25,26,27),sec="3.2")
R("C2b","химиолучевой этап режима №2 (стадия IVB)",["химиолучевая терапия"],"Цисплатин (синхронно с ЛТ)",
  [d("Цисплатин","20 мг/м²","в/в за 1 час","первые 3 и последние 3 дня лучевой терапии")],
  uur="B",udd=3,refs=(25,27),sec="3.2")
R("C3a","индукционный этап режима №3",["химиотерапия"],"Гемцитабин + Цисплатин",
  [d("Гемцитабин","1000 мг/м²","в/в инфузия 30 мин","дни 1, 8","каждые 21 день",3),
   d("Цисплатин","80 мг/м²","в/в инфузия 4 ч","день 1")],
  uur="B",udd=2,refs=(29,30),sec="3.3",table="Таблица 5",
  special="# гемцитабин — off-label; 3 курса индукции для стадий II, III, IVA")
R("C3b","индукционный этап режима №3 (стадия IVB)",["химиотерапия","иммунотерапия"],
  "Гемцитабин + Цисплатин + Пембролизумаб",
  [d("Гемцитабин","1000 мг/м²","в/в инфузия 30 мин","дни 1, 8","каждые 21 день",4),
   d("Цисплатин","80 мг/м²","в/в инфузия 4 ч","день 1"),
   d("Пембролизумаб","2 мг/кг (макс. 200 мг)","в/в инфузия 30 мин","день 1")],
  uur="C",udd=5,refs=(31,32),sec="3.3",table="Таблица 6",
  special="# гемцитабин, # пембролизумаб — off-label; добавление пембролизумаба возможно при наличии Федерального консилиума; 4 курса")
R("C3a","химиолучевой этап режима №3 (первые и последние 3 дня ЛТ)",["химиолучевая терапия"],"Цисплатин (синхронно с ЛТ)",
  [d("Цисплатин","20 мг/м²","в/в за 1 час","первые 3 и последние 3 дня лучевой терапии")],
  uur="B",udd=3,refs=(25,26),sec="3.3")
R("C5","поддерживающая терапия после лучевой терапии",["иммунотерапия"],"Интерферон бета-1b",
  [d("Интерферон бета-1b","100 тыс. МЕ/кг","п/к","3 раза в неделю","—","6 месяцев")],
  uur="B",udd=3,refs=(25,27),sec="3.4",table="Таблица 8",
  maint="Интерферон бета-1b 100 тыс. МЕ/кг п/к 3 раза в неделю в течение 6 месяцев после завершения лучевой терапии",
  special="# интерферон бета-1b — off-label")

with open(f"output-cohort/{DOC}.cohorts.json","w") as f: json.dump(cohorts,f,ensure_ascii=False,indent=1)
with open(f"output-cohort/{DOC}.regimens.json","w") as f: json.dump(rows,f,ensure_ascii=False,indent=1)
for c in cohorts: audit.cohort(DOC,c)
for r in rows: audit.regimen(DOC,r)
audit.event(DOC,"phase2-done",f"{len(rows)} regimens, {len(cohorts)} cohorts")
print(f"{DOC}: {len(cohorts)} cohorts, {len(rows)} regimens written")
