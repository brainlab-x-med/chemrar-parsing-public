Необходимо доставать из клин реков все *медикаментозные* виды лечения со следующими характеристиками:

 1. **Заболевание:** Название нозологии (например, "Злокачественные новообразования губы").

 2. **Код МКБ**

 3. **Линия/Этап лечения:**

 * Адъювантная / Неоадъювантная / Периоперационная.

 * Индукционная (ИХТ).

 * 1-я линия, 2-я линия, 3-я линия (для метастатического/рецидивного процесса).

 * Терапия рецидивов.

 * Терапия отдаленных метастазов.

 * Поддерживающая терапия.

 4. Тип терапии (модальность): ХТ, ЛТ, ХЛТ, Таргетная терапия, Иммунотерапия. (можно несколько)

 5. **Название режима/схемы:** (как в таблицах, например, *PF\+ Cet*, *DC*, *Пембролизумаб*).

 6. **Препараты:** Список препаратов в схеме (МНН).

 7. **Дозировка и схема (для КАЖДОГО препарата в схеме):**

 * Доза (мг/м², AUC, мг/кг, фиксированная).

 * Способ введения (в/в, внутрь, п/к).

 * Дни введения (1-й день, 1-4 дни, непрерывно и т.д.).

 * Частота циклов (каждые 3 нед., еженедельно).

 * Количество циклов/длительность (6 циклов, до прогрессирования, max 2 года).

 8. **Показания (критерии выбора):**

 * **Стадия (TNM / римская цифра):** (например, T4bN0-3, IVA, M1). Учитывать, что стадия может быть описана текстом или таблицей.

 * **Общее состояние (ECOG):** (например, ECOG 0-1, ECOG 2).

 * **Молекулярные маркеры:** (например, экспрессия PD-L1 CPS ≥ 20, платинорезистентность).

 9. Уровни доказательности:

 * УУР (A, B, C).

 * УДД (1, 2, 3, 4, 5).

10. **Источник данных в клинреке:**

 * Страница PDF / точное место, откуда взята информацию.

 * Ссылка на исследование (из списка литературы) — желательно в формате "Автор, журнал, год" или хотя бы номер ссылки.

11. Примечания / Уточнения:

 * Любые маркировки типа "неоптимальный режим", "только при противопоказаниях к ...", "для пациентов с ECOG 2".

 * Информация о поддерживающей терапии после основного курса.

12. **Гистологический тип / подтип заболевания**

 * Например: плоскоклеточный рак, аденокарцинома, мелкоклеточный рак и т.д.

**{red}(жирным выделено)** {red}(- must have)

Пример json

```json
{
 "disease_name": "Злокачественные новообразования губы",
 "icd_code": "C00",
 "histology_type": "плоскоклеточный рак",
 "treatment_regimen_name": "PF + Cet",
 "therapy_type": ["химиотерапия", "таргетная терапия"],
 "treatment_line_stage": "1L",
 "special_conditions": "ECOG 0-1",
 "ecog_status": "0-1",
 "biomarkers": [],
 "drugs": [
 {
 "inn": "Цисплатин",
 "dose": "75-100 мг/м²",
 "route": "в/в",
 "schedule": "1 раз в 3 недели"
 },
 {
 "inn": "Фторурацил",
 "dose": "1000 мг/м²/сут",
 "route": "в/в",
 "schedule": "96-часовая инфузия в 1-4 дни"
 },
 {
 "inn": "Цетуксимаб",
 "dose": "400 мг/м² (нагрузочная), затем 250 мг/м²",
 "route": "в/в",
 "schedule": "еженедельно"
 }
 ],
 "cycle_duration_days": 21,
 "max_cycles": 6,
 "maintenance_therapy": "Цетуксимаб 250 мг/м² еженедельно до прогрессирования",
 "recommendation_level": "C",
 "evidence_level": 2,
 "reference_ids": ["23"],
 "source_page": 27,
 "source_section": "3.3",
 "source_table": "Таблица №1"
}
```

&nbsp;

&nbsp;

### Пример для клин река С00

**Из таблицы 1**

Строка 1

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "1-я линия (метастатический/рецидивный процесс, неоперабельные опухоли)",
 "therapy_type": ["химиотерапия", "таргетная терапия"],
 "regimen_name": "PF + Cet"
 },
 "drugs": [
 {
 "inn": "Цисплатин",
 "dose": "75–100 мг/м²",
 "route": "в/в",
 "schedule": "1-й день",
 "cycle_frequency": "каждые 3 недели",
 "max_cycles": 6
 },
 {
 "inn": "Фторурацил",
 "dose": "1000 мг/м²/сут",
 "route": "в/в",
 "schedule": "96-часовая инфузия в 1–4-й дни",
 "cycle_frequency": "каждые 3 недели",
 "max_cycles": 6
 },
 {
 "inn": "Цетуксимаб",
 "dose": "400 мг/м² (нагрузочная), затем 250 мг/м²",
 "route": "в/в",
 "schedule": "еженедельно (нагрузочная доза в 1-й день 1-го цикла)",
 "cycle_frequency": "еженедельно",
 "max_cycles": "до прогрессирования или непереносимой токсичности (после 6 циклов ХТ – поддерживающая терапия)"
 }
 ],
 "indications": {
 "stage": "IV стадия (M1 — метастатический процесс, а также рецидивные и первично-неоперабельные опухоли, в том числе T4bN0–3)",
 "ecog": "0–1 (предположительно, так как для ECOG 2 есть отдельный режим Pacli+Carbo+Cet)",
 "biomarkers": []
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 27,
 "section": "3.3",
 "table": "Таблица №1"
	"references": ["23"],
 "citation": "Vermorken J.B., Mesia R., Rivera F. et al. Platinum-based chemotherapy plus cetuximab in head and neck cancer. N Engl J Med 2008;359:1116−27"
 },
 "special_conditions": "",
 "maintenance_therapy": "Цетуксимаб 250 мг/м² еженедельно до прогрессирования или непереносимой токсичности"
}
```

Строка 2

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "1-я линия (метастатический/рецидивный процесс, неоперабельные опухоли)",
 "therapy_type": ["химиотерапия", "таргетная терапия"],
 "regimen_name": "DC + Cet"
 },
 "drugs": [
 {
 "inn": "Доцетаксел",
 "dose": "75 мг/м²",
 "route": "в/в",
 "schedule": "1-й день",
 "cycle_frequency": "каждые 3 недели",
 "max_cycles": 4
 },
 {
 "inn": "Цисплатин",
 "dose": "75 мг/м²",
 "route": "в/в",
 "schedule": "1-й день",
 "cycle_frequency": "каждые 3 недели",
 "max_cycles": 4
 },
 {
 "inn": "Цетуксимаб",
 "dose": "400 мг/м² (нагрузочная), затем 250 мг/м²",
 "route": "в/в",
 "schedule": "нагрузочная доза в 1-й день 1-го цикла, далее еженедельно",
 "cycle_frequency": "еженедельно",
 "max_cycles": "до прогрессирования или непереносимой токсичности (после 4 циклов ХТ – поддерживающая терапия)"
 }
 ],
 "indications": {
 "stage": "IV стадия (M1 — метастатический процесс, а также рецидивные и первично-неоперабельные опухоли)",
 "ecog": "0–1 (предположительно, так как для ECOG 2 есть отдельный режим Pacli+Carbo+Cet)",
 "biomarkers": []
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 27,
 "section": "3.3",
 "table": "Таблица №1",
 "references": ["116"],
 "citation": "Guigay J, Fayette J, Dillies A-F, et al. Cetuximab, docetaxel, and cisplatin (TPEx) as first-line treatment in patients with recurrent or metastatic (R/M) squamous cell carcinoma of the head and neck (SCCHN): Final results of phase II trial GORTEC 2008-03 [abstract]. J Clin Oncol 2012;30(suppl 15):Abstract 5505."
 },
 "special_conditions": "",
 "maintenance_therapy": "Цетуксимаб 500 мг/м² в/в 1 раз в 2 недели до прогрессирования или непереносимой токсичности"
}
```

Строка 3

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "1-я линия (метастатический/рецидивный процесс, неоперабельные опухоли)",
 "therapy_type": ["химиотерапия", "таргетная терапия"],
 "regimen_name": "Цисплатин + Cet"
 },
 "drugs": [
 {
 "inn": "Цисплатин",
 "dose": "75–100 мг/м²",
 "route": "в/в",
 "schedule": "1-й день",
 "cycle_frequency": "1 раз в 3 недели",
 "max_cycles": "6–8 введений"
 },
 {
 "inn": "Цетуксимаб",
 "dose": "400 мг/м² (нагрузочная), затем 250 мг/м²",
 "route": "в/в",
 "schedule": "нагрузочная доза в 1-й день 1-го цикла, далее еженедельно",
 "cycle_frequency": "еженедельно",
 "max_cycles": "до прогрессирования или непереносимой токсичности"
 }
 ],
 "indications": {
 "stage": "IV стадия (M1 — метастатический процесс, а также рецидивные и первично-неоперабельные опухоли)",
 "ecog": "0–1 (предположительно, так как для ECOG 2 есть отдельный режим Pacli+Carbo+Cet)",
 "biomarkers": []
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 27,
 "section": "3.3",
 "table": "Таблица №1",
	"references": ["27"],
 "citation": "Burtness B., Goldwasser M.A., Flood W. et al. Phase III randomized trial of cisplatin plus placebo compared with cisplatin plus cetuximab in metastatic/recurrent head and neck cancer: an Eastern Cooperative Oncology Group study. J Clin Oncol 2005;23:8646−54"
 },
 "special_conditions": "",
 "maintenance_therapy": "Цетуксимаб 250 мг/м² в/в еженедельно до прогрессирования или непереносимой токсичности (после завершения цисплатина)"
}
```

Строка 4

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "1-я линия (метастатический/рецидивный процесс, неоперабельные опухоли)",
 "therapy_type": ["химиотерапия", "таргетная терапия"],
 "regimen_name": "Pacli + Carbo + Cet"
 },
 "drugs": [
 {
 "inn": "Паклитаксел",
 "dose": "80 мг/м²",
 "route": "в/в",
 "schedule": "еженедельно",
 "cycle_frequency": "еженедельно",
 "max_cycles": "индивидуально (количество введений цитостатиков определяется индивидуально)"
 },
 {
 "inn": "Карбоплатин",
 "dose": "AUC 2,0",
 "route": "в/в",
 "schedule": "еженедельно",
 "cycle_frequency": "еженедельно",
 "max_cycles": "индивидуально (количество введений цитостатиков определяется индивидуально)"
 },
 {
 "inn": "Цетуксимаб",
 "dose": "400 мг/м² (нагрузочная), затем 250 мг/м²",
 "route": "в/в",
 "schedule": "нагрузочная доза в 1-й день 1-го цикла, далее еженедельно",
 "cycle_frequency": "еженедельно",
 "max_cycles": "до прогрессирования или непереносимой токсичности"
 }
 ],
 "indications": {
 "stage": "IV стадия (метастатический, рецидивный, первично-неоперабельный процесс)",
 "ecog": "2",
 "biomarkers": []
 },
 "evidence": {
 "uur": "C",
 "udd": 2,
 },
 "source": {
 "page": 27,
 "section": "3.3",
 "table": "Таблица №1",
 "references": ["121", "122"],
 "citation": ["Болотина Л.В., Владимирова Л.Ю., Деньгина Н.В., Кутукова С.И., Новик А.В., Романов И.С. Практические рекомендации по лекарственному лечению опухолей головы и шеи. Практические рекомендации RUSSCO, часть 1. Злокачественные опухоли, 2023 (том 13), #3s2, стр. 100–119.",
	"Narveson L, Kathol E, Rockey M, Henry D, Grauer D, Neupane P.Evaluation of weekly paclitaxel, carboplatin, and cetuximab in head and neck cancer patients with incurable disease. Med Oncol.2016 Oct;33(10):107."]
 },
 "special_conditions": "Для пациентов в общем состоянии ECOG 2. Количество введений цитостатиков определяется индивидуально. После завершения химиотерапии при отсутствии прогрессирования – поддерживающая терапия цетуксимабом 250 мг/м² еженедельно",
 "maintenance_therapy": "Цетуксимаб 250 мг/м² в/в еженедельно до прогрессирования или непереносимой токсичности"
}
```

Строка 5

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "1-я линия (метастатический/рецидивный процесс, неоперабельные опухоли)",
 "therapy_type": ["химиотерапия"],
 "regimen_name": "PF"
 },
 "drugs": [
 {
 "inn": "Цисплатин",
 "dose": "75–100 мг/м²",
 "route": "в/в",
 "schedule": "1-й день",
 "cycle_frequency": "каждые 3 недели",
 "max_cycles": 6
 },
 {
 "inn": "Фторурацил",
 "dose": "1000 мг/м²/сут",
 "route": "в/в",
 "schedule": "96-часовая инфузия в 1–4-й дни",
 "cycle_frequency": "каждые 3 недели",
 "max_cycles": 6
 }
 ],
 "indications": {
 "stage": "IV стадия (M1 — метастатический процесс, а также рецидивные и первично-неоперабельные опухоли)",
 "ecog": "0–1 (предположительно, так как для ECOG 2 есть отдельные режимы)",
 "biomarkers": []
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 27,
 "section": "3.3",
 "table": "Таблица №1",
 "references": ["117"],
 "citation": "Gibson MK, Li Y, Murphy B, et al. Randomized phase III evaluation of cisplatin plus fluorouracil versus cisplatin plus paclitaxel in advanced head and neck cancer (E1395): an intergroup trial of the Eastern Cooperative Oncology Group. J Clin Oncol 2005;23:3562-3567"
 },
 "special_conditions": "Неоптимальный режим лечения; возможен к применению только в случае абсолютных противопоказаний к назначению анти-EGFR моноклональных антител (МКА).",
 "maintenance_therapy": null
},

{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "1-я линия (метастатический/рецидивный процесс, неоперабельные опухоли)",
 "therapy_type": ["химиотерапия"],
 "regimen_name": "PF"
 },
 "drugs": [
 {
 "inn": "Карбоплатин",
 "dose": "AUC 5",
 "route": "в/в",
 "schedule": "1-й день",
 "cycle_frequency": "каждые 3 недели",
 "max_cycles": "6 (может быть увеличено до 8 при хорошей переносимости и положительной динамике)"
 },
 {
 "inn": "Фторурацил",
 "dose": "1000 мг/м²/сут",
 "route": "в/в",
 "schedule": "96-часовая инфузия в 1–4-й дни",
 "cycle_frequency": "каждые 3 недели",
 "max_cycles": "6 (может быть увеличено до 8 при хорошей переносимости и положительной динамике)"
 }
 ],
 "indications": {
 "stage": "IV стадия (метастатический, рецидивный, первично-неоперабельный процесс)",
 "ecog": "0–1 (предположительно, так как для ECOG 2 есть отдельные режимы)",
 "biomarkers": []
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 27,
 "section": "3.3",
 "table": "Таблица №1",
 "references": ["29"],
 "citation": "Forastiere A.A., Metch B., Schuller D.E. et al. Randomized comparison of cisplatin plus fluorouracil and carboplatin plus fluorouracil versus methotrexate in advanced squamous-cell carcinoma of the head and neck: a Southwest Oncology Group study. J Clin Oncol 1992;10:1245−51"
 },
 "special_conditions": "Неоптимальный режим лечения; возможен к применению только в случае абсолютных противопоказаний к назначению анти-EGFR моноклональных антител (МКА).",
 "maintenance_therapy": null
}
```

Строка 6

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "1-я линия (метастатический/рецидивный процесс, неоперабельные опухоли)",
 "therapy_type": ["химиотерапия"],
 "regimen_name": "Pacli + Carbo"
 },
 "drugs": [
 {
 "inn": "Паклитаксел",
 "dose": "175 мг/м²",
 "route": "в/в",
 "schedule": "1-й день",
 "cycle_frequency": "каждые 3 недели",
 "max_cycles": "6 (может быть увеличено до 8 при хорошей переносимости и положительной динамике)"
 },
 {
 "inn": "Карбоплатин",
 "dose": "AUC 5–6",
 "route": "в/в",
 "schedule": "1-й день",
 "cycle_frequency": "каждые 3 недели",
 "max_cycles": "6 (может быть увеличено до 8 при хорошей переносимости и положительной динамике)"
 }
 ],
 "indications": {
 "stage": "IV стадия (метастатический, рецидивный, первично-неоперабельный процесс)",
 "ecog": null,
 "biomarkers": []
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 28,
 "section": "3.3",
 "references": ["121"],
 "citation": ["Болотина Л.В., Владимирова Л.Ю., Деньгина Н.В., Кутукова С.И., Новик А.В., Романов И.С. Практические рекомендации по лекарственному лечению опухолей головы и шеи. Практические рекомендации RUSSCO, часть 1. Злокачественные опухоли, 2023 (том 13), #3s2, стр. 100–119."]
 },
 "special_conditions": "Режим может применяться у пациентов, не имеющих противопоказаний к комбинированной химиотерапии. Количество циклов определяется индивидуально.",
 "maintenance_therapy": null
},

{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "1-я линия (метастатический/рецидивный процесс, неоперабельные опухоли)",
 "therapy_type": ["химиотерапия"],
 "regimen_name": "Pacli + Carbo"
 },
 "drugs": [
 {
 "inn": "Паклитаксел",
 "dose": "60–80 мг/м²",
 "route": "в/в",
 "schedule": "еженедельно",
 "cycle_frequency": null,
 "max_cycles": "до прогрессирования или неприемлемой токсичности, не более 18 недель"
 },
 {
 "inn": "Карбоплатин",
 "dose": "AUC 2",
 "route": "в/в",
 "schedule": "еженедельно",
 "cycle_frequency": null,
 "max_cycles": "до прогрессирования или неприемлемой токсичности, не более 18 недель"
 }
 ],
 "indications": {
 "stage": "IV стадия (метастатический, рецидивный, первично-неоперабельный процесс)",
 "ecog": null,
 "biomarkers": []
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 28,
 "section": "3.3",
 "references": ["117"],
 "citation": "Gibson MK, Li Y, Murphy B, et al. Randomized phase III evaluation of cisplatin plus fluorouracil versus cisplatin plus paclitaxel in advanced head and neck cancer (E1395): an intergroup trial of the Eastern Cooperative Oncology Group. J Clin Oncol 2005;23:3562-3567"
 },
 "special_conditions": "Еженедельный режим может быть предпочтительным для пациентов с более низким ECOG или при необходимости снижения токсичности.",
 "maintenance_therapy": null
}
```

Строка 7

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "1-я линия (метастатический/рецидивный процесс, неоперабельные опухоли)",
 "therapy_type": ["химиотерапия"],
 "regimen_name": "DC"
 },
 "drugs": [
 {
 "inn": "Доцетаксел",
 "dose": "175 мг/м²",
 "route": "в/в",
 "schedule": "1-й день",
 "cycle_frequency": "каждые 3 недели",
 "max_cycles": "6 (может быть увеличено до 8 при хорошей переносимости и положительной динамике)"
 },
 {
 "inn": "Цисплатин",
 "dose": "75 мг/м²",
 "route": "в/в",
 "schedule": "1-й день",
 "cycle_frequency": "каждые 3 недели",
 "max_cycles": "6 (может быть увеличено до 8 при хорошей переносимости и положительной динамике)"
 }
 ],
 "indications": {
 "stage": "IV стадия (метастатический, рецидивный или первично-неоперабельный процесс)",
 "ecog": "0–1 (предположительно)",
 "biomarkers": []
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 27,
 "section": "3.3",
 "table": "Таблица №1",
 "references": ["120", "121"],
 "citation": ["Specht L, Larsen SK, Hansen HS Phase II study of docetaxel and cisplatin in patients with recurrent or disseminated squamous-cell carcinoma of the head and neck. .Ann Oncol. 2000 Jul;11(7):845-9.",
				"Болотина Л.В., Владимирова Л.Ю., Деньгина Н.В., Кутукова С.И., Новик А.В., Романов И.С. Практические рекомендации по лекарственному лечению опухолей головы и шеи. Практические рекомендации RUSSCO, часть 1. Злокачественные опухоли, 2023 (том 13), #3s2, стр. 100–119."]
 },
 "special_conditions": "Неоптимальный режим лечения; возможен к применению только в случае абсолютных противопоказаний к назначению анти-EGFR моноклональных антител (МКА). ",
 "maintenance_therapy": null
}
```

Строка 8

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "2-я и последующие линии (метастатический/рецидивный процесс)",
 "therapy_type": ["иммунотерапия"],
 "regimen_name": "Ниволумаб"
 },
 "drugs": [
 {
 "inn": "Ниволумаб",
 "dose": "3 мг/кг или 240 мг или 480 мг",
 "route": "в/в",
 "schedule": "3 мг/кг 1 раз в 2 нед; 240 мг 1 раз в 2 нед; 480 мг 1 раз в 4 нед",
 "cycle_frequency": "каждые 2 или 4 недели",
 "max_cycles": "до прогрессирования или неприемлемой токсичности, не более 2 лет"
 }
 ],
 "indications": {
 "stage": "IV стадия (метастатический, рецидивный или первично-неоперабельный процесс)",
 "ecog": null,
 "biomarkers": []
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 27,
 "section": "3.3",
 "table": "Таблица №1",
 "references": ["36"],
 "citation": "Ferris R., Blumenschein G., Fayette J. et al. Nivolumab for recurrent squamous-cell carcinoma of the head and neck. N Engl J Med 2016;375:1856‒67"
 },
 "special_conditions": "Может назначаться независимо от уровня экспрессии PD-L1.",
 "maintenance_therapy": null
}
```

Строка 9

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "1-я линия (при PD-L1 CPS > 20); 2-я и последующие линии (при прогрессировании после платиносодержащей ХТ и TPS ≥ 50%)",
 "therapy_type": ["иммунотерапия"],
 "regimen_name": "Пембролизумаб (монотерапия)"
 },
 "drugs": [
 {
 "inn": "Пембролизумаб",
 "dose": "200 мг или 400 мг",
 "route": "в/в",
 "schedule": "200 мг 1 раз в 3 нед (30-минутная инфузия) или 400 мг 1 раз в 6 нед",
 "cycle_frequency": "каждые 3 или 6 недель",
 "max_cycles": "до прогрессирования или неприемлемой токсичности, не более 2 лет"
 }
 ],
 "indications": {
 "stage": "IV стадия (метастатический, рецидивный или первично-неоперабельный процесс)",
 "ecog": null,
 "biomarkers": ["PD-L1 CPS > 20 (для 1-й линии)", "TPS ≥ 50% (для 2-й линии после платиносодержащей ХТ)"]
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 27,
 "section": "3.3",
 "table": "Таблица №1",
 "references": ["38", "39", "118"],
 "citation": ["Сohen, E. E. W., Soulières, D., Le Tourneau, C., et al. (2018). Pembrolizumab versus methotrexate, docetaxel, or cetuximab for recurrent or metastatic head-and-neck squamous cell carcinoma (KEYNOTE-040): a randomised, open-label, phase 3 study. The Lancet. doi:10.1016/s0140-6736(18)31999-8",
 "Сhow L.Q., Haddad R., Gupta S. et al. Antitumor activity of pembrolizumab in biomarker-unselected patients with recurrent and/or metastatic head and neck squamous cell carcinoma: results from the phase Ib KEYNOTE-012 expansion cohort. J Clin Oncol 2016;34(32):3838‒45",
				 "Lala M, Li M, Sinha V, de Alwis D, Chartash E, Jain L. A six-weekly (Q6W) dosing schedule for pembrolizumab based on an exposure-response (E-R) evaluation using modeling and simulation. J Clin Oncol. 2018;36 (suppl; abstr 306)"]
 },
 "special_conditions": "Рекомендуемая длительность применения соответствует дизайну регистрационных исследований (не более 2 лет). В 1-й линии применяется при наличии экспрессии PD-L1 CPS > 20. Во 2-й линии – при прогрессировании на фоне или после химиотерапии, включающей препараты платины, при уровне TPS ≥ 50%.",
 "maintenance_therapy": null
}
```

Строка 10

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "1-я линия (метастатический/рецидивный процесс, неоперабельные опухоли)",
 "therapy_type": ["химиотерапия", "иммунотерапия"],
 "regimen_name": "PF + Пембролизумаб"
 },
 "drugs": [
 {
 "inn": "Пембролизумаб",
 "dose": "200 мг",
 "route": "в/в",
 "schedule": "1 раз в 3 недели",
 "cycle_frequency": "каждые 3 недели",
 "max_cycles": "6 (в комбинации с ХТ), далее поддерживающая терапия до 35 введений всего"
 },
 {
 "inn": "Карбоплатин (альтернатива 1) или Цисплатин (альтернатива 2)",
 "dose": "AUC 5 (карбоплатин) или 100 мг/м² (цисплатин)",
 "route": "в/в",
 "schedule": "1-й день",
 "cycle_frequency": "каждые 3 недели",
 "max_cycles": 6
 },
 {
 "inn": "Фторурацил",
 "dose": "1000 мг/м²/сут",
 "route": "в/в",
 "schedule": "96-часовая инфузия в 1–4-й дни",
 "cycle_frequency": "каждые 3 недели",
 "max_cycles": 6
 }
 ],
 "indications": {
 "stage": "IV стадия (метастатический, рецидивный или первично-неоперабельный процесс)",
 "ecog": "0–1 (предположительно)",
 "biomarkers": ["экспрессия PD-L1 CPS ≥ 1%"]
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 27,
 "section": "3.3",
 "table": "Таблица №1",
 "references": ["123"],
 "citation": "Burtness B, Harrington KJ, Greil R, et al. Pembrolizumab alone or with chemotherapy versus cetuximab with chemotherapy for recurrent or metastatic squamous cell carcinoma of the head and neck (KEYNOTE-048): a randomised, open-label, phase 3 study. Lancet 2019;394:1915-1928"
 },
 "special_conditions": "Выбор препарата платины (карбоплатин или цисплатин) – индивидуально.",
 "maintenance_therapy": "Пембролизумаб 200 мг в/в 1 раз в 3 недели или 400 мг 1 раз в 6 недель до прогрессирования, неприемлемой токсичности или до 35 введений в целом"
}
```

Строка 11

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "1-я линия (метастатический/рецидивный процесс, неоперабельные опухоли)",
 "therapy_type": ["химиотерапия"],
 "regimen_name": "Цисплатин (монотерапия)"
 },
 "drugs": [
 {
 "inn": "Цисплатин",
 "dose": "60–70 мг/м²",
 "route": "в/в",
 "schedule": "1 раз в 3 недели",
 "cycle_frequency": "каждые 3 недели",
 "max_cycles": "индивидуально, не более 6–8 введений"
 }
 ],
 "indications": {
 "stage": "IV стадия (метастатический процесс, а также рецидивные и первично-неоперабельные опухоли)",
 "ecog": "может применяться при ECOG 2",
 "biomarkers": []
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 28,
 "section": "3.3",
 "table": "Таблица №1",
 "references": ["121"],
 "citation": "Болотина Л.В., Владимирова Л.Ю., Деньгина Н.В., Кутукова С.И., Новик А.В., Романов И.С. Практические рекомендации по лекарственному лечению опухолей головы и шеи. Практические рекомендации RUSSCO, часть 1. Злокачественные опухоли, 2023 (том 13), #3s2, стр. 100–119."
 },
 "special_conditions": "Применяется как монотерапия, в том числе у пациентов с ECOG 2 или при противопоказаниях к комбинированным режимам.",
 "maintenance_therapy": null
}
```

Строка 12

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "1-я линия (метастатический/рецидивный процесс, неоперабельные опухоли)",
 "therapy_type": ["химиотерапия"],
 "regimen_name": "Карбоплатин (монотерапия)"
 },
 "drugs": [
 {
 "inn": "Карбоплатин",
 "dose": "AUC 5–6 или AUC 2",
 "route": "в/в",
 "schedule": "AUC 5–6 1 раз в 3 нед или AUC 2 еженедельно",
 "cycle_frequency": "каждые 3 недели или еженедельно",
 "max_cycles": null
 }
 ],
 "indications": {
 "stage": "IV стадия (метастатический процесс, а также рецидивные и первично-неоперабельные опухоли)",
 "ecog": "может применяться при ECOG 2",
 "biomarkers": []
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 28,
 "section": "3.3",
 "table": "Таблица №1",
 "references": ["119"],
 "citation": "Al-Sarraf M, Metch B, Kish J, et al. Platinum analogs in recurrent and advanced head and neck cancer: a Southwest Oncology Group and Wayne State University Study. Cancer Treat Rep 1987;71:723-726."
 },
 "special_conditions": "Применяется как монотерапия, в том числе у пациентов с ECOG 2 или при противопоказаниях к комбинированным режимам.",
 "maintenance_therapy": null
}
```

Строка 13

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "1-я линия (метастатический/рецидивный процесс, неоперабельные опухоли)",
 "therapy_type": ["химиотерапия"],
 "regimen_name": "Паклитаксел (монотерапия)"
 },
 "drugs": [
 {
 "inn": "Паклитаксел",
 "dose": "175 мг/м² или 80 мг/м²",
 "route": "в/в",
 "schedule": "175 мг/м² 1 раз в 3 нед или 80 мг/м² еженедельно",
 "cycle_frequency": "каждые 3 недели или еженедельно",
 "max_cycles": null
 }
 ],
 "indications": {
 "stage": "IV стадия (метастатический процесс, а также рецидивные и первично-неоперабельные опухоли)",
 "ecog": "может применяться при ECOG 2",
 "biomarkers": []
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 28,
 "section": "3.3",
 "table": "Таблица №1",
 "references": ["31"],
 "citation": "Grau J.J., Caballero M., Verger E. et al. Weekly paclitaxel for platin-resistant stage IV head and neck cancer patients. Acta Otolaryngol 2009;129:1294−9"
 },
 "special_conditions": "Применяется как монотерапия, в том числе у пациентов с ECOG 2 или при противопоказаниях к комбинированным режимам.",
 "maintenance_therapy": null
}
```

Строка 14

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "1-я линия (метастатический/рецидивный процесс, неоперабельные опухоли)",
 "therapy_type": ["химиотерапия"],
 "regimen_name": "Доцетаксел (монотерапия)"
 },
 "drugs": [
 {
 "inn": "Доцетаксел",
 "dose": "70–75 мг/м²",
 "route": "в/в",
 "schedule": "1 раз в 3 недели",
 "cycle_frequency": null,
 "max_cycles": null
 }
 ],
 "indications": {
 "stage": "IV стадия (метастатический процесс, а также рецидивные и первично-неоперабельные опухоли)",
 "ecog": "2",
 "biomarkers": []
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 28,
 "section": "3.3",
 "table": "Таблица №1 (монотерапии)",
 "references": ["121"],
 "citation": "Болотина Л.В., Владимирова Л.Ю., Деньгина Н.В., Кутукова С.И., Новик А.В., Романов И.С. Практические рекомендации по лекарственному лечению опухолей головы и шеи. Практические рекомендации RUSSCO, часть 1. Злокачественные опухоли, 2023 (том 13), #3s2, стр. 100–119."
 },
 "special_conditions": "Для пациентов в общем состоянии ECOG 2 балла. Количество введений определяется индивидуально.",
 "maintenance_therapy": null
}
```

Строка 15

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "1-я линия (метастатический/рецидивный процесс, неоперабельные опухоли)",
 "therapy_type": ["химиотерапия"],
 "regimen_name": "Капецитабин (монотерапия)"
 },
 "drugs": [
 {
 "inn": "Капецитабин",
 "dose": "2000 мг/м²",
 "route": "внутрь",
 "schedule": "в 2 приема в 1–14-й дни, затем перерыв 1 неделя; или 2000 мг/сут ежедневно в метрономном режиме",
 "cycle_frequency": "каждые 3 недели (при прерывистом режиме) или непрерывно",
 "max_cycles": null
 }
 ],
 "indications": {
 "stage": "IV стадия (метастатический процесс, а также рецидивные и первично-неоперабельные опухоли)",
 "ecog": "2",
 "biomarkers": []
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 28,
 "section": "3.3",
 "table": "Таблица №1 (монотерапии)",
 "references": ["121"],
 "citation": "Болотина Л.В., Владимирова Л.Ю., Деньгина Н.В., Кутукова С.И., Новик А.В., Романов И.С. Практические рекомендации по лекарственному лечению опухолей головы и шеи. Практические рекомендации RUSSCO, часть 1. Злокачественные опухоли, 2023 (том 13), #3s2, стр. 100–119."
 },
 "special_conditions": "Для пациентов в общем состоянии ECOG 2 балла. Длительность терапии определяется индивидуально. Возможны два режима: прерывистый (2000 мг/м² в 1–14 дни, 1 неделя перерыв) и метрономный (2000 мг/сут ежедневно).",
 "maintenance_therapy": null
}
```

Строка 16

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "1-я линия (метастатический/рецидивный процесс, неоперабельные опухоли)",
 "therapy_type": ["химиотерапия"],
 "regimen_name": "Метотрексат (монотерапия)"
 },
 "drugs": [
 {
 "inn": "Метотрексат",
 "dose": "40 мг/м²",
 "route": "в/в",
 "schedule": "еженедельно",
 "cycle_frequency": null,
 "max_cycles": null
 }
 ],
 "indications": {
 "stage": "IV стадия (метастатический процесс, а также рецидивные и первично-неоперабельные опухоли)",
 "ecog": "2",
 "biomarkers": []
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 28,
 "section": "3.3",
 "table": "Таблица №1 (монотерапии)",
 "references": ["29"],
 "citation": "Forastiere A.A., Metch B., Schuller D.E. et al. Randomized comparison of cisplatin plus fluorouracil and carboplatin plus fluorouracil versus methotrexate in advanced squamous-cell carcinoma of the head and neck: a Southwest Oncology Group study. J Clin Oncol 1992;10:1245−51"
 },
 "special_conditions": "Для пациентов в общем состоянии ECOG 2 балла. Количество введений определяется индивидуально.",
 "maintenance_therapy": null
}
```

Строка 17

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "1-я линия (метастатический/рецидивный процесс, неоперабельные опухоли)",
 "therapy_type": ["таргетная терапия"],
 "regimen_name": "Цетуксимаб (монотерапия)"
 },
 "drugs": [
 {
 "inn": "Цетуксимаб",
 "dose": "400 мг/м² (нагрузочная), затем 250 мг/м²",
 "route": "в/в",
 "schedule": "нагрузочная доза: 2-часовая инфузия в 1-й день 1-го курса; далее 250 мг/м² 1-часовая инфузия еженедельно",
 "cycle_frequency": "еженедельно",
 "max_cycles": null
 }
 ],
 "indications": {
 "stage": "IV стадия (метастатический процесс, а также рецидивные и первично-неоперабельные опухоли)",
 "ecog": "2",
 "biomarkers": []
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 28,
 "section": "3.3",
 "table": "Таблица №1",
 "references": ["34"],
 "citation": "Vermorken J.B., Trigo J., Hitt R. et al. Open-label, uncontrolled, multicenter phase II study to evaluate the efficacy and toxicity of cetuximab as a single agent in patients with recurrent and/or metastatic squamous cell carcinoma of the head and neck who failed to respond to platinum-based therapy. J Clin Oncol 2007;25:2171−7"
 },
 "special_conditions": "Для пациентов в общем состоянии ECOG 2 балла. Монотерапия цетуксимабом может рассматриваться как альтернатива комбинированным режимам при ECOG 2 или при непереносимости химиотерапии. Длительность терапии определяется индивидуально (до прогрессирования или неприемлемой токсичности).",
 "maintenance_therapy": null
}
```

**Сноски после таблицы**

Ниволумаб

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "2-я и последующие линии (метастатический/рецидивный процесс, платинорезистентные опухоли)",
 "therapy_type": ["иммунотерапия"],
 "regimen_name": "Ниволумаб"
 },
 "drugs": [
 {
 "inn": "Ниволумаб",
 "dose": "3 мг/кг или 240 мг или 480 мг",
 "route": "в/в",
 "schedule": "3 мг/кг 1 раз в 2 нед; 240 мг 1 раз в 2 нед; 480 мг 1 раз в 4 нед",
 "cycle_frequency": "каждые 2 или 4 недели (в зависимости от дозы)",
 "max_cycles": "до прогрессирования или неприемлемой токсичности, не более 2 лет"
 }
 ],
 "indications": {
 "stage": "IV стадия (метастатический, рецидивный)",
 "ecog": null,
 "biomarkers": ["независимо от уровня экспрессии PD-L1"]
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 28,
 "section": "3.3",
 "references": ["36"],
 "citation": "Ferris R., Blumenschein G., Fayette J. et al. Nivolumab for recurrent squamous-cell carcinoma of the head and neck. N Engl J Med 2016;375:1856‒67"
 },
 "special_conditions": "Во 2 и последующих линиях терапии при прогрессировании на фоне или после платиносодержащей схемы химиотерапии. Может назначаться независимо от уровня экспрессии PD-L1.",
 "maintenance_therapy": null
}
```

Пембролизумаб

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "2-я и последующие линии (метастатический/рецидивный процесс, прогрессирование после платиносодержащей терапии)",
 "therapy_type": ["иммунотерапия"],
 "regimen_name": "Пембролизумаб"
 },
 "drugs": [
 {
 "inn": "Пембролизумаб",
 "dose": "200 мг",
 "route": "в/в",
 "schedule": "200 мг 1 раз в 3 нед",
 "cycle_frequency": "каждые 3 недели",
 "max_cycles": "до прогрессирования или неприемлемой токсичности"
 }
 ],
 "indications": {
 "stage": "IV стадия (метастатический, рецидивный)",
 "ecog": null,
 "biomarkers": null
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 28,
 "section": "3.3",
 "references": ["37", "38", "39"],
 "citation": ["Ye W., Schmitt, N. C. (2019). Pembrolizumab for recurrent/metastatic head and neck cancer: equally promising for Asian patients? Annals of Translational Medicine, 7(S1), S14–S14. doi:10.21037/atm.2019.01.46",
				"Сohen, E. E. W., Soulières, D., Le Tourneau, C., et al. (2018). Pembrolizumab versus methotrexate, docetaxel, or cetuximab for recurrent or metastatic head-and-neck squamous cell carcinoma (KEYNOTE-040): a randomised, open-label, phase 3 study. The Lancet. doi:10.1016/s0140-6736(18)31999-8",
				"Сhow L.Q., Haddad R., Gupta S. et al. Antitumor activity of pembrolizumab in biomarker-unselected patients with recurrent and/or metastatic head and neck squamous cell carcinoma: results from the phase Ib KEYNOTE-012 expansion cohort. J Clin Oncol 2016;34(32):3838‒45"]
 },
 "special_conditions": "При прогрессировании на фоне или после платиносодержащей схемы химиотерапии. Рекомендуемая длительность применения соответствует дизайну регистрационных исследований (до 2 лет).",
 "maintenance_therapy": null
}
```

Афатиниб

```json
{
 "disease": {
 "name": "Злокачественные новообразования губы",
 "icd10": "C00",
 "histology_type": "плоскоклеточный рак"
 },
 "treatment": {
 "line_stage": "2-я и последующие линии (метастатический/рецидивный процесс, прогрессирование после платиносодержащей терапии)",
 "therapy_type": ["таргетная терапия"],
 "regimen_name": "Афатиниб"
 },
 "drugs": [
 {
 "inn": "Афатиниб",
 "dose": "40 мг",
 "route": "внутрь",
 "schedule": "ежедневно",
 "cycle_frequency": null,
 "max_cycles": "до прогрессирования или неприемлемой токсичности"
 }
 ],
 "indications": {
 "stage": "IV стадия (метастатический, рецидивный)",
 "ecog": null,
 "biomarkers": null
 },
 "evidence": {
 "uur": "C",
 "udd": 2
 },
 "source": {
 "page": 29,
 "section": "3.3",
 "references": ["40"],
 "citation": "Machiels J.P., Haddad R.I., Fayette J. et al. Afatinib versus methotrexate as second-line treatment in patients with recurrent or metastatic squamous-cell carcinoma of the head and neck progressing on or after platinum-based therapy (LUX-Head & Neck 1): an open-label, randomised phase 3 trial. Lancet Oncol 2015;16:583−94"
 },
 "special_conditions": "При прогрессировании после платиносодержащей терапии. Эффективность при плоскоклеточном раке головы и шеи оценена только по данным зарубежных исследований.",
 "maintenance_therapy": null
}
```

&nbsp;


