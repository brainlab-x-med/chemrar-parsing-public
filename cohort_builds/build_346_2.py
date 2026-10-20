# -*- coding: utf-8 -*-
"""Build cohorts + medication regimens for doc 346_2 (пограничные опухоли яичников)."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills", "clinrec-cohort-extract", "scripts"))
import audit  # noqa: E402

DOC = "346_2"

DISEASE = {
    "name": "Пограничные опухоли яичников (ПОЯ, атипически пролиферирующие опухоли)",
    "icd10": "D39.1 (также использовался код C56)",
    "histology_type": "эпителиальные пограничные опухоли: серозные (СПОЯ, ~53%), муцинозные (~43%), эндометриоидные, светлоклеточные, опухоли Бреннера; без деструктивной стромальной инвазии",
}

cohorts = [
    {
        "cohort_id": "C1", "disease": DISEASE,
        "stage": "все стадии ПОЯ (I–III по FIGO, в т.ч. IIA–IIIC для СПОЯ)",
        "resectability": None,
        "clinical_situation": "первичный процесс; лечение хирургическое",
        "ecog": None,
        "biomarkers": ["мутации BRAF/KRAS (патогенетическая характеристика СПОЯ)"],
        "treatment_stages": ["хирургическое лечение — основной и единственный метод; химиотерапия не рекомендуется независимо от гистотипа и стадии"],
        "source": {"section": "3 / 3.1 / 3.2"},
    },
    {
        "cohort_id": "C2", "disease": DISEASE,
        "stage": "рецидив СПОЯ в яичнике/яичниках",
        "resectability": None,
        "clinical_situation": "рецидив",
        "ecog": None, "biomarkers": [],
        "treatment_stages": ["хирургическое лечение (резекция яичника/аднексэктомия/экстирпация матки с придатками)"],
        "source": {"section": "3.3.1"},
    },
    {
        "cohort_id": "C3", "disease": DISEASE,
        "stage": "экстрагонадный/экстрагенитальный рецидив СПОЯ",
        "resectability": None,
        "clinical_situation": "рецидив",
        "ecog": None, "biomarkers": [],
        "treatment_stages": ["хирургическое удаление рецидивных узлов; при раке low grade в имплантах — тактика РЯ"],
        "source": {"section": "3.3.2"},
    },
]

regimens = []  # документ не содержит лекарственных режимов: ХТ при ПОЯ неэффективна и не рекомендуется

audit.event(DOC, "phase2-start", "346_2 пограничные опухоли яичников: cohort-first extraction")
audit.read_block(DOC, "346_2.md", 200, 273, "§3 Лечение: хирургия как единственный метод; ХТ неэффективна")
for c in cohorts:
    audit.cohort(DOC, c)
audit.event(DOC, "no-regimens", "Химиотерапия в лечении ПОЯ не рекомендована (§3: 'Химиотерапия в лечении ПОЯ неэффективна [10, 22-24]'); лекарственных схем в документе нет")
for r in regimens:
    audit.regimen(DOC, r)
audit.event(DOC, "phase2-done", f"{len(regimens)} regimens")

with open(f"output-cohort/{DOC}.cohorts.json", "w", encoding="utf-8") as f:
    json.dump(cohorts, f, ensure_ascii=False, indent=2)
with open(f"output-cohort/{DOC}.regimens.json", "w", encoding="utf-8") as f:
    json.dump(regimens, f, ensure_ascii=False, indent=2)

print(f"{DOC}: {len(regimens)} rows, {len(cohorts)} cohorts (лекарственных режимов в КР нет)")
