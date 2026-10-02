# Exploratory Data Analysis — Titanic Dataset

**Task 2 — Data Analytics Internship**
Dataset: `titanic_cleaned.csv` (output of Task 1)
Tools: Python (pandas, seaborn, matplotlib)
Script: `eda_analysis.py`

All statistics below were recalculated directly from `titanic_cleaned.csv` by running `eda_analysis.py`; none are hard-coded or assumed.

---

## 1. Dataset Overview

- 891 passenger records, 15 columns (12 original + `Has_Cabin`, `Title`, `Embarked_Full` engineered in Task 1).
- No missing values remain (handled in Task 1).
- Target variable: `Survived` (0 = died, 1 = survived).

## 2. Summary Statistics

| Metric | Value |
|---|---|
| Total passengers | 891 |
| Survivors | 342 |
| Non-survivors | 549 |
| Overall survival rate | 38.4% |

| Metric | Age | Fare |
|---|---|---|
| Mean | 29.11 | $32.20 |
| Median | 26.00 | $14.45 |
| Std Dev | 13.30 | $49.69 |
| Min | 0.40 | $0.00 |
| Max | 80.00 | $512.33 |

| Family Size (SibSp + Parch + 1) | Value |
|---|---|
| Mean | 1.90 |
| Median | 1.00 |

Fare is heavily right-skewed (mean $32.20 vs. median $14.45) — a small number of very expensive tickets pull the average well above the typical fare.

## 3. Survival Analysis by Sex and Passenger Class

![Survival by class and sex](charts/01_survival_by_class_sex.png)

| Sex | Survival Rate | Count |
|---|---|---|
| Female | 74.2% | 314 |
| Male | 18.9% | 577 |

| Class | Survival Rate | Count |
|---|---|---|
| 1st | 63.0% | 216 |
| 2nd | 47.3% | 184 |
| 3rd | 24.2% | 491 |

| Class + Sex | Survival Rate | Count |
|---|---|---|
| 1st, Female | 96.8% | 94 |
| 1st, Male | 36.9% | 122 |
| 2nd, Female | 92.1% | 76 |
| 2nd, Male | 15.7% | 108 |
| 3rd, Female | 50.0% | 144 |
| 3rd, Male | 13.5% | 347 |

Sex showed the largest difference in survival rate among the major categorical variables analyzed, and this gap held within every passenger class — the most extreme contrast being 1st-class women (96.8%) versus 3rd-class men (13.5%).

## 4. Age Distribution

![Age distribution by survival](charts/02_age_distribution.png)

Age is right-skewed with a concentration of passengers in their 20s–30s. The distributions for survivors and non-survivors overlap substantially. Age has a weak linear correlation with survival (r = -0.06), indicating that age alone does not show a strong linear relationship with survival in this dataset.

## 5. Fare Distribution

![Fare distribution by class](charts/03_fare_by_class.png)

Fare rises with passenger class, as expected (1st class fares are visibly higher and more variable than 2nd or 3rd). The chart uses a symlog y-axis, noted explicitly in the axis label, to keep the small number of very high fares from compressing the rest of the distribution.

## 6. Family Size Analysis

![Survival by family size](charts/04_survival_by_family_size.png)

| Family Size | Survival Rate | Count (n) |
|---|---|---|
| 1 | 30.4% | 537 |
| 2 | 55.3% | 161 |
| 3 | 57.8% | 102 |
| 4 | 72.4% | 29 |
| 5 | 20.0% | 15 |
| 6 | 13.6% | 22 |
| 7 | 33.3% | 12 |
| 8 | 0.0% | 6 |
| 11 | 0.0% | 7 |

Solo travelers (n=537) had a notably lower survival rate (30.4%) than passengers in small-to-medium families of 2–4 (55–72%). Very large family groups (size 8 and 11) show extremely low observed survival in this dataset, but the sample sizes are small (6 and 7 passengers respectively), so these percentages should be interpreted cautiously rather than treated as a strong general trend.

## 7. Title Analysis

![Survival by title](charts/06_survival_by_title.png)

| Title | Survival Rate | Count (n) |
|---|---|---|
| the Countess | 100.0% | 1 |
| Mrs | 79.4% | 126 |
| Miss | 70.3% | 185 |
| Master | 57.5% | 40 |
| Rare | 31.8% | 22 |
| Mr | 15.7% | 517 |

"Master" (a title historically used for young boys) survived at a much higher rate (57.5%) than adult men under "Mr" (15.7%), suggesting age within the male population mattered beyond the sex-only breakdown. The "the Countess" category has only 1 passenger, so its 100% rate is not a generalizable trend — it reflects the outcome of a single individual and is reported here for completeness, not as evidence of a title-based pattern. The "Rare" category (n=22) should also be read with some caution given its smaller size relative to Mr/Miss/Mrs.

## 8. Correlation Analysis

![Correlation heatmap](charts/05_correlation_heatmap.png)

| Variable | Correlation with Survived |
|---|---|
| Has_Cabin | +0.32 |
| Fare | +0.26 |
| Family_Size | +0.02 |
| Age | -0.06 |
| Pclass | -0.34 |

Notes on interpretation:
- `Pclass` is negatively correlated with survival because of how the classes are numerically coded (1 = 1st class, 3 = 3rd class) — a negative correlation here means *lower* class numbers (i.e., higher-class travel) are associated with *higher* survival.
- `Fare` is positively correlated with survival, consistent with fare acting as a rough proxy for class and cabin location.
- `Age` and `Family_Size` each show weak linear correlation with survival individually; as shown in Sections 4 and 6, their relationship with survival is non-linear and only becomes visible when the data is segmented into groups.
- **Correlation does not imply causation.** These figures describe statistical association in this dataset, not a causal mechanism, and none of these variables are described as "predictors" here since no predictive model or feature-importance analysis was built as part of this EDA.

## 9. Anomalies and Data Quality Observations

- **High-fare outliers:** 9 passengers paid $262.38–$512.33 for their tickets, all in 1st class, several traveling as families (e.g., the Fortune family, the Ryerson family). These are treated as legitimate high-value group-booking outliers rather than data errors, and are retained rather than removed.
- **Zero-fare records:** 15 passengers have a fare of exactly $0.00, all male, spread across all three classes. Only 1 of these 15 survived. These are plausible real-world records (e.g., crew, company employees, or comped tickets) rather than clear data-entry errors, so they are flagged as anomalies for downstream review rather than altered or deleted.
- **Small-sample categories:** the "the Countess" title (n=1) and family sizes of 8 (n=6) and 11 (n=7) each rely on very few records. Their extreme survival percentages (100% and 0% respectively) are reported for transparency but should not be treated as statistically reliable trends.

## 10. Five Key Insights

**Insight 1 — Sex.** Survival rate differed substantially by sex: 74.2% for female passengers versus 18.9% for male passengers (n=314 and n=577 respectively). This is the largest gap among the major categorical variables analyzed. This pattern is consistent with the historical "women and children first" evacuation practice, although the dataset alone cannot establish the cause.

**Insight 2 — Passenger Class.** Survival rate decreased steadily across passenger classes: 63.0% (1st, n=216) → 47.3% (2nd, n=184) → 24.2% (3rd, n=491).

**Insight 3 — Fare.** Fare showed a positive relationship with survival (r = +0.26) and differed substantially by passenger class, with 1st-class fares visibly higher and more spread out than 2nd or 3rd class.

**Insight 4 — Family Size.** Family size showed a non-linear relationship with survival: solo travelers (30.4%, n=537) had a lower observed survival rate than passengers in small-to-medium families of 2–4 people (55–72%), while very large family groups had extremely low observed survival rates (0%, n=6–7) but require cautious interpretation because of their small sample sizes.

**Insight 5 — Title.** Passenger title showed substantial differences in observed survival rates (Mrs 79.4%, Miss 70.3%, Master 57.5%, Rare 31.8%, Mr 15.7%), but the smallest categories (e.g., "the Countess," n=1) require cautious interpretation given their limited sample size.

**Bonus Insight — Port of Embarkation.** Passengers who embarked at Cherbourg had a higher survival rate (55.4%, n=168) than those from Southampton (33.9%, n=646) or Queenstown (39.0%, n=77). This is likely a confounding effect of class composition — a larger share of Cherbourg passengers traveled in 1st class — rather than a direct effect of the embarkation port itself.

## 11. Conclusion

EDA indicates that survival outcomes varied substantially across sex and passenger class, while fare, family size, and title also showed meaningful patterns. Several extreme observations (very high fares, zero fares, single-passenger title categories, and very large family groups) were identified and retained because they may represent legitimate historical records rather than data errors. These findings describe associations observed in this specific dataset; they are not causal claims and are not based on a predictive model.

## 12. How to Reproduce

```bash
pip install pandas matplotlib seaborn
python3 eda_analysis.py
```

Running the script prints all summary statistics and group breakdowns to the console and (re)generates all six charts into the `charts/` folder, which is created automatically if it does not already exist.
