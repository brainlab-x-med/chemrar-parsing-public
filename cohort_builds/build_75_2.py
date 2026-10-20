#!/usr/bin/env python3
"""Build 75_2 (Опухоли слюнных желез у детей) cohorts + regimens."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import json, audit

DOC="75_2"
audit.event(DOC,"phase2-start","75_2 Опухоли слюнных желез (дети): cohort-first extraction")

DISEASE={
 "name":"Опухоли слюнных желез у детей",
 "icd10":"C07, C08",
 "histology_type":"злокачественные эпителиальные опухоли: мукоэпидермоидная карцинома, аденокистозная карцинома, ацинарноклеточная карцинома, секреторная карцинома (ETV6-NTRK3 >90%, ETV6-RET 2–5%), микросекреторная аденокарцинома, полиморфная аденокарцинома, внутрипротоковая карцинома, рак протоков слюнных желез, миоэпителиальная карцинома, эпителиально-миоэпителиальная карцинома и др.",
}

cohorts=[
 {"cohort_id":"C1","disease":DISEASE,"stage":"секреторная карцинома при неоперабельной опухоли и/или отдалённых метастазах; случаи, когда опции хирургического лечения и лучевой терапии исчерпаны","resectability":"неоперабельные/метастатические",
  "clinical_situation":"Молекулярно-направленная терапия по результатам федерального консилиума после молекулярно-генетического исследования (конкретные препараты и дозы в документе не приведены)","ecog":None,
  "biomarkers":["ETV6-NTRK3 перестройка","ETV6-RET перестройка","ETV6-MET перестройка"],"treatment_stages":["молекулярно-направленная терапия (по решению консилиума)"],"source":{"section":"3.3"}},
]

rows=[]
def R(cid,line,rtype,name,drugs,uur="C",udd=5,refs=(),sec="3.3",table=None,special="",maint=None,**ind):
    st=ind.get("stage",next((c["stage"] for c in cohorts if c["cohort_id"]==cid),None))
    ec=ind.get("ecog",next((c["ecog"] for c in cohorts if c["cohort_id"]==cid),None))
    bm=ind.get("biomarkers",next((c["biomarkers"] for c in cohorts if c["cohort_id"]==cid),[]))
    rows.append({"cohort_id":cid,"disease":DISEASE,
      "treatment":{"line_stage":line,"therapy_type":rtype,"regimen_name":name},
      "drugs":drugs,"indications":{"stage":st,"ecog":ec,"biomarkers":bm},
      "evidence":{"uur":uur,"udd":udd},
      "source":{"page":None,"section":sec,"table":table,"references":[str(x) for x in refs],
                "citation":None if not refs else CITE.get(str(refs[0]))},
      "special_conditions":special,"maintenance_therapy":maint})

CITE={
 "6":"Yoshida E.J. et al. Salivary gland malignancies in children // Int J Pediatr Otorhinolaryngol. 2014;78(2):174–178",
 "7":"Zamani M. et al. Survival and characteristics of pediatric salivary gland cancer: A systematic review and meta-analysis // Pediatr Blood Cancer. 2019;66(3)",
 "10":"Skálová A., Hyrcza M.D., Leivo I. Update from the 5th Edition of the WHO Classification of Head and Neck Tumors: Salivary Glands // Head Neck Pathol. 2022;16(1):40–53",
 "27":"Kim H.J., Kim J.S. Ultrasound-guided core needle biopsy in salivary glands: A meta-analysis // Laryngoscope. 2018;128(1):118–125",
 "28":"Romano E.B. et al. Fine-needle aspiration with selective use of core needle biopsy of major salivary gland tumors // Laryngoscope. 2017;127(11):2522–2527",
 "39":"Surun A. et al. Salivary gland carcinoma in children and adolescents: The EXPeRT/PARTNER diagnosis and treatment recommendations // Pediatr Blood Cancer. 2021;68(S4)",
 "40":"Wang X. et al. Management of salivary gland carcinomas — a review. 2017;8(3):3946–3956",
}
rows[0] if rows else None

R("C1","молекулярно-направленная терапия при исчерпанных опциях хирургии и ЛТ",
  ["таргетная терапия (молекулярно-направленная)","химиотерапия (по решению федерального консилиума)"],
  "Молекулярно-направленная терапия по результатам молекулярно-генетического исследования",
  [],
  uur="C",udd=5,refs=(6,27,28,39,40),sec="3.3",
  special="ГЭП: в документе не названы конкретные препараты, дозы и схемы — назначение только по результатам федерального онкологического консилиума после поиска молекулярных мишеней (секреторная карцинома: ETV6-NTRK3 >90%); химиотерапия может быть рекомендована консилиумом")
# fix citation after CITE defined
rows[-1]["source"]["citation"]=CITE["6"]

with open(f"output-cohort/{DOC}.cohorts.json","w") as f: json.dump(cohorts,f,ensure_ascii=False,indent=1)
with open(f"output-cohort/{DOC}.regimens.json","w") as f: json.dump(rows,f,ensure_ascii=False,indent=1)
for c in cohorts: audit.cohort(DOC,c)
for r in rows: audit.regimen(DOC,r)
audit.event(DOC,"phase2-done",f"{len(rows)} regimens, {len(cohorts)} cohorts")
print(f"{DOC}: {len(cohorts)} cohorts, {len(rows)} regimens written")
