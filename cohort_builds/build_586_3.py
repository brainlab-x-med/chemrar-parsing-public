#!/usr/bin/env python3
"""Build 586_3 (Острые миелоидные лейкозы, дети) cohorts + regimens, audit events."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import json, audit

DOC = "586_3"
audit.event(DOC, "phase2-start", "586_3 Острые миелоидные лейкозы (дети): cohort-first extraction")

DISEASE = {
    "name": "Острые миелоидные лейкозы",
    "icd10": "C92.0, C92.3, C92.5, C92.6, C92.7, C92.8, C92.9, C93.0, C94.0, C94.2",
    "histology_type": "острый миелоидный лейкоз (включая миелоидную саркому, острый миеломоноцитарный, монобластный/моноцитарный лейкоз, острый мегакариобластный лейкоз); у детей с синдромом Дауна — транзиторный аномальный миелопоэз (ТАМ) и ОМЛ",
}

def d(inn, dose, route, sched=None, freq=None, mx=None):
    return {"inn": inn, "dose": dose, "route": route, "schedule": sched,
            "cycle_frequency": freq, "max_cycles": mx}

CITE = {
 "1": "Детская гематология / Под ред. А.Г. Румянцева, А.А. Масчана, Е.В. Жуковской. 2015. 656 p.",
 "2": "Pui C.-H. Childhood leukemias. 2012. 880 p.",
 "37": "Winestone L.E. et al. Disparities in pediatric acute myeloid leukemia (AML) clinical trial enrollment // Leuk. Lymphoma. 2019;60(9):2190–2198",
 "38": "Perel Y. et al. Treatment of childhood acute myeloblastic leukemia: Dose intensification improves outcome and maintenance therapy is of no benefit — French LAME Cooperative Group // Leukemia. 2005;19(12):2082–2089",
 "39": "Rasche M. et al. Successes and challenges in the treatment of pediatric acute myeloid leukemia: AML-BFM trials 1987–2012 // Leukemia. 2018;32(10):2167–2177",
 "40": "Шнейдер М.М. Эффективность риск-адаптированной терапии ОМЛ у детей... Дисс. д-ра мед. наук. 2009. 223 p.",
 "41": "Olmos-Jiménez R. et al. Practical aspects of the use of intrathecal chemotherapy // Farm Hosp. 2017;41(1):105–129",
 "42": "Creutzig U. et al. CNS irradiation in pediatric acute myeloid leukemia: Equal results by 12 or 18 Gy in studies AML-BFM98 and 2004 // Pediatr Blood Cancer. 2011;57(6):986–992",
 "43": "Stevens R.F. et al. Marked improvements in outcome with chemotherapy alone in paediatric AML: UK MRC 10th AML trial // Br. J. Haematol. 1998;101(1):130–140",
 "44": "Ravindranath Y. et al. Pediatric Oncology Group (POG) studies of AML: review of four consecutive childhood AML trials 1981–2000 // Leukemia. 2005;19(12):2101–2116",
 "45": "Kardos G. et al. Treatment strategy and results in children treated on three Dutch Childhood Oncology Group AML trials // Leukemia. 2005;19(12):2063–2071",
 "46": "Smith F.O. et al. Long-term results of children with AML: CCG 251, CCG 213 and CCG 2891 // Leukemia. 2005;19(12):2054–2062",
 "47": "Perel Y. et al. Maintenance therapy in childhood acute myeloid leukemia // Ann. Hematol. 2004;Suppl 1:S116–S119",
 "48": "Toyama D. et al. Successful Treatment of Pediatric Refractory/Relapsed AML with KIR-Ligand-Mismatched Cord Blood Transplant after FLAG-IDA Reinduction Therapy... Case Rep Hematol. 2020;2020",
 "49": "Hashmi K.U. et al. FLAG-IDA in the treatment of refractory/relapsed acute leukaemias: single centre study // J. Pak. Med. Assoc. 2005;55(6):234–238",
 "50": "Safaian N.N. et al. Sorafenib (Nexavar) induces molecular remission and regression of extramedullary disease in a patient with FLT3-ITD+ AML // Leuk. Res. 2009;33(2):348–350",
 "51": "Osone S. et al. Sorafenib Therapy for Pediatric AML with FLT3-ITD Mutations: 2 Case Reports // J. Pediatr. Hematol. Oncol. 2017;39(4):e199–e202",
 "52": "Crews K.R. et al. Interim comparison of a continuous infusion versus a short daily infusion of cytarabine given in combination with cladribine for pediatric AML // J Clin Oncol. 2002;20(20):4217–4224",
 "62": "Cornely O.A. et al. Posaconazole vs. fluconazole or itraconazole prophylaxis in patients with neutropenia // N Engl J Med. 2007;356:348–359",
 "68": "Tramsen L. et al. Lack of effectiveness of neutropenic diet... AML-BFM 2004 trial // J Clin Oncol. 2016;34(23):2776–2783",
 "69": "Milligan D.W. et al. Fludarabine and cytosine are less effective than standard ADE chemotherapy in high-risk AML... MRC AML-HR randomized trial // Blood. 2006;107(12):4614–4622",
 "70": "Gibson B.E.S. et al. Results of a randomized trial in children with Acute Myeloid Leukaemia: Medical Research Council AML12 trial // Br. J. Haematol. 2011;155(3):366–376",
 "72": "Creutzig U. et al. Improved treatment results in high-risk pediatric AML after intensification with high-dose cytarabine and mitoxantrone: AML-BFM 93 // J Clin Oncol. 2001;19(10):2705–2713",
 "74": "Uffmann M. et al. Therapy reduction in patients with Down syndrome and myeloid leukemia: the international ML-DS 2006 trial // Blood. 2017;129(25):3314–3321",
 "82": "Uffmann M., Rasche M., Zimmermann M., et al. Therapy reduction in patients with Down syndrome and myeloid leukemia: the international ML-DS 2006 trial // Blood. 2017;129(25):3314–3321",
 "84": "Инструкция по медицинскому применению лекарственного препарата Венклекста. ГРЛС. Доступ от 17.04.2023",
 "85": "Omima M. et al. FLAG/FLAG-IDA regimen for children with relapsed/refractory acute leukemia in the era of targeted novel therapies // J Oncol Pharm Pract. 2019;25(8):1831–1838",
 "86": "NCCN Clinical Practice Guidelines in Oncology (NCCN Guidelines) Acute Myeloid Leukemia. Version 2.2023",
 "87": "Heuser M. et al. Acute myeloid leukaemia in adult patients: ESMO Clinical Practice Guidelines. Ann Oncol. 2020",
 "89": "Попа А.В., Горохова Е.В., Флейшман Е.В. и др. Эпигенетическая терапия – важная составляющая в лечении детей, больных ОМЛ // Клиническая онкогематология. 2011;4(1):20–26",
 "90": "Попа А.В., Немировченко В.С., Флейшман Е.В. и др. Ингибиторы гистондеацетилазы и ДНК-метилтрансферазы в лечении детей, больных ОМЛ // Рос. журн. детской гематологии и онкологии. 2016;3(4):48–54",
 "91": "Попа А.В., Тиганова О.А., Сокова О.И. и др. Значение эпигенетической терапии в лечении детей, больных ОМЛ // Вопросы онкологии, гематологии, иммунологии. 2025;24(1)",
 "96": "Creutzig U., Zimmermann M., Ritter J., Reinhardt D., et al. Treatment strategies and long-term results in pediatric patients treated in four consecutive AML-BFM trials. Leukemia. 2005;19:2030–2042",
 "97": "Rasche M., Zimmermann M., Borschel L., et al. Successes and challenges in the treatment of pediatric AML: AML-BFM trials 1987–2012 // Leukemia. 2018;32:2167–2177",
 "98": "Trabal A., Gibson A., HeM J., et al. Venetoclax for Acute Myeloid Leukemia in Pediatric Patients: A Texas Medical Center Experience // Cancers. 2023;15:1983–1999",
 "99": "Penel-Page M., Plesa A., Girard S., et al. Association of fludarabine, cytarabine, and fractionated gemtuzumab followed by HSCT for first-line refractory AML in children // Pediatr Blood Cancer. 2020;67:e28305",
 "100": "Coope T.M., Franklin J., Gerbing R.B. et al. MD15AAML03P1, a Pilot Study of the Safety of Gemtuzumab Ozogamicin in Combination With Chemotherapy for Newly Diagnosed Childhood AML // Cancer. 2012;118(3):579–769",
 "101": "Creutzig U., Zimmermann M., Bourquin J-P. et al. Favorable outcome in infants with AML after intensive first- and second-line treatment: an AML-BFM study group report // Leukemia. 2012;26:654–661",
 "102": "Creutzig U., Zimmermann M., Lehrnbecher T., et al. Less toxicity by optimizing chemotherapy... results of AML-BFM 98 // J Clin Oncol. 2006;24:4499–506",
 "103": "Tavil B., Aytac S., Balcı Y.I. et al. Fludarabine, cytarabine, G-CSF, and idarubicin (FLAG-IDA) for children with poor-prognosis acute leukemia: the Hacettepe experience // Pediatr Hematol Oncol. 2010;27(7):517–528",
 "104": "Rubnitz J.E., Inaba H., Dahl G. et al. Minimal Residual Disease-Directed Therapy for Childhood AML: Results of the AML02 Multicenter Trial // Lancet Oncol. 2010;11(6):543–552",
 "180": "McCall D. et al. Gilteritinib combination therapies in pediatric patients with FLT3-mutated AML // Blood Advances. 2021;5(23):5215–5219",
 "181": "Selected schedules in the therapy of childhood cancers, 1st ed. / G. Henze, H. Weinberger; Baxter Oncology GmbH – Berlin, 2012. 125 p.",
 "182": "Диагностика и лечение острого миелоидного лейкоза у детей / И.И. Калинина, А.А. Масчан, Ю.В. Ольшанская [и др.]; ФГБУ НМИЦ ДГОИ им. Дмитрия Рогачева. М.: 2021. 104 с.",
 "183": "Aplenc R., Alonzo T.A., Gerbing R.B., et al. Safety and efficacy of gemtuzumab ozogamicin in combination with chemotherapy for pediatric AML: COG report // J Clin Oncol. 2008;26(14):2390–3295",
 "184": "LeBlanc F.R. et al. Clinical outcomes of hypomethylating agents and venetoclax in newly diagnosed unfit and relapsed/refractory paediatric, adolescent and young adult AML // Br J Haematol. 2024;205(3):1055–1066",
 "185": "Badawi M. et al. Dosing of Venetoclax in Pediatric Patients with Relapsed AML: Analysis of Developmental Pharmacokinetics... // Clin Ther. 2024",
}

cohorts = [
 {"cohort_id":"C1","disease":DISEASE,"stage":"впервые выявленный ОМЛ (дети)","resectability":None,
  "clinical_situation":"Индукция ремиссии (курс индукции с последующей консолидацией; для высокой группы риска — алло-ТГСК)","ecog":None,
  "biomarkers":[],"treatment_stages":["индукция ремиссии"],"source":{"section":"3.1"}},
 {"cohort_id":"C1a","parent":"C1","disease":DISEASE,"stage":"ОМЛ с inv(16)","resectability":None,
  "clinical_situation":"Индукция AM36E / консолидация HA, haM 24","ecog":None,"biomarkers":["inv(16) (CBF::MYH11)"],
  "treatment_stages":["индукция","консолидация"],"source":{"section":"3.1"}},
 {"cohort_id":"C1b","parent":"C1","disease":DISEASE,"stage":"ОМЛ с inv(16) и t(8;21)","resectability":None,
  "clinical_situation":"Индукция ADEGO / консолидация haMGO","ecog":None,"biomarkers":["inv(16) (CBF::MYH11)","t(8;21) (RUNX1::RUNX1T1)"],
  "treatment_stages":["индукция","консолидация"],"source":{"section":"3.1"}},
 {"cohort_id":"C2","disease":DISEASE,"stage":"ОМЛ после окончания индукции ремиссии (все пациенты)","resectability":None,
  "clinical_situation":"Консолидационная терапия, 3–4 курса на основе высоких доз цитарабина","ecog":None,"biomarkers":[],
  "treatment_stages":["консолидация (курсы 1–4)"],"source":{"section":"3.1"}},
 {"cohort_id":"C3","disease":DISEASE,"stage":"ОМЛ при невозможности проведения интенсивной ПХТ","resectability":None,
  "clinical_situation":"Таргетная терапия венетоклакс ± децитабин","ecog":None,"biomarkers":[],
  "treatment_stages":["таргетная терапия вместо интенсивной ХТ"],"source":{"section":"3.1"}},
 {"cohort_id":"C4","disease":DISEASE,"stage":"ОМЛ после курса индукции ремиссии (с целью более глубокой ремиссии)","resectability":None,
  "clinical_situation":"Эпигенетическая терапия (вальпроевая кислота + ATRA ± децитабин по протоколу)","ecog":None,"biomarkers":[],
  "treatment_stages":["после индукции"],"source":{"section":"3.1"}},
 {"cohort_id":"C5","disease":DISEASE,"stage":"Все пациенты с ОМЛ (профилактика нейролейкоза; терапия при поражении ЦНС)","resectability":None,
  "clinical_situation":"Интратекальная терапия цитарабином (возрастные дозы)","ecog":None,"biomarkers":[],
  "treatment_stages":["профилактика/лечение нейролейкоза"],"source":{"section":"3.1"}},
 {"cohort_id":"C6","disease":DISEASE,"stage":"ОМЛ после завершения индукционной и консолидационной терапии по протоколу BFM-2004 и далее","resectability":None,
  "clinical_situation":"Поддерживающая терапия (по решению с учётом пользы/риска)","ecog":None,"biomarkers":[],
  "treatment_stages":["поддерживающая терапия"],"source":{"section":"3.1"}},
 {"cohort_id":"C7","disease":DISEASE,"stage":"Первичная рефрактерность ОМЛ и рецидив ОМЛ","resectability":None,
  "clinical_situation":"Интенсивная высокодозная ПХТ с целью ремиссии и последующей алло-ТГСК","ecog":None,"biomarkers":[],
  "treatment_stages":["терапия рецидивов/рефрактерности"],"source":{"section":"3.2"}},
 {"cohort_id":"C7a","parent":"C7","disease":DISEASE,"stage":"Рецидив/рефрактерность ОМЛ при невозможности интенсивной ХТ","resectability":None,
  "clinical_situation":"Таргетная терапия венетоклакс + децитабин","ecog":None,"biomarkers":[],
  "treatment_stages":["терапия рецидивов/рефрактерности"],"source":{"section":"3.2"}},
 {"cohort_id":"C8","disease":DISEASE,"stage":"ОМЛ с мутацией гена FLT3-ITD (рецидив/рефрактерность)","resectability":None,
  "clinical_situation":"Таргетная терапия ингибиторами FLT3 (сорафениб, гилтеритиниб)","ecog":None,
  "biomarkers":["FLT3-ITD мутация"],"treatment_stages":["таргетная терапия"],"source":{"section":"3.2"}},
 {"cohort_id":"C9","disease":DISEASE,"stage":"Рецидив/рефрактерность ОМЛ (альтернативная опция)","resectability":None,
  "clinical_situation":"Индукция кладрибин+цитарабин с последующими 2 курсами DAV","ecog":None,"biomarkers":[],
  "treatment_stages":["терапия рецидивов/рефрактерности"],"source":{"section":"3.2"}},
 {"cohort_id":"C10","disease":DISEASE,"stage":"ОМЛ/МДС у детей с синдромом Дауна","resectability":None,
  "clinical_situation":"Терапия сниженными дозами по протоколу ML-DS-2006 (индукция AIE + 3 цикла консолидации AI/haM/HA)","ecog":None,
  "biomarkers":["мутация GATA1 (ТАМ)"],"treatment_stages":["индукция и консолидация сниженной интенсивности"],"source":{"section":"3.3"}},
 {"cohort_id":"C10a","parent":"C10","disease":DISEASE,"stage":"ТАМ у новорождённых с синдромом Дауна с жизнеугрожающими симптомами (лейкоцитоз >100 тыс/мкл, билирубин >83 ммоль/л и др.)","resectability":None,
  "clinical_situation":"Терапия низкими дозами цитарабина","ecog":None,"biomarkers":["мутация GATA1"],
  "treatment_stages":["терапия ТАМ"],"source":{"section":"3.3"}},
]

rows=[]
def R(cid,line,rtype,name,drugs,uur="C",udd=5,refs=(),sec="3.1",table=None,special="",maint=None,**ind):
    st=next((c["stage"] for c in cohorts if c["cohort_id"]==cid),None)
    ec=next((c["ecog"] for c in cohorts if c["cohort_id"]==cid),None)
    bm=next((c["biomarkers"] for c in cohorts if c["cohort_id"]==cid),None)
    stage=ind.get("stage",st); ecog=ind.get("ecog",ec); biom=ind.get("biomarkers",bm)
    rows.append({"cohort_id":cid,"disease":DISEASE,
        "treatment":{"line_stage":line,"therapy_type":rtype,"regimen_name":name},
        "drugs":drugs,
        "indications":{"stage":stage,"ecog":ecog,"biomarkers":biom},
        "evidence":{"uur":uur,"udd":udd},
        "source":{"page":None,"section":sec,"table":table,"references":[str(x) for x in refs],
                  "citation":CITE.get(str(refs[0])) if refs else None},
        "special_conditions":special,"maintenance_therapy":maint})

IND="индукция ремиссии, впервые выявленный ОМЛ"
# Индукция
R("C1",IND,["химиотерапия"],"AIE (цитарабин + идарубицин + этопозид)",
  [d("Цитарабин","100 мг/м² в сутки","в/в непрерывная инфузия","дни 1–2 постоянной инфузией; дни 3–8 30-минутной инфузией каждые 12 часов"),
   d("Идарубицин","# off-label; 12 мг/м² в сутки".replace("# off-label; ",""),"в/в 4-часовая инфузия","в течение 3 дней (по протоколу)"),
   d("Этопозид","150 мг/м²","в/в 1-часовая инфузия","дни 6, 7, 8")],
  uur="B",udd=2,refs=(68,181,182),special="# идарубицин — off-label")
R("C1",IND,["химиотерапия"],"АМ42Е (цитарабин + митоксантрон + этопозид)",
  [d("Цитарабин","100 мг/м²","в/в 1-часовая инфузия","каждые 12 часов, дни 1–7"),
   d("Митоксантрон","14 мг/м² в сутки","в/в 1-часовая инфузия","дни 2, 3, 4 (всего 3 дозы)"),
   d("Этопозид","100 мг/м²","в/в 1-часовая инфузия","дни 5, 6, 7 (всего 3 дозы)")],
  udd=5,refs=(182,),special="# митоксантрон, # этопозид — off-label")
R("C1a",IND,["химиотерапия"],"АМ36Е (для пациентов с inv16)",
  [d("Цитарабин","100 мг/м²","в/в 1-часовая инфузия","каждые 12 часов, дни 1–7"),
   d("Митоксантрон","12 мг/м² в сутки","в/в 1-часовая инфузия","дни 2, 3, 4 (всего 3 дозы)"),
   d("Этопозид","100 мг/м²","в/в 1-часовая инфузия","дни 5, 6, 7 (всего 3 дозы)")],
  udd=5,refs=(182,))
R("C1",IND,["химиотерапия"],"ADE (цитарабин + даунорубицин + этопозид)",
  [d("Цитарабин","100 мг/м² 2 раза в сутки","в/в","дни 1–10 (всего 20 доз в 1-й цикл), далее дни 1–8 (всего 16 доз)"),
   d("Даунорубицин","50 мг/м²","в/в","дни 1, 3, 5"),
   d("Этопозид","100 мг/м²","в/в","дни 1–5")],
  uur="B",udd=2,refs=(69,))
R("C1b",IND,["химиотерапия","иммунотерапия (иммунотоксин)"],"ADEGO (для inv16 и t(8;21))",
  [d("Цитарабин","100 мг/м²","в/в 1-часовая инфузия","каждые 12 часов, дни 1–10"),
   d("Даунорубицин","50 мг/м² в сутки","в/в","дни 2, 4, 6"),
   d("Этопозид","100 мг/м² в сутки","в/в","дни 2–6"),
   d("Гемтузумаб озогамицин","3 мг/м²","в/в 2-часовая инфузия","день 6")],
  udd=5,refs=(104,181,182))
CONS="консолидация после индукции (3–4 курса высоких доз цитарабина)"
R("C2",CONS+", курс 1",["химиотерапия"],"HAM 30",
  [d("Цитарабин","3000 мг/м²","в/в 3-часовая инфузия","каждые 12 часов, дни 1, 2, 3 (всего 6 доз)"),
   d("Митоксантрон","10 мг/м²","в/в 1-часовая инфузия","дни 2, 3, 4 (всего 3 дозы)")],refs=(72,175,181,182))
R("C2",CONS+", курс 1",["химиотерапия"],"HAM 20",
  [d("Цитарабин","3000 мг/м²","в/в 3-часовая инфузия","каждые 12 часов, дни 1, 2, 3 (всего 6 доз)"),
   d("Митоксантрон","10 мг/м²","в/в 30-минутная инфузия","дни 4, 5 (всего 2 дозы)")],refs=(96,175,181,182))
R("C1a",CONS+", курс 1 (inv16)",["химиотерапия"],"HA (высокодозный цитарабин)",
  [d("Цитарабин","3000 мг/м²","в/в 3-часовая инфузия","каждые 12 часов, дни 1, 2, 3 (всего 6 доз)")],refs=(74,181,182))
R("C2",CONS+", курс 1",["химиотерапия"],"AI",
  [d("Цитарабин","500 мг/м² в сутки","в/в 96-часовая инфузия","дни 1, 2, 3, 4"),
   d("Идарубицин","7 мг/м²","в/в 60-минутная инфузия","дни 3, 5 (всего 2 дозы)")],refs=(68,181,182))
R("C2",CONS+", курс 2",["химиотерапия"],"haM",
  [d("Цитарабин","1000 мг/м²","в/в 3-часовая инфузия","каждые 12 часов, 3 дня (всего 6 доз)"),
   d("Митоксантрон","10 мг/м²","в/в 30-минутная инфузия","2 дня (всего 2 дозы)")],refs=(68,175,181,182))
R("C2",CONS+", курс 2 (после HAM 20)",["химиотерапия"],"AI",
  [d("Цитарабин","500 мг/м² в сутки","в/в 96-часовая инфузия","дни 1, 2, 3, 4"),
   d("Идарубицин","7 мг/м²","в/в 60-минутная инфузия","дни 3, 5 (всего 2 дозы)")],refs=(68,181,182))
R("C2",CONS+", курс 2",["химиотерапия"],"НАЕ",
  [d("Цитарабин","3000 мг/м²","в/в 3-часовая инфузия","каждые 12 часов, дни 1, 2, 3 (всего 6 доз)"),
   d("Этопозид","125 мг/м²","в/в 2-часовая инфузия","дни 2, 3, 4, 5 (всего 4 дозы)")],refs=(68,181,182))
R("C1a",CONS+", курс 2 (inv16)",["химиотерапия"],"haM 24",
  [d("Цитарабин","1000 мг/м²","в/в 2-часовая инфузия","каждые 12 часов, дни 1, 2, 3, 4 (всего 8 доз)"),
   d("Митоксантрон","12 мг/м²","в/в 60-минутная инфузия","дни 3, 4 (всего 2 дозы)")],refs=(70,175,181,182))
R("C2",CONS+", курс 2 (высокий риск, запланирована ТГСК)",["химиотерапия"],"FLA",
  [d("Флударабин","30 мг/м²","в/в 30-минутная инфузия","дни 1–5 (всего 5 доз); интервал между началом инфузий флударабина и цитарабина — 4 часа"),
   d("Цитарабин","2000 мг/м²","в/в 3-часовая инфузия","каждые 24 часа, дни 1–5 (всего 10 доз)")],
  refs=(99,103,181,182),special="может применяться как с антрациклином, так и без него")
R("C1b",CONS+", курс 2 (inv16 и t(8;21))",["химиотерапия","иммунотерапия (иммунотоксин)"],"haMGO",
  [d("Цитарабин","1000 мг/м²","в/в 2-часовая инфузия","каждые 12 часов, 4 дня (всего 8 доз)"),
   d("Митоксантрон","12 мг/м²","в/в 60-минутная инфузия","дни 3–6 (всего 4 дозы)"),
   d("Гемтузумаб озогамицин","3 мг/м²","в/в 2-часовая инфузия","однократно в день 7")],
  refs=(183,),special="суммарная доза митоксантрона снижена до 24 мг из-за токсичности")
R("C2",CONS+", курс 3",["химиотерапия"],"НАЕ",
  [d("Цитарабин","3000 мг/м²","в/в 3-часовая инфузия","каждые 12 часов, дни 1, 2, 3 (всего 6 доз)"),
   d("Этопозид","125 мг/м²","в/в 2-часовая инфузия","дни 2, 3, 4, 5 (всего 4 дозы)")],refs=(68,97,181,182))
R("C2",CONS+", курс 3",["химиотерапия"],"haM",
  [d("Цитарабин","1000 мг/м²","в/в 3-часовая инфузия","каждые 12 часов, 3 дня (всего 6 доз)"),
   d("Митоксантрон","10 мг/м²","в/в 30-минутная инфузия","2 дня (всего 2 дозы)")],refs=(181,))
R("C1a",CONS+", курс 3 (inv16)",["химиотерапия"],"HA",
  [d("Цитарабин","3000 мг/м²","в/в 3-часовая инфузия","каждые 12 часов, дни 1, 2, 3 (всего 6 доз)")],refs=(74,181,182))
R("C2",CONS+", курс 3",["химиотерапия"],"AI",
  [d("Цитарабин","500 мг/м²","в/в 2-часовая инфузия каждые 12 часов","4 дня (всего 8 доз)"),
   d("Идарубицин","7 мг/м²","в/в 60-минутная инфузия","дни 3, 5 (всего 2 дозы)")],refs=(101,181,182))
R("C2",CONS+", курс 4 (если предусмотрен протоколом)",["химиотерапия"],"НАЕ",
  [d("Цитарабин","3000 мг/м²","в/в 3-часовая инфузия","каждые 12 часов, дни 1, 2, 3 (всего 6 доз)"),
   d("Этопозид","125 мг/м²","в/в 1-часовая инфузия","дни 2, 3, 4, 5 (всего 4 дозы)")],refs=(101,102,181,182))
R("C3","таргетная терапия при невозможности интенсивной ПХТ",["таргетная терапия"],"Венетоклакс ± децитабин",
  [d("Венетоклакс","титрация до целевой суточной дозы к 3-му дню (по массе: 10–20 кг → 250 мг; 20–30 кг → 350 мг; 30–45 кг → 500 мг; >45 кг → 800 мг/сут)","внутрь","с 1-го дня курса 1 раз в сутки, постепенно повышая дозу; 28 дней"),
   d("Децитабин","5 мг/м²","п/к (с местным обезболиванием лидокаин+прилокаин)","дни 1, 3, 5, 8, 10, 12, 15, 17, 19, 22, 24, 26 каждого цикла (первые 6 введений обязательны)")],
  udd=4,refs=(84,86,87,98,184,185),
  special="# венетоклакс, # децитабин — off-label; децитабин опционален («в сочетании с децитабином или без него»); редукция дозы венетоклакса при приёме ингибиторов CYP3A4 (умеренные −50%, сильные −75%); также назначается с 16 дня индукции на 14 дней для глубины ремиссии",
  table="Таблица 1 (расчёт дозы венетоклакса)")
R("C4","эпигенетическая терапия после индукции (более глубокая ремиссия)",["химиотерапия (эпигенетическая терапия)"],"Вальпроевая кислота + Третиноин (ATRA) ± Децитабин",
  [d("Вальпроевая кислота","50 мг/кг ежедневно","внутрь","с первого дня химиотерапии на протяжении всей терапии"),
   d("Третиноин (ATRA)","45 мг/м²","внутрь","ежедневно первые 42 дня, далее 14 дней с 1-го дня каждого последующего курса консолидации"),
   d("Децитабин","20 мг/м²","—","в режиме «окна» на 5 дней (если опцию предусматривает протокол)")],
  uur="B",udd=3,refs=(90,),special="# вальпроевая кислота, # третиноин, # децитабин — off-label")
R("C5","интратекальная терапия (профилактика/лечение нейролейкоза)",["химиотерапия (интратекально)"],"Интратекальное введение цитарабина",
  [d("Цитарабин","возрастная доза: <1 года — 20 мг; 1–2 года — 26 мг; 2–3 года — 34 мг; старше 3 лет — 40 мг","интратекально",
     "профилактически: 5 введений (одно перед каждым блоком терапии + 2 после последнего блока с интервалом 1 месяц); при поражении ЦНС: 1 раз в неделю до санации ликвора (не менее 3 раз), затем как профилактика")],
  uur="A",udd=1,refs=(41,),table="Табл. 2 (дозы цитарабина для интратекального введения)")
R("C6","поддерживающая терапия после индукции и консолидации",["химиотерапия (поддерживающая)"],"Меркаптопурин + Цитарабин",
  [d("Меркаптопурин","50 мг/м²","внутрь","ежедневно"),
   d("Цитарабин","40 мг/м²","п/к","1 раз в день 4 дня каждого месяца")],
  refs=(38,),maint="Меркаптопурин 50 мг/м² внутрь ежедневно + цитарабин 40 мг/м² п/к 4 дня/месяц, длительность 12 месяцев",
  special="начало после восстановления гемопоэза после последнего курса; ценность сомнительна, есть данные о негативном влиянии на ОВ")
REL="терапия первичной рефрактерности и рецидива ОМЛ"
R("C7",REL,["химиотерапия"],"Высокодозный цитарабин + флударабин + идарубицин (FLAIda-подобный режим)",
  [d("Флударабин","30 мг/м² (max 50 мг)","в/в 30-минутная инфузия","ежедневно, дни 2–6 (всего 5 доз)"),
   d("Цитарабин","2 г/м²","в/в инфузия 4 часа","ежедневно, дни 2–6 (всего 5 доз), начиная через 4 часа после окончания инфузии флударабина"),
   d("Идарубицин","8 мг/м²","в/в инфузия 1 час","дни 4, 5, 6 (всего 3 дозы), за 1 час до введения флударабина и цитарабина")],
  udd=4,refs=(49,85,103,181,182),special="по решению консилиума; # флударабин — off-label")
R("C7",REL,["химиотерапия"],"FLAIda",
  [d("Флударабин","30 мг/м²","в/в 30-минутная инфузия","дни 1–5 (всего 5 доз); интервал до начала инфузии цитарабина 4 часа"),
   d("Цитарабин","2000 мг/м²","в/в 3-часовая инфузия","каждые 24 часа, дни 1–5 (всего 10 доз)"),
   d("Идарубицин","10 мг/м²","в/в 60-минутная инфузия","дни 1, 3, 5")],
  refs=(85,103,181,182),special="# флударабин, # идарубицин — off-label")
R("C7",REL,["химиотерапия"],"FLAM (замена идарубицина митоксантроном)",
  [d("Флударабин","30 мг/м²","в/в 30-минутная инфузия","дни 1–5 (всего 5 доз)"),
   d("Цитарабин","2000 мг/м²","в/в 3-часовая инфузия","каждые 24 часа, дни 1–5 (всего 10 доз)"),
   d("Митоксантрон","10 мг/м²","в/в инфузия 60 минут","дни 1, 3, 5")],
  refs=(85,103,181,182),special="при отсутствии идарубицина; # препараты — off-label")
R("C7",REL,["химиотерапия"],"FLA",
  [d("Флударабин","30 мг/м²","в/в 30-минутная инфузия","дни 1–5 (всего 5 доз); интервал до начала инфузии цитарабина 4 часа"),
   d("Цитарабин","2000 мг/м²","в/в 3-часовая инфузия","каждые 24 часа, дни 1–5 (всего 10 доз)")],
  refs=(99,103,181,182),special="# флударабин — off-label")
R("C7a",REL+", невозможность интенсивной ХТ",["таргетная терапия"],"Венетоклакс + Децитабин",
  [d("Венетоклакс","400 мг однократно в сутки","перорально","28 дней цикла"),
   d("Децитабин","20 мг/м²","в/в","дни 3–10 каждого цикла (первые 6 введений обязательны)")],
  udd=4,refs=(98,184,185),special="# венетоклакс, # децитабин — off-label; для детей с рецидивами/рефрактерностью, которым не показана интенсивная индукционная ХТ (сопутствующие заболевания)")
R("C8","таргентная терапия FLT3-ITD",["таргетная терапия"],"Сорафениб",
  [d("Сорафениб","300 мг/м² ежедневно (в сообщении о случае); поддерживающе 170 мг/м² ежедневно","внутрь","47 дней, затем поддерживающая терапия")],
  udd=4,refs=(51,),biom=["мутация FLT3-ITD"],special="# сорафениб — off-label; данные ограничены описаниями случаев")
R("C8","таргентная терапия FLT3-ITD",["таргетная терапия"],"Гилтеритиниб",
  [d("Гилтеритиниб",None,"внутрь")],
  udd=4,refs=(180,),biom=["мутация FLT3-ITD"],special="# гилтеритиниб — off-label; конкретные дозы в документе не приведены")
R("C9",REL+", альтернативная опция",["химиотерапия"],"Кладрибин + Цитарабин с последующими 2 курсами DAV",
  [d("Кладрибин","9 мг/м²","в/в","в течение 5 дней"),
   d("Цитарабин","500 мг/м²","в/в","в течение 5 дней")],
  udd=4,refs=(52,),special="# кладрибин — off-label")
R("C9",REL+", альтернативная опция (после кладрибин+цитарабин)",["химиотерапия"],"DAV",
  [d("Даунорубицин","30 мг/м²","в/в 72-часовая инфузия","дни 1–3"),
   d("Цитарабин","250 мг/м²","в/в 120-часовая инфузия","дни 1–5"),
   d("Этопозид","200 мг/м²","в/в 48-часовая инфузия","дни 4 и 5")],
  udd=4,refs=(52,),special="2 курса после индукции кладрибин+цитарабин")
DS="терапия ОМЛ/МДС у детей с синдромом Дауна (протокол ML-DS-2006, сниженные дозы)"
R("C10",DS+", индукция ремиссии",["химиотерапия"],"AIE (сниженные дозы)",
  [d("Цитарабин","100 мг/м²/день","в/в непрерывная инфузия","48 часов (с утра дня 1 до утра дня 3); затем 100 мг/м² каждые 12 часов 30-минутной инфузией дни 3–8 (всего 12 доз)"),
   d("Идарубицин","8 мг/м²/день","в/в 4-часовая инфузия","дни 3, 5, 7 (всего 3 дозы), непосредственно перед цитарабином"),
   d("Этопозид","150 мг/м²/день","в/в одночасовая инфузия","дни 6, 7, 8 (всего 3 дозы)"),
   d("Цитарабин","возрастная доза (<1 года — 20 мг; 1–2 года — 26 мг; 2–3 года — 34 мг; >3 лет — 40 мг)","интратекально","день 1")],
  uur="B",udd=3,refs=(82,181,182))
R("C10",DS+", консолидация 1",["химиотерапия"],"AI",
  [d("Цитарабин","500 мг/м²/день","в/в непрерывная 24-часовая инфузия","дни 1–4 (всего 96 часов)"),
   d("Идарубицин","5 мг/м²","в/в 1-часовая инфузия","день 3 и день 5 (2 дозы)"),
   d("Цитарабин","возрастная доза","интратекально","день 0")],
  uur="B",udd=3,refs=(74,181,182))
R("C10",DS+", консолидация 2",["химиотерапия"],"haM",
  [d("Цитарабин","1 г/м²","в/в 3-часовая инфузия","каждые 12 часов, 3 дня (всего 6 доз)"),
   d("Митоксантрон","10 мг/м²/день","в/в 30-минутная инфузия","2 дня (всего 2 дозы)"),
   d("Цитарабин","возрастная доза","интратекально","день 0")],
  uur="B",udd=3,refs=(68,100,181))
R("C10",DS+", консолидация 3",["химиотерапия"],"HA (высокие дозы цитарабина)",
  [d("Цитарабин","3 г/м²","в/в 3-часовая инфузия","каждые 12 часов, дни 1–3 (всего 6 доз)"),
   d("Цитарабин","возрастная доза","интратекально","день 0")],
  uur="B",udd=3,refs=(74,181,182))
R("C10a","терапия ТАМ с жизнеугрожающим течением",["химиотерапия"],"Низкие дозы цитарабина",
  [d("Цитарабин","0,5–2 мг/кг",None)],
  uur="B",udd=3,refs=(82,),
  special="при жизнеугрожающих симптомах ТАМ (лейкоцитоз >100 тыс/мкл, конъюгированный билирубин >83 ммоль/л, выраженная гепатоспленомегалия, водянка, выпоты, почечная недостаточность, ДВС)")

with open(f"output-cohort/{DOC}.cohorts.json","w") as f: json.dump(cohorts,f,ensure_ascii=False,indent=1)
with open(f"output-cohort/{DOC}.regimens.json","w") as f: json.dump(rows,f,ensure_ascii=False,indent=1)
for c in cohorts: audit.cohort(DOC,c)
for r in rows: audit.regimen(DOC,r)
audit.event(DOC,"phase2-done",f"{len(rows)} regimens, {len(cohorts)} cohorts")
print(f"{DOC}: {len(cohorts)} cohorts, {len(rows)} regimens written")
