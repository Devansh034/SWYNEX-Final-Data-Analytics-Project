# Data Cleaning & Preparation — Titanic Dataset

## Dataset
- **Source:** [Titanic passenger dataset](https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv) (public, 891 records, 12 columns)
- **Files:**
  - `titanic_raw.csv` — original, unmodified dataset
  - `titanic_cleaned.csv` — cleaned dataset (891 rows, 15 columns)
  - `clean_data.py` — script containing all cleaning logic (fully reproducible)

## Issues Found & How They Were Fixed

### 1. Missing Values
| Column | Missing | Action Taken |
|---|---|---|
| `Age` | 177 (19.9%) | Imputed using the **median age within each Pclass + Sex group** (more accurate than a single overall median, since age correlates with class and gender). |
| `Cabin` | 687 (77.1%) | Too sparse to impute reliably. Converted into a new boolean column `Has_Cabin` (1/0) to preserve the signal, and filled the text field with `"Unknown"`. |
| `Embarked` | 2 (0.2%) | Filled with the mode (most frequent port, "S" — Southampton). |

### 2. Duplicate Records
- Checked for exact duplicate rows (excluding the ID column) → **0 found**.
- Checked for duplicate `PassengerId` values (a data-integrity check) → **0 found**.
- Deduplication logic is included in the script regardless, so it's safe to rerun on future data pulls that may contain duplicates.

### 3. Incorrect Data Types
- `Pclass`, `Survived`, `Sex`, and `Embarked` were stored as raw integers/strings but are actually **categorical variables** — converted to `category` dtype for correctness and memory efficiency.

### 4. Inconsistent Values
- The `Name` field mixed formats (e.g., `"Braund, Mr. Owen Harris"`). Extracted a clean `Title` column (Mr, Mrs, Miss, Master, Rare, etc.) and **standardized rare/foreign-language titles** (e.g., `Mlle` → `Miss`, `Mme` → `Mrs`, `Dr`/`Rev`/`Col` etc. → `Rare`).
- `Embarked` was stored as single-letter port codes (S/C/Q). Added a human-readable `Embarked_Full` column (Southampton, Cherbourg, Queenstown) while keeping the original code column intact.
- `Sex` values standardized to Title Case for display consistency.
- Flagged 15 records with `Fare == 0` as a data-quality note for downstream analysts (not altered, since zero fares can be legitimate for crew/comp tickets, but worth reviewing).

## New Columns Added
- `Has_Cabin` — 1 if cabin info was originally present, 0 if not
- `Title` — extracted/standardized title from passenger name
- `Embarked_Full` — full port name for readability

## How to Reproduce
```bash
pip install pandas
python3 clean_data.py
```

## Result
- **Before:** 891 rows × 12 columns, 866 missing values across 3 columns
- **After:** 891 rows × 15 columns, 0 missing values, consistent types and categories
