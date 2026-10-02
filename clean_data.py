"""
Data Cleaning & Preparation - Titanic Dataset
Source: https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv
"""
import pandas as pd
import numpy as np

# --- 1. LOAD RAW DATA ---
df = pd.read_csv("titanic_raw.csv")
print(f"Raw shape: {df.shape}")

# --- 2. CHECK & HANDLE DUPLICATES ---
# a) Exact duplicate rows (excluding the unique ID column)
exact_dupes = df.drop(columns=['PassengerId']).duplicated().sum()
print(f"Exact duplicate rows found: {exact_dupes}")

# b) Duplicate PassengerId (would indicate a data integrity issue)
id_dupes = df['PassengerId'].duplicated().sum()
print(f"Duplicate PassengerId found: {id_dupes}")

df = df.drop_duplicates(subset=['PassengerId'], keep='first')
df = df.drop_duplicates(subset=df.columns.difference(['PassengerId']), keep='first')

# --- 3. HANDLE MISSING VALUES ---
missing_before = df.isnull().sum()
print("\nMissing values before cleaning:\n", missing_before[missing_before > 0])

# Age: 177 missing (~20%) -> impute using median age within each Pclass/Sex group
# (more accurate than a single global median, since age varies by class/gender)
df['Age'] = df.groupby(['Pclass', 'Sex'])['Age'].transform(
    lambda x: x.fillna(x.median())
)
df['Age'] = df['Age'].fillna(df['Age'].median())  # safety net for any remaining gaps
df['Age'] = df['Age'].round(1)

# Cabin: 687 missing (~77%) -> too sparse to impute meaningfully.
# Convert to a boolean flag (Has_Cabin) which preserves signal without inventing data.
df['Has_Cabin'] = df['Cabin'].notna().astype(int)
df['Cabin'] = df['Cabin'].fillna('Unknown')

# Embarked: 2 missing -> fill with the mode (most frequent port)
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])

# Fare: check for zero-fare records (data entry issue, not truly "free")
zero_fares = (df['Fare'] == 0).sum()
print(f"\nZero-value fares found: {zero_fares} (kept, but flagged for review)")

missing_after = df.isnull().sum()
print("\nMissing values after cleaning:\n", missing_after[missing_after > 0] if missing_after.sum() else "None")

# --- 4. DATA TYPE OPTIMIZATION ---
# Pclass, Survived, Sex, Embarked are converted to categorical dtype
# to better represent their meaning and improve memory efficiency
df['Pclass'] = df['Pclass'].astype('category')
df['Survived'] = df['Survived'].astype('category')
df['Sex'] = df['Sex'].astype('category')
df['Embarked'] = df['Embarked'].astype('category')

# --- 5. STANDARDIZE INCONSISTENT VALUES ---
# Name field mixes formats ("Last, Title. First"); extract a clean Title column
df['Title'] = df['Name'].str.extract(r',\s*([^\.]+)\.')
title_map = {
    'Mlle': 'Miss', 'Ms': 'Miss', 'Mme': 'Mrs',
    'Lady': 'Rare', 'Countess': 'Rare', 'Capt': 'Rare', 'Col': 'Rare',
    'Don': 'Rare', 'Dr': 'Rare', 'Major': 'Rare', 'Rev': 'Rare',
    'Sir': 'Rare', 'Jonkheer': 'Rare', 'Dona': 'Rare'
}
df['Title'] = df['Title'].str.strip().replace(title_map)

# Embarked stored as single-letter codes (S/C/Q) -> map to full, readable names
embarked_map = {'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'}
df['Embarked_Full'] = df['Embarked'].map(embarked_map)

# Sex -> Title Case for readability
df['Sex'] = df['Sex'].str.title()

# --- 6. FINAL CHECKS ---
print(f"\nFinal shape: {df.shape}")
print(f"Final dtypes:\n{df.dtypes}")
assert df.isnull().sum().sum() == 0, "Missing values remain!"
assert df.duplicated(subset=['PassengerId']).sum() == 0, "Duplicate IDs remain!"

# --- 7. SAVE CLEANED DATASET ---
df.to_csv("titanic_cleaned.csv", index=False)
print("\nSaved cleaned dataset -> titanic_cleaned.csv")
