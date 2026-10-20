#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pipeline build for doc 534_3 (Вторичное ЗНО головного мозга и мозговых оболочек)."""
import os
import sys, json, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit

DOC="534_3"; MD=f"output-cohort/{DOC}.md"

def load_bib():
    txt=open(MD,encoding="utf-8").read(); i=txt.rfind("## Список литературы"); bib={}; n=0
    for line in txt[i:].splitlines()[1:]:
        if line.startswith("- "): n+=1; bib[n]=line[2:].strip()
        elif bib and line.strip() and not line.startswith(("#","|")): break
    return bib
bib=load_bib()
def cite(refs):
    if not refs: return None
    m=re.match(r"\[?(\d+)",str(refs[0]))
    if not m: return None
    e=bib.get(int(m.group(1)))
    return re.sub(r"\s+"," ",e)[:300] if e else None

def D(inn,dose=None,route=None,sched=None,freq=None,mx=None):
    return {"inn":inn,"dose":dose,"route":route,"schedule":sched,"cycle_frequency":freq,"max_cycles":mx}

DIS={"name":"Вторичное злокачественное новообразование головного мозга и мозговых оболочек (метастазы в головной мозг, МГМ)","icd10":"C79.3","histology_type":"метастатическое поражение; гистология соответствует первичной опухоли (наиболее часто — немелкоклеточный рак лёгкого, меланома, рак молочной железы)"}

COHORTS=[
 {"cohort_id":"C1","parent":None,"disease":DIS,"stage":"первично выявленные бессимптомные МГМ (единичные/олгометастатические/множественные)","resectability":None,
  "clinical_situation":"НМРЛ с активирующими мутациями/транслокациями EGFR/ALK/ROS1/BRAF/NTRK — старт с таргетной терапии","ecog":None,
  "biomarkers":["EGFR ex19/ex21 (редкие ex18/ex20)","ALK","ROS1","BRAF V600E","NTRK"],"treatment_stages":["первая линия системной терапии"],"source":{"section":"3.3"}},
 {"cohort_id":"C2","parent":None,"disease":DIS,"stage":"бессимптомные МГМ при НМРЛ без мутаций EGFR/ALK/ROS1","resectability":None,
  "clinical_situation":"ИКТ-монотерапия при PD-L1>50% либо ХТ + ИКТ при PD-L1<50%","ecog":None,
  "biomarkers":["PD-L1 >50%","PD-L1 <50%"],"treatment_stages":["первая линия"],"source":{"section":"3.3"}},
 {"cohort_id":"C3","parent":None,"disease":DIS,"stage":"бессимптомные МГМ меланомы (в т.ч. BRAF-мутированная)","resectability":None,
  "clinical_situation":"ИКТ (ниволумаб+ипилимумаб) как предпочтительная 1-я линия независимо от статуса BRAF; при BRAF-мутации возможны ингибиторы BRAF/MEK","ecog":None,
  "biomarkers":["BRAF V600E"],"treatment_stages":["первая линия"],"source":{"section":"3.3"}},
 {"cohort_id":"C4","parent":None,"disease":DIS,"stage":"лептоменингеальное поражение (типы I–II, A–D)","resectability":None,
  "clinical_situation":"Лекарственное лечение по характеристикам первичной опухоли ± интратекальная терапия при цитологическом подтверждении","ecog":None,
  "biomarkers":[],"treatment_stages":["системная терапия ± интратекальная"],"source":{"section":"3.4"}},
 {"cohort_id":"C5","parent":None,"disease":DIS,"stage":"МГМ с неврологической симптоматикой (отёк, масс-эффект, гидроцефалия); радионекроз","resectability":None,
  "clinical_situation":"Стероидная и противоотёчная терапия; бевацизумаб при резистентном отёке/радионекрозе","ecog":None,
  "biomarkers":[],"treatment_stages":["симптоматическая терапия"],"source":{"section":"3.6"}},
]

R=[]
def reg(coh,line,name,drugs,refs,sec,uur=None,udd=None,stage=None,bio=None,spec="",tt=None,table=None):
    R.append({"cohort_id":coh,
      "disease":{"name":DIS["name"],"icd10":DIS["icd10"],"histology_type":DIS["histology_type"]},
      "treatment":{"line_stage":line,"therapy_type":tt or ["таргетная терапия"],"regimen_name":name},
      "drugs":drugs,
      "indications":{"stage":stage,"ecog":None,"biomarkers":bio if bio is not None else []},
      "evidence":{"uur":uur,"udd":udd},
      "source":{"page":None,"section":sec,"table":table,"references":refs,"citation":None},
      "special_conditions":spec,"maintenance_therapy":None})

S33="3.3"
reg("C1","1-я линия (бессимптомные МГМ, первичная системная терапия)","Осимертиниб (EGFR ex19del/L858R; редкие мутации ex18/ex20)",
    [D("Осимертиниб",None,"внутрь",None,None,None)],["17"],S33,uur="C",udd=5,
    stage="НМРЛ с мутациями EGFR (19, 21-е экзоны; редкие 18 и 20-е экзоны) с бессимптомными МГМ",
    bio=["EGFR"],spec="# off-label (ЖНВЛП-маркер в документе); дозы в документе не приведены — по КР «Рак лёгкого»")
reg("C1","1-я линия (бессимптомные МГМ)","Алектиниб (транслокация ALK)",
    [D("Алектиниб",None,"внутрь",None,None,None)],["17"],S33,uur="C",udd=5,
    stage="НМРЛ с транслокацией ALK, бессимптомные МГМ",bio=["ALK"],
    spec="дозы в документе не приведены")
reg("C1","1-я линия (бессимптомные МГМ)","Лорлатиниб (транслокация ALK)",
    [D("Лорлатиниб",None,"внутрь",None,None,None)],["17"],S33,uur="C",udd=5,
    stage="НМРЛ с транслокацией ALK, бессимптомные МГМ",bio=["ALK"],spec="дозы в документе не приведены")
reg("C1","1-я линия (бессимптомные МГМ)","Энтректиниб (транслокация ROS1 или NTRK)",
    [D("Энтректиниб",None,"внутрь",None,None,None)],["17"],S33,uur="C",udd=5,
    stage="НМРЛ с транслокацией ROS-1 или NTRK, бессимптомные МГМ",bio=["ROS1","NTRK"],spec="дозы в документе не приведены")
reg("C1","1-я линия (бессимптомные МГМ)","Дабрафениб + траметиниб (мутация BRAF V600E)",
    [D("Дабрафениб",None,"внутрь",None,None,None),
     D("Траметиниб",None,"внутрь",None,None,None)],
    ["17"],S33,uur="C",udd=5,stage="НМРЛ (и меланома) с мутацией BRAF V600E, бессимптомные МГМ",
    bio=["BRAF V600E"],spec="дозы в документе не приведены")
reg("C1","1-я линия (бессимптомные МГМ)","Афатиниб (редкие мутации EGFR в 18-м и 20-м экзонах)",
    [D("Афатиниб",None,"внутрь",None,None,None)],["17"],S33,uur="C",udd=5,
    stage="НМРЛ с редкими мутациями EGFR (экзоны 18, 20)",bio=["EGFR"],spec="дозы в документе не приведены")
reg("C2","1-я линия (бессимптомные МГМ)","Монотерапия ингибиторами иммунных контрольных точек (PD-L1 >50%)",
    [D("Ингибиторы иммунных контрольных точек, группа L01XC (конкретные МНН в документе не указаны)",None,None,None,None,None)],
    ["17"],S33,uur="C",udd=5,stage="НМРЛ без мутаций EGFR/ALK/ROS1, бессимптомные МГМ",
    bio=["PD-L1 >50%"],tt=["иммунотерапия"])
reg("C2","1-я линия (бессимптомные МГМ)","Системная химиотерапия в сочетании с ингибиторами иммунных контрольных точек (PD-L1 <50%)",
    [D("Ингибиторы иммунных контрольных точек, группа L01XC (конкретные МНН в документе не указаны)",None,None,None,None,None),
     D("Препараты химиотерапии (режим по КР «Рак лёгкого», в документе не детализирован)",None,None,None,None,None)],
    ["17"],S33,uur="C",udd=5,stage="НМРЛ без мутаций EGFR/ALK/ROS1, бессимптомные МГМ",
    bio=["PD-L1 <50%"],tt=["химиотерапия","иммунотерапия"])
reg("C3","1-я линия (бессимптомные МГМ)","Ниволумаб + ипилимумаб (меланома, независимо от статуса BRAF)",
    [D("Ниволумаб",None,"в/в",None,None,None),
     D("Ипилимумаб",None,"в/в",None,None,None)],
    ["17"],S33,uur="C",udd=5,stage="Бессимптомные МГМ меланомы",bio=["BRAF (любой статус)"],
    tt=["иммунотерапия"],spec="# off-label (маркер ** в документе); дозы в документе не приведены")
reg("C3","1-я линия (бессимптомные МГМ, BRAF-мутированная меланома)","Дабрафениб + траметиниб (ингибиторы BRAF и MEK)",
    [D("Дабрафениб",None,"внутрь",None,None,None),
     D("Траметиниб",None,"внутрь",None,None,None)],
    ["17"],S33,uur="C",udd=5,stage="Первично выявленные метастазы BRAF-мутированной меланомы в головной мозг",
    bio=["BRAF V600E"],tt=["таргетная терапия"],spec="дозы в документе не приведены")
reg("C4","терапия лептоменингеального поражения","Противоопухолевое лекарственное лечение ЛМП с учётом молекулярно-генетических характеристик первичной опухоли ± интратекальная терапия",
    [D("Препараты определяются первичной опухолью (в документе не детализированы)",None,None,None,None,None)],
    ["6"],S33,uur="C",udd=5,stage="Лептоменингеальное метастазирование (типы I–II; нейровизуализационные типы A–D)",
    spec="интратекальное введение рекомендуется только при цитологическом подтверждении ЛП; конкретные препараты/дозы интратекальной терапии в документе не приведены (gap)",
    tt=["химиотерапия","таргетная терапия","иммунотерапия"])
reg("C5","симптоматическая/противоотёчная терапия","Дексаметазон (стероидная терапия масс-эффекта/отёка)",
    [D("Дексаметазон","0,5–4 мг или больше (минимально необходимая доза)","внутрь или в/м","в 1–2 приёма с учётом циркадного ритма, максимум утром, последний приём не позднее 16–17 ч; отмена постепенно ≥2 недель","ежедневно",None)],
    ["13"],"3.6",uur="C",udd=3,stage="МГМ с неврологической симптоматикой (внутричерепная гипертензия, масс-эффект, гидроцефалия)",
    tt=["симптоматическая терапия"],spec="при обширном отёке — не менее чем за 24 часа до радиотерапии; H02AB02")
reg("C5","терапия радионекроза/резистентного отёка","Бевацизумаб (отёк мозга/радионекроз, резистентный к стандартной противоотёчной терапии)",
    [D("Бевацизумаб","5 мг/кг каждые 2 недели или 7,5 мг/кг каждые 3 недели","в/в","до регресса симптоматики или улучшения рентгенологической картины (обычно 4 введения)","каждые 2–3 недели","обычно 4 введения")],
    ["23"],"3.6",uur="C",udd=5,stage="МГМ с обширным отёком/радионекрозом после радиотерапии",
    tt=["таргетная терапия"],spec="# off-label (маркер # в документе); показания: противопоказания к стероидам, радионекроз ± локальный рецидив (ПЭТ КТ с тирозином/метионином), планируемая терапия ИКТ")

for r in R: r["source"]["citation"]=cite(r["source"]["references"])

with open(f"output-cohort/{DOC}.cohorts.json","w",encoding="utf-8") as f: json.dump(COHORTS,f,ensure_ascii=False,indent=1)
with open(f"output-cohort/{DOC}.regimens.json","w",encoding="utf-8") as f: json.dump(R,f,ensure_ascii=False,indent=1)

audit.event(DOC,"phase2-start","cohort-first extraction")
audit.read_block(DOC,f"{DOC}.md",809,930,"§3.3–3.6 лекарственное лечение")
for c in COHORTS: audit.cohort(DOC,c)
for r in R: audit.regimen(DOC,r)
audit.event(DOC,"phase2-done",f"{len(R)} regimens")

tot=len(R)
def cnt(fn): return sum(1 for r in R if fn(r))
print(json.dumps({"rows":tot,
 "disease.name":cnt(lambda r:r["disease"]["name"]),
 "disease.icd10":cnt(lambda r:r["disease"]["icd10"]),
 "histology":cnt(lambda r:r["disease"]["histology_type"]),
 "line_stage":cnt(lambda r:r["treatment"]["line_stage"]),
 "regimen_name":cnt(lambda r:r["treatment"]["regimen_name"]),
 "ind.stage":cnt(lambda r:r["indications"]["stage"]),
 "src.section":cnt(lambda r:r["source"]["section"]),
 "src.refs":cnt(lambda r:r["source"]["references"]),
 "src.citation":cnt(lambda r:r["source"]["citation"]),
 "drug.inn":cnt(lambda r:all(d["inn"] for d in r["drugs"])),
 "drug.dose":cnt(lambda r:all(d["dose"] for d in r["drugs"])),
 "drug.route":cnt(lambda r:all(d["route"] for d in r["drugs"])),
 "drug.schedule":cnt(lambda r:all(d["schedule"] for d in r["drugs"]))},ensure_ascii=False,indent=1))
print("GAPS:")
for r in R:
    miss=[]
    if not r["source"]["references"]: miss.append("refs/citation")
    for d in r["drugs"]:
        if not d["dose"]: miss.append("dose:"+d["inn"][:40])
        if not d["schedule"]: miss.append("schedule:"+d["inn"][:40])
    if miss: print("-",r["treatment"]["regimen_name"],"=>",miss)
