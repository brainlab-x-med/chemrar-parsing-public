#!/usr/bin/env python3
"""Build 69_2 (Экстракраниальные герминогенные опухоли, дети) cohorts + regimens."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import json, audit

DOC="69_2"
audit.event(DOC,"phase2-start","69_2 Экстракраниальные герминогенные опухоли (дети): cohort-first extraction")

DISEASE={
 "name":"Экстракраниальные герминогенные опухоли",
 "icd10":"C38.1, C48.0, C49.0, C49.5, C49.9, C56, C62",
 "histology_type":"герминогенные опухоли: герминома/семинома/дисгерминома (ОЖМ), зрелая и незрелая тератома (Grade 0–2), злокачественная тератома (Grade 3), эмбриональный рак, опухоль желточного мешка, хориокарцинома, смешанные ГКО",
}

def d(inn,dose,route,sched=None,freq=None,mx=None):
    return {"inn":inn,"dose":dose,"route":route,"schedule":sched,"cycle_frequency":freq,"max_cycles":mx}

CITE={
 "3":"Детская онкология. Национальное руководство / под ред. М.Д. Алиева, В.Г. Полякова, Г.Л. Менткевича, С.А. Маяковой",
 "5":"Cecchetto G. Gonadal germ cell tumors in children and adolescents // J Indian Assoc Pediatr Surg. 2014;19(4):189–194",
 "11":"Marina N. et al. Treatment of childhood germ cell tumors. Review of the St. Jude experience from 1979 to 1988 // Cancer. 1992;70(10):2568–2575",
 "12":"Marina N.M. et al. Complete surgical excision is effective treatment for children with immature teratomas... // J Clin Oncol. 1999;17(7):2137–2143",
 "13":"MAKEI 05 protocol (versie 1)",
 "14":"Ongoing Clinical Trials in Testicular Cancer: The TIGER Trial // Oncol Res Treat",
 "15":"Einhorn L.H. et al. Phase II study of paclitaxel plus gemcitabine salvage chemotherapy for germ cell tumors after progression following high-dose chemotherapy with tandem transplant // J Clin Oncol. 2007;25(5):513–516",
 "16":"Bokemeyer C. et al. Combination chemotherapy with gemcitabine, oxaliplatin, and paclitaxel in patients with cisplatin-refractory or multiply relapsed germ-cell tumors // Ann Oncol. 2008;19(3):448–453",
 "17":"Al F. et al. Comparison of carboplatin versus cisplatin in the treatment of paediatric extracranial malignant germ cell tumours // Eur J Cancer. 2018;98",
 "31":"Mead G.M. et al. A phase II trial of TIP (paclitaxel, ifosfamide and cisplatin) given as second-line (post-BEP) salvage chemotherapy... // Br J Cancer. 2005;93(2):178–184",
 "32":"Shatara M. et al. GCT-66. Final report of the prospective NEXT/CNS-GCT-4 consortium trial (GemPOx followed by marrow-ablative chemotherapy) // Neuro-Oncol. 2020;22(Suppl 3):iii341",
 "36":"Frazier A.L. et al. Revised risk classification for pediatric extracranial germ cell tumors based on 25 years of clinical trial data from the United Kingdom and United States // J Clin Oncol. 2015;33(2):195–201",
}

cohorts=[
 {"cohort_id":"C1","disease":DISEASE,"stage":"внегонадные злокачественные ГКО: T1aN0M0/T1bN0M0 (R0 — наблюдение; R1/R2 — ХТ)","resectability":"R0/R1/R2",
  "clinical_situation":"w&w при R0; 3×PEI при R1/R2 с 2nd look и 1×PEI","ecog":None,
  "biomarkers":["АФП","ХГЧ"],"treatment_stages":["послеоперационная терапия по радикальности резекции"],"source":{"section":"3"}},
 {"cohort_id":"C2","disease":DISEASE,"stage":"внегонадные злокачественные ГКО T2a/bN0M0","resectability":"R0/R1/R2",
  "clinical_situation":"4×PEI (R0/R1) или 3×PEI (R2) со second-look и 1×PEI","ecog":None,
  "biomarkers":["АФП","ХГЧ"],"treatment_stages":["постоперационная ХТ"],"source":{"section":"3"}},
 {"cohort_id":"C3","disease":DISEASE,"stage":"злокачественные ГКО яичка: IA «чистая» ОЖМ — watch-and-wait; IA другая/смешанная и IB–IC — 2×PE; IIA — 2×PEI; IIB–IIID — 3×PEI ± 1×PEI","resectability":None,
  "clinical_situation":"Терапия злокачественных ГКО яичка после высокой паховой орхиэктомии (Lugano)","ecog":None,
  "biomarkers":["АФП","ХГЧ"],"treatment_stages":["адъювантная/индукционная ХТ"],"source":{"section":"3"}},
 {"cohort_id":"C4","disease":DISEASE,"stage":"злокачественные ГКО яичников FIGO Ia–Ib — watch-and-wait (R0-R1); Ic, IIa–IIb — 2×PE; IIc — 3×PEI+1×PEI; IIIa–IV — предоперационная ХТ 3×PEI + удаление остаточной опухоли + 1×PEI","resectability":None,
  "clinical_situation":"Терапия злокачественных ГКО яичников","ecog":None,
  "biomarkers":["АФП","ХГЧ"],"treatment_stages":["предоперационная и послеоперационная ХТ"],"source":{"section":"3"}},
 {"cohort_id":"C5","disease":DISEASE,"stage":"рефрактерное течение или рецидив ГКО (младше 18 лет); детям до 10 лет доступны JEB и CarboPET","resectability":None,
  "clinical_situation":"Химиотерапия второй линии (CarboPET, TIP, TI-CE, гемцитабин+паклитаксел, GemPOx, JEB) после консультации с Федеральным центром","ecog":None,
  "biomarkers":["АФП","ХГЧ"],"treatment_stages":["2-я линия терапии"],"source":{"section":"3"}},
]

rows=[]
def R(cid,line,name,drugs,uur="C",udd=5,refs=(),sec="3",table=None,special="",**ind):
    st=ind.get("stage",next((c["stage"] for c in cohorts if c["cohort_id"]==cid),None))
    ec=ind.get("ecog",next((c["ecog"] for c in cohorts if c["cohort_id"]==cid),None))
    bm=ind.get("biomarkers",next((c["biomarkers"] for c in cohorts if c["cohort_id"]==cid),[]))
    rows.append({"cohort_id":cid,"disease":DISEASE,
      "treatment":{"line_stage":line,"therapy_type":["химиотерапия"],"regimen_name":name},
      "drugs":drugs,"indications":{"stage":st,"ecog":ec,"biomarkers":bm},
      "evidence":{"uur":uur,"udd":udd},
      "source":{"page":None,"section":sec,"table":table,"references":[str(x) for x in refs],
                "citation":CITE.get(str(refs[0])) if refs else None},
      "special_conditions":special,"maintenance_therapy":None})

R("C1","терапия внегонадных злокачественных ГКО (T1aN0M0/T1bN0M0, R1/R2)","PEI ×3 (+ second-look + PEI ×1)",
  [d("Цисплатин","20 мг/м² в сутки (кумулятивно за курс 100 мг/м²)","в/в инфузия 1 ч","дни 1, 2, 3, 4, 5","каждые 21 день"),
   d("Этопозид","100 мг/м² в сутки (кумулятивно за курс 300 мг/м²)","в/в инфузия 1 ч (до цисплатина)","дни 1, 2, 3"),
   d("Ифосфамид","1500 мг/м² в сутки (кумулятивно за курс 7500 мг/м²) на фоне инфузионной терапии месной","в/в инфузия 22 ч","дни 1, 2, 3, 4, 5")],
  refs=(3,),sec="3",table="Таблица 10; таблица терапевтических опций вне gonadных ГКО",
  special="# этопозид, # ифосфамид — off-label; детям младше 2 лет либо менее 10 кг доза рассчитывается на кг (30 кг = 1 м²); при индексе Карновского <50 доза ифосфамида 1000 мг/м²/день дни 1–5; в возрасте менее 4 месяцев ифосфамид исключается")
R("C2","терапия внегонадных злокачественных ГКО (T2a/bN0M0)","PEI ×4 (R0/R1) или ×3 (R2)",
  [d("Цисплатин","20 мг/м² в сутки (100 мг/м² за курс)","в/в инфузия 1 ч","дни 1–5","каждые 21 день"),
   d("Этопозид","100 мг/м² в сутки (300 мг/м² за курс)","в/в инфузия 1 ч (до цисплатина)","дни 1, 2, 3"),
   d("Ифосфамид","1500 мг/м² в сутки (7500 мг/м² за курс) на фоне месны","в/в инфузия 22 ч","дни 1–5")],
  refs=(3,),sec="3",table="Таблица 10",
  special="# этопозид, # ифосфамид — off-label")
R("C3","терапия злокачественных ГКО яичка (IA другая/смешанная, IB–IC)","PE ×2",
  [d("Цисплатин","20 мг/м² в сутки (100 мг/м² за курс)","в/в инфузия 1 ч","дни 1–5","каждые 21 день"),
   d("Этопозид","100 мг/м² в сутки (300 мг/м² за курс)","в/в инфузия 1 ч (до цисплатина)","дни 1, 2, 3")],
  refs=(13,),sec="3",table="Таблица 9; Таблица 3",
  special="# этопозид — off-label")
R("C3","терапия злокачественных ГКО яичка (IIA)","PEI ×2",
  [d("Цисплатин","20 мг/м² в сутки","в/в инфузия 1 ч","дни 1–5","каждые 21 день"),
   d("Этопозид","100 мг/м² в сутки","в/в инфузия 1 ч (до цисплатина)","дни 1, 2, 3"),
   d("Ифосфамид","1500 мг/м² в сутки на фоне месны","в/в инфузия 22 ч","дни 1–5")],
  refs=(13,),sec="3",table="Таблица 10; Таблица 3",special="# этопозид, # ифосфамид — off-label; повторная оценка опухоли, при PR — 2nd look")
R("C3","терапия злокачественных ГКО яичка (IIB–IIID)","PEI ×3 (CR → 1×PEI)",
  [d("Цисплатин","20 мг/м² в сутки","в/в инфузия 1 ч","дни 1–5","каждые 21 день"),
   d("Этопозид","100 мг/м² в сутки","в/в инфузия 1 ч (до цисплатина)","дни 1, 2, 3"),
   d("Ифосфамид","1500 мг/м² в сутки на фоне месны","в/в инфузия 22 ч","дни 1–5")],
  refs=(13,),sec="3",table="Таблица 3",
  special="# этопозид, # ифосфамид — off-label; пациенты с инвазией опухоли в лимфоузлы или сосуды лечатся по высокой группе риска (с ифосфамидом)")
R("C4","терапия злокачественных ГКО яичников (FIGO Ic, IIa–IIb)","PE ×2",
  [d("Цисплатин","20 мг/м² в сутки","в/в инфузия 1 ч","дни 1–5","каждые 21 день"),
   d("Этопозид","100 мг/м² в сутки","в/в инфузия 1 ч (до цисплатина)","дни 1, 2, 3")],
  refs=(13,),sec="3",table="Таблица 9; Таблица 4",special="# этопозид — off-label")
R("C4","терапия злокачественных ГКО яичников (FIGO IIc)","PEI ×3 + PEI ×1",
  [d("Цисплатин","20 мг/м² в сутки","в/в инфузия 1 ч","дни 1–5","каждые 21 день"),
   d("Этопозид","100 мг/м² в сутки","в/в инфузия 1 ч (до цисплатина)","дни 1, 2, 3"),
   d("Ифосфамид","1500 мг/м² в сутки на фоне месны","в/в инфузия 22 ч","дни 1–5")],
  refs=(13,),sec="3",table="Таблица 4",special="# этопозид, # ифосфамид — off-label")
R("C4","предоперационная ХТ (FIGO IIIa–IV)","PEI ×3 → удаление остаточного компонента опухоли → PEI ×1",
  [d("Цисплатин","20 мг/м² в сутки","в/в инфузия 1 ч","дни 1–5","каждые 21 день"),
   d("Этопозид","100 мг/м² в сутки","в/в инфузия 1 ч (до цисплатина)","дни 1, 2, 3"),
   d("Ифосфамид","1500 мг/м² в сутки на фоне месны","в/в инфузия 22 ч","дни 1–5")],
  refs=(13,),sec="3",table="Таблица 4",
  special="# этопозид, # ифосфамид — off-label; при гепатоидной или эндометриоидной дифференцировке ОЖМ терапия проводится по более высокой группе риска (при стадиях III и IV — как для высокой группы риска внегонадных ГКО)")
# 2nd line
R("C5","химиотерапия второй линии (рефрактерность/рецидив ГКО)","CarboPET (высокодозная последовательная ХТ с трансплантацией ПСКК)",
  [d("Карбоплатин","400 мг/м²","внутривенно за 3 часа","курс 1: дни −5, −4, −3"),
   d("Этопозид","500 мг/м²","внутривенно за 3 часа","курс 1: дни −5, −4, −3; курс 2 (тиотепа+этопозид): дни −5, −4, −3"),
   d("ПСКК (периферические стволовые кроветворные клетки-предшественники)","2–4×10⁶ CD34+/кг","внутривенно за 1 час","день 0 каждого курса"),
   d("Тиотепа","300 мг/м²","внутривенно за 3 часа","курс 2 (на 28-е сутки от начала 1-го курса): дни −5, −4, −3")],
  refs=(13,),sec="Приложение А3.1",table="Таблицы 11–12",
  special="# карбоплатин — off-label; высокодозная ХТ с поддержкой аутологичных ПСКК; доступна детям до 10 лет; выбор режима — после обсуждения с Федеральным центром")
R("C5","химиотерапия второй линии (рефрактерность/рецидив ГКО)","TIP",
  [d("Паклитаксел","175 мг/м²","внутривенно за 3 часа","день 1"),
   d("Ифосфамид","1000 мг/м² на фоне профилактики месной 500 мг/м²","внутривенно за 1 час","дни 1–5"),
   d("Цисплатин","20 мг/м²","внутривенно за 1 час","дни 1–5")],
  uur="C",udd=5,refs=(14,31),sec="Приложение А3.1",table="Таблица 15",
  special="# паклитаксел — off-label; тайминг между курсами 21 день")
R("C5","химиотерапия второй линии (рефрактерность/рецидив ГКО)","TI-CE (индукция TI + высокодозная ХТ CE с ПСКК)",
  [d("Паклитаксел","200 мг/м²","внутривенно за 24 часа","этап 1 (индукция, 2 цикла с аферезом ПСКК): день 1; интервал между курсами 14 дней"),
   d("Ифосфамид","2000 мг/м² на фоне профилактики уромитексаном","внутривенно за 3 часа","этап 1: дни 2–4"),
   d("Этопозид","400 мг/м²","внутривенно за 1 час","этап 2 (3 цикла высокодозной ХТ с поддержкой аутологичных ПСКК): дни −4…−2; интервал 21–28 дней"),
   d("Карбоплатин","AUC=8","внутривенно за 1 час","этап 2: дни −4…−2")],
  uur="C",udd=5,refs=(14,),sec="Приложение А3.1",table="Таблицы 13–14",
  special="# паклитаксел, # ифосфамид, # этопозид, # карбоплатин — off-label; целевое количество клеток ≥2×10⁶ CD34+/кг на каждую реинфузию")
R("C5","химиотерапия второй линии (рефрактерность/рецидив ГКО)","Гемцитабин + Паклитаксел",
  [d("Гемцитабин","1000 мг/м²","внутривенно за 30 минут","дни 1, 8, 15","каждые 28 дней"),
   d("Паклитаксел","100 мг/м²","внутривенно за 1 час","дни 1, 8, 15")],
  uur="C",udd=5,refs=(15,),sec="Приложение А3.1",table="Таблица 16",
  special="# гемцитабин, # паклитаксел — off-label")
R("C5","химиотерапия второй линии (рефрактерность/рецидив ГКО)","Гемцитабин + Паклитаксел + Оксалиплатин (GemPOx)",
  [d("Гемцитабин","800 мг/м²","внутривенно за 30 минут","дни 1, 8","каждые 21 день"),
   d("Паклитаксел","80 мг/м²","внутривенно за 1 час","дни 1, 8"),
   d("Оксалиплатин","130 мг/м²","внутривенно за 2 часа","день 1")],
  uur="C",udd=5,refs=(32,),sec="Приложение А3.1",table="Таблица 17",
  special="# гемцитабин, # паклитаксел, # оксалиплатин — off-label")
R("C5","химиотерапия второй линии (рефрактерность/рецидив ГКО, дети до 10 лет)","JEB (карбоплатин + этопозид + блеомицин)",
  [d("Карбоплатин","600 мг/м²","внутривенно за 3 часа","день 2","каждые 21 день"),
   d("Этопозид","120 мг/м²","внутривенно за 3 часа","дни 1–3"),
   d("Блеомицин","15 мг/м²","внутривенно за 1 час","день 3")],
  uur="C",udd=5,refs=(36,),sec="Приложение А3.1",table="Таблица 19",
  special="# карбоплатин — off-label; решение о выборе режима принимается индивидуально после обсуждения с Федеральным центром")

with open(f"output-cohort/{DOC}.cohorts.json","w") as f: json.dump(cohorts,f,ensure_ascii=False,indent=1)
with open(f"output-cohort/{DOC}.regimens.json","w") as f: json.dump(rows,f,ensure_ascii=False,indent=1)
for c in cohorts: audit.cohort(DOC,c)
for r in rows: audit.regimen(DOC,r)
audit.event(DOC,"phase2-done",f"{len(rows)} regimens, {len(cohorts)} cohorts")
print(f"{DOC}: {len(cohorts)} cohorts, {len(rows)} regimens written")
