# Titanic Survival Analytics — Final Case Study

**SWYNEX Data Analytics Internship — Task 4: Final Data Analytics Project**
**Author:** Divyanshu Batham
**Repository contents:** this document, `titanic_raw.csv`, `titanic_cleaned.csv`, `clean_data.py`, `README.md` (Task 1), `eda_analysis.py`, `EDA_REPORT.md`, `charts/`, `All_Charts.pdf` (Task 2), `titanic_dashboard.html` (Task 3)

---

## 1. Problem Statement

On April 15, 1912, the RMS Titanic sank after striking an iceberg, resulting in the deaths of over 1,500 of the estimated 2,224 passengers and crew. This project asks: **which passenger characteristics were associated with higher or lower observed survival rates, and what patterns can a data team extract from imperfect historical records to inform how such data should be collected, cleaned, and communicated?**

This matters beyond a historical curiosity — the project exercises the full analytics lifecycle a business analyst uses on any raw dataset: assess data quality, clean responsibly, explore and quantify patterns, visualize findings for a non-technical audience, and communicate insights without overstating what the data can prove.

**Guiding questions:**
1. Did sex, passenger class, fare, family size, or title show a meaningful association with survival?
2. What data quality issues existed in the raw dataset, and how should they be handled defensibly?
3. What actionable, correctly-caveated insights can be communicated to a non-technical stakeholder via an interactive dashboard?

---

## 2. Dataset Information

- **Source:** [Titanic passenger dataset](https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv) — a widely used public dataset, 891 passenger records, 12 original columns.
- **Fields:** PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked.
- **Target variable:** `Survived` (0 = died, 1 = survived). Overall base rate: 38.4% survived.

---

## 3. Data Cleaning Process (Task 1 summary)

Full detail in `README.md` / `clean_data.py`. Key steps:

| Issue | Finding | Action |
|---|---|---|
| Missing `Age` | 177 missing (19.9%) | Imputed with the median age within each Pclass + Sex group |
| Missing `Cabin` | 687 missing (77.1%) | Converted to a boolean `Has_Cabin` flag; text field set to "Unknown" |
| Missing `Embarked` | 2 missing | Filled with the mode (Southampton) |
| Duplicates | 0 exact duplicates, 0 duplicate IDs | Verified, dedup logic retained for future data pulls |
| Data type optimization | `Pclass`, `Survived`, `Sex`, `Embarked` stored as raw ints/strings | Converted to categorical dtype |
| Inconsistent `Name`/`Title` formatting | Mixed and foreign-language titles (Mlle, Mme, Dr, Rev, etc.) | Extracted and standardized into a clean `Title` column |
| Inconsistent `Embarked` codes | Single-letter port codes | Added human-readable `Embarked_Full` column |

**Result:** 891 rows × 15 columns, zero missing values, consistent types and categories.

---

## 4. Exploratory Analysis & Key Statistics (Task 2 summary)

Full detail, all charts, and methodology in `EDA_REPORT.md` / `eda_analysis.py`. Headline statistics (all recalculated directly from the cleaned dataset):

| Metric | Value |
|---|---|
| Total passengers | 891 |
| Survivors / Non-survivors | 342 / 549 |
| Overall survival rate | 38.4% |
| Avg age / Avg fare | 29.1 / $32.20 |
| Avg family size | 1.9 |

**Key associations observed with survival:**
- **Sex** — the largest gap of any variable analyzed: 74.2% (female) vs. 18.9% (male).
- **Passenger class** — 63.0% (1st) → 47.3% (2nd) → 24.2% (3rd).
- **Class + sex combined** — a large observed contrast in survival rates: 1st-class female passengers (96.8%) vs. 3rd-class male passengers (13.5%).
- **Fare** — positively associated with survival (r = +0.26) and varied substantially across passenger classes.
- **Family size** — a non-linear pattern: solo travelers (30.4%) and very large families (0%, but n=6–7, too small to generalize) fared worse than small-to-medium families of 2–4 (55–72%).
- **Title** (engineered from `Name`) — Mrs 79.4%, Miss 70.3%, Master 57.5%, Rare 31.8%, Mr 15.7%, with the single-passenger "Countess" category explicitly flagged as not generalizable.

All of these are reported as **statistical associations observed in this dataset, not causal claims**, consistent with the scope of exploratory analysis rather than a predictive model.

---

## 5. Interactive Dashboard (Task 3 summary)

**Live dashboard:** `titanic_dashboard.html` — a self-contained, dependency-free interactive dashboard (no external libraries, charts render as inline SVG for maximum reliability).

**Features:**
- 5 live KPI cards (Passengers, Survival Rate, Avg Age, Avg Fare, Avg Family Size)
- 3 working filters: Passenger Class, Sex, Embarkation Port (fully combinable)
- 6 charts, all recalculating from the filtered data in real time: Survival by Class & Sex, Survival by Title, Survival by Family Size, Survival by Sex, Average Fare by Class, and Age Distribution by Survival Outcome
- Small-sample categories (e.g., Countess, very large families) are flagged in-dashboard rather than presented as reliable trends
- A "Reset Filters" control restores the full 891-passenger view

The dashboard was tested using different filter combinations to confirm that the KPIs and visualizations update according to the selected filters and that the Reset Filters control restores the full dataset view.

---

## 6. Key Analytical / Business Insights

Framed for a non-technical stakeholder, with appropriate caution on causality:

1. **Sex showed the largest observed difference in survival rate among the major categorical variables analyzed.** Female passengers had a survival rate of 74.2%, compared with 18.9% for male passengers. The dataset alone cannot establish the reason for this difference.
2. **Passenger class and sex showed a strong combined difference in observed survival rates.** The survival rate was 96.8% for 1st-class female passengers compared with 13.5% for 3rd-class male passengers. This describes an observed association in the dataset and does not establish the underlying cause.
3. **Family size showed a non-linear pattern in observed survival rates.** Solo travelers had a survival rate of 30.4%, while passengers in small-to-medium family groups of 2–4 had higher observed survival rates of approximately 55–72%. Very large family groups had extremely low observed survival rates, but these groups had very small sample sizes and should not be generalized.
4. **Fare showed a positive association with survival (r = +0.26) and varied substantially across passenger classes.** This relationship should be interpreted cautiously because fare is also related to passenger class and other characteristics in the dataset.
5. **Passenger title also showed differences in observed survival rates.** Mrs, Miss, Master, Rare, and Mr had survival rates of 79.4%, 70.3%, 57.5%, 31.8%, and 15.7%, respectively. Small categories, such as the Countess (n=1), should not be treated as generalizable trends.
6. **Data completeness was uneven by field.** Cabin data was missing for over three-quarters of passengers — any analysis leaning heavily on cabin location should be treated as exploratory at best, not a firm conclusion.

**Observation for future data collection:** if this were an ongoing operational dataset (e.g., a modern cruise/ferry manifest), prioritizing complete capture of cabin/location and boarding fields would be reasonable, since these fields had the highest missingness and the most analytical value in this dataset.

---

## 7. Limitations

- This is descriptive, exploratory analysis — no predictive model or feature-importance analysis was built, so no variable is described as a "predictor" in the statistical sense.
- Several small-sample categories (single-passenger titles, large family sizes) produced extreme percentages that are reported for transparency but are not statistically reliable.
- Correlation values describe association only; none of the relationships reported here establish causation.

---

## 8. How to Reproduce This Project

```bash
# Task 1 — clean the raw dataset
pip install pandas
python3 clean_data.py

# Task 2 — run the full exploratory analysis and regenerate charts
pip install pandas matplotlib seaborn
python3 eda_analysis.py

# Task 3 — open the dashboard
open titanic_dashboard.html   # or double-click in any browser; no server or install required
```

## 9. Repository Structure

```
├── CASE_STUDY.md              ← this document (Task 4)
├── titanic_raw.csv            ← original dataset (Task 1)
├── titanic_cleaned.csv        ← cleaned dataset (Task 1)
├── clean_data.py              ← cleaning script (Task 1)
├── README.md                  ← Task 1 write-up
├── eda_analysis.py            ← EDA script (Task 2)
├── EDA_REPORT.md              ← full EDA write-up (Task 2)
├── charts/                    ← 6 chart PNGs (Task 2)
├── All_Charts.pdf             ← all charts combined (Task 2)
└── titanic_dashboard.html     ← interactive dashboard (Task 3)
```
