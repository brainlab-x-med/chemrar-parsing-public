#!/usr/bin/env python3
"""Build 74_2 (Рак щитовидной железы, дети) cohorts + regimens."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import json, audit

DOC="74_2"
audit.event(DOC,"phase2-start","74_2 Рак щитовидной железы (дети): cohort-first extraction")

DISEASE={
 "name":"Рак щитовидной железы",
 "icd10":"C73",
 "histology_type":"дифференцированный РЩЖ (папиллярный рак 8260/3, фолликулярная карцинома 8330/3), медуллярная карцинома 8345/3 (в т.ч. high grade), анапластический (недифференцированный) рак; карциномы с неопределённого гистогенеза (склерозирующая мукоэпидермоидная 8430/3, криброформно-морулярная 8201/3)",
}

def d(inn,dose,route,sched=None,freq=None,mx=None):
    return {"inn":inn,"dose":dose,"route":route,"schedule":sched,"cycle_frequency":freq,"max_cycles":mx}

CITE={
 "3":"Поляков В.Г. Опухоли головы и шеи у детей // Опухоли головы и шеи. 5-е изд. / под ред. А.И. Пачеса. 2013. P. 454–473",
 "4":"Детская онкология. Национальное руководство / под ред. М.Д. Алиева и др. М.: Практическая медицина, 2012. 684 p.",
 "22":"Francis G.L., Waguespack S.G., Bauer A.J., et al. Management Guidelines for Children with Thyroid Nodules and Differentiated Thyroid Cancer // Thyroid. 2015;25(7):716–759",
 "26":"Verburg F.A., van Santen H., Luster M. Pediatric papillary thyroid cancer: current management challenges // Onco Targets Ther",
 "57":"Radakrishnan A. et al. Hypocalcemia prevention and management after thyroidectomy in children: a systematic review // J Pediatr",
 "58":"Waguespack S.G. et al. The successful use of sorafenib to treat pediatric papillary thyroid carcinoma // Thyroid",
 "59":"Iyer P., Mayer J.L.R., Ewig J.M. Response to sorafenib in a pediatric patient with papillary thyroid carcinoma with diffuse nodular pulmonary disease",
 "60":"Kraft I.L. et al. Outcomes of children and adolescents with advanced hereditary medullary thyroid carcinoma treated with vandetanib",
 "61":"Spinelli C. et al. Surgical management of medullary thyroid carcinoma in pediatric age",
 "62":"Диагностика и лечение медуллярного рака щитовидной железы. Национальные клинические рекомендации // Опухоли головы и шеи",
 "65":"Rivkees S.A. et al. The treatment of differentiated thyroid cancer in children: Emphasis on surgical approach and radioactive iodine therapy",
 "70":"Mhiri A. et al. Differentiated Thyroid Cancer in Children: The Contribution of Radioiodine Therapy. 2015",
 "71":"Lin J. Der et al. The efficacy of radioactive iodine for the treatment of well-differentiated thyroid cancer with distant metastases",
 "79":"Martucci C., Madafferi S., Crocoli A., et al. Intraoperative Neuromonitoring for pediatric thyroid surgery",
 "82":"Mahajan P., Dawrant J., Kheradpour A., et al. Response to Lenvatinib in pediatric radioiodine-refractory differentiated thyroid carcinoma",
 "84":"Reiners C., Biko J., Haenscheid H., et al. Twenty-five years after Chernobyl: outcome of radioiodine treatment in children and adolescents",
 "85":"Lebbink C.A., Links T.P., Czarniecka A., et al. Radioiodine therapy guidelines",
}

cohorts=[
 {"cohort_id":"C1","disease":DISEASE,"stage":"ДРЩЖ высокой и промежуточной группы риска прогрессирования после тиреоидэктомии (или близкой к ней операции); прогрессирование","resectability":None,
  "clinical_situation":"Радиойодтерапия/радиойодаблация натрия йодидом [131I]","ecog":None,
  "biomarkers":[],"treatment_stages":["радиойодтерапия после операции"],"source":{"section":"3.4"}},
 {"cohort_id":"C1a","parent":"C1","disease":DISEASE,"stage":"ДРЩЖ с метастазами в лёгких","resectability":None,
  "clinical_situation":"Радиойодтерапия в качестве первой линии","ecog":None,
  "biomarkers":[],"treatment_stages":["радиойодтерапия"],"source":{"section":"3.4"}},
 {"cohort_id":"C2","disease":DISEASE,"stage":"рецидивный неоперабельный или метастатический радиойодрефрактерный ДРЩЖ при неэффективности РЙТ, при прогрессировании и/или жизнеугрожающем состоянии","resectability":"нерезектабельный/метастатический",
  "clinical_situation":"Таргетная терапия ленватинибом","ecog":None,
  "biomarkers":[],"treatment_stages":["таргентная терапия (радиойодрефрактерный ДРЩЖ)"],"source":{"section":"3.2"}},
 {"cohort_id":"C2a","parent":"C2","disease":DISEASE,"stage":"радиойодрефрактерный ДРЩЖ, прогрессирующий на стандартных режимах таргетной терапии","resectability":None,
  "clinical_situation":"Комплексное геномное секвенирование для выбора молекулярно-ориентированной терапии (RET, NTRK)","ecog":None,
  "biomarkers":["мутации RET-протоонкогена","слияния в гене NTRK"],"treatment_stages":["таргентная терапия по молекулярным мишеням"],"source":{"section":"3.2"}},
 {"cohort_id":"C3","disease":DISEASE,"stage":"МРЩЖ с отдалёнными метастазами, оперативное лечение невозможно","resectability":"неоперабельный",
  "clinical_situation":"Консервативное паллиативное лечение вандетанибом","ecog":None,
  "biomarkers":["мутация RET"],"treatment_stages":["паллиативная таргетная терапия"],"source":{"section":"3.2"}},
 {"cohort_id":"C4","disease":DISEASE,"stage":"все пациенты после ТЭ/оперативного лечения ДРЩЖ и МРЩЖ (послеоперационный период; после РЙТ)","resectability":None,
  "clinical_situation":"Супрессивная терапия левотироксином натрия (СТТ); заместительная терапия после МРЩЖ — пожизненно","ecog":None,
  "biomarkers":[],"treatment_stages":["супрессивная/заместительная гормональная терапия"],"source":{"section":"7.2"}},
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

R("C1","радиойодтерапия после тиреоидэктомии (высокая и промежуточная группа риска прогрессирования)",["радиойодтерапия"],
  "Натрия йодид [131I] (радиойодаблация)",
  [d("Натрия йодида [131I] раствор","послеоперационная РЙТ: 30–100 мКи; повторные лечебные курсы: 100–200 мКи (редко до 300 мКи); в немецком протоколе — 50 МБк/кг для абляции остаточной ткани и 100 МБк/кг для лечения метастазов","перорально","рекомендуемые сроки — до 6 месяцев после хирургического этапа; интервал между повторными курсами около одного года")],
  uur="C",udd=4,refs=(22,),sec="3.4",
  special="# натрия йодид [131I] — off-label (по тексту помечен #); перед РЙТ стимуляция ТТГ >30 мМЕ/л (отмена левотироксина за 2 недели или рчТГ), йод-ограниченная диета 1–2 недели; супрессивная терапия левотироксином натрия с 3-го дня после приёма 131I")
R("C1a","радиойодтерапия первой линии при метастазах в лёгких",["радиойодтерапия"],
  "Натрия йодид [131I] (метастазы в лёгких)",
  [d("Натрия йодида [131I] раствор","активность по группе риска (30–200 мКи)","перорально","повторные курсы с интервалом ~12 месяцев после оценки ответа")],
  uur="C",udd=4,refs=(84,),sec="3.4",
  special="# натрия йодид [131I]; перед повторным лечением диффузных метастазов в лёгких — исследование функции лёгких; осторожность у детей, ранее получавших препараты с лёгочной токсичностью (блеомицин)")
R("C2","таргетная терапия радиойодрефрактерного ДРЩЖ при рецидиве/метастазах после неэффективности РЙТ",["таргетная терапия"],
  "Ленватиниб",
  [d("Ленватиниб","14 мг/сут","per os","ежедневно до прогрессирования или неприемлемой токсичности")],
  uur="C",udd=4,refs=(82,),sec="3.2",
  special="# ленватиниб — off-label; предпочтителен у пациентов детского возраста из-за более значимого клинического ответа; назначается только при наличии прогрессирования; требуется заключение онкологического консилиума")
R("C3","паллиативная консервативная терапия МРЩЖ с отдалёнными метастазами (неоперабельного)",["таргетная терапия"],
  "Вандетаниб",
  [d("Вандетаниб","100–300 мг/м²/сут","per os","непрерывно, с паллиативной целью")],
  uur="C",udd=4,refs=(60,),sec="3.2",
  special="# вандетаниб — off-label; ингибитор протеинкиназ с активностью относительно VEGFR (VEGFR-2), EGFR и протоонкогена Ret")
R("C4","супрессивная терапия ДРЩЖ после операции и РЙТ; заместительная терапия после лечения МРЩЖ",["гормональная терапия"],
  "Левотироксин натрия",
  [d("Левотироксин натрия","2,5–3 мкг/кг веса (супрессивная терапия при ДРЩЖ); доза подбирается по уровню ТТГ","per os","утром, не менее чем за 1 час до еды; с 3-го дня после приёма натрия йодида [131I]"),
   d("Натрия йодида [131I] раствор","(см. режимы РЙТ выше)","перорально","—")],
  uur="C",udd=5,refs=(65,),sec="3.4",
  special="при МРЩЖ — пожизненная заместительная терапия левотироксином натрия",
  maint="Супрессивная терапия левотироксином натрия 2,5–3 мкг/кг/сут при ДРЩЖ; пожизненная заместительная терапия при МРЩЖ")

with open(f"output-cohort/{DOC}.cohorts.json","w") as f: json.dump(cohorts,f,ensure_ascii=False,indent=1)
with open(f"output-cohort/{DOC}.regimens.json","w") as f: json.dump(rows,f,ensure_ascii=False,indent=1)
for c in cohorts: audit.cohort(DOC,c)
for r in rows: audit.regimen(DOC,r)
audit.event(DOC,"phase2-done",f"{len(rows)} regimens, {len(cohorts)} cohorts")
print(f"{DOC}: {len(cohorts)} cohorts, {len(rows)} regimens written")
