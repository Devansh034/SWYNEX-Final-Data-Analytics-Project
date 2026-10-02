"""
Exploratory Data Analysis - Titanic Dataset (cleaned)
Task 2: Data Analytics Internship

Reads the Task 1 cleaned dataset, computes summary statistics and
group-level survival breakdowns, flags anomalies, and generates charts.
All numbers are calculated directly from titanic_cleaned.csv (no
hard-coded statistics) so this script can be re-run to verify the
figures quoted in EDA_REPORT.md.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 120

DATA_PATH = "titanic_cleaned.csv"
CHARTS_DIR = "charts"


def load_data(path=DATA_PATH):
    """Load the cleaned dataset and restore convenient dtypes for analysis."""
    df = pd.read_csv(path)
    df['Pclass'] = df['Pclass'].astype(int)
    df['Survived_Label'] = df['Survived'].map({0: 'Died', 1: 'Survived'})
    df['Family_Size'] = df['SibSp'] + df['Parch'] + 1
    return df


def print_summary_statistics(df):
    """Print overall counts and descriptive statistics for Age and Fare."""
    total = len(df)
    survivors = int(df['Survived'].sum())
    non_survivors = total - survivors

    print("=== SUMMARY STATISTICS ===")
    print(f"Total passengers: {total}")
    print(f"Survivors: {survivors}")
    print(f"Non-survivors: {non_survivors}")
    print(f"Overall survival rate: {survivors / total:.1%}")

    for col in ['Age', 'Fare']:
        print(f"\n{col} statistics:")
        print(f"  mean:   {df[col].mean():.2f}")
        print(f"  median: {df[col].median():.2f}")
        print(f"  std:    {df[col].std():.2f}")
        print(f"  min:    {df[col].min():.2f}")
        print(f"  max:    {df[col].max():.2f}")

    print("\nFamily size (SibSp + Parch + 1) statistics:")
    print(f"  mean:   {df['Family_Size'].mean():.2f}")
    print(f"  median: {df['Family_Size'].median():.2f}")


def print_group_breakdowns(df):
    """Print survival rate broken down by the key categorical variables."""
    print("\n=== SURVIVAL BY SEX ===")
    print(df.groupby('Sex')['Survived'].agg(['mean', 'count']))

    print("\n=== SURVIVAL BY CLASS ===")
    print(df.groupby('Pclass')['Survived'].agg(['mean', 'count']))

    print("\n=== SURVIVAL BY SEX + CLASS ===")
    print(df.groupby(['Pclass', 'Sex'])['Survived'].agg(['mean', 'count']))

    print("\n=== SURVIVAL BY FAMILY SIZE ===")
    print(df.groupby('Family_Size')['Survived'].agg(['mean', 'count']))

    print("\n=== SURVIVAL BY TITLE ===")
    print(df.groupby('Title')['Survived'].agg(['mean', 'count']).sort_values('mean', ascending=False))

    print("\n=== SURVIVAL BY EMBARKATION PORT ===")
    print(df.groupby('Embarked_Full')['Survived'].agg(['mean', 'count']))


def print_correlations(df):
    """Print the correlation of numeric variables with Survived."""
    print("\n=== CORRELATION WITH SURVIVED ===")
    corr_cols = ['Survived', 'Pclass', 'Age', 'Fare', 'Family_Size', 'Has_Cabin']
    print(df[corr_cols].corr()['Survived'].sort_values(ascending=False))
    return df[corr_cols].corr()


def print_anomalies(df):
    """Flag notable outliers: very high fares and zero fares."""
    print("\n=== HIGH-FARE OUTLIERS (top 1%) ===")
    high_fare_cutoff = df['Fare'].quantile(0.99)
    high_fare = df[df['Fare'] > high_fare_cutoff][['Name', 'Pclass', 'Fare', 'Survived']]
    print(high_fare)

    print("\n=== ZERO-FARE RECORDS ===")
    zero_fare = df[df['Fare'] == 0][['Name', 'Pclass', 'Sex', 'Survived']]
    print(zero_fare)
    print(f"Count: {len(zero_fare)}, Survived: {int(zero_fare['Survived'].sum())}")


def make_charts(df, corr, out_dir=CHARTS_DIR):
    """Generate and save all charts used in the EDA report."""
    os.makedirs(out_dir, exist_ok=True)

    # 1. Survival rate by class and sex
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.barplot(data=df, x='Pclass', y='Survived', hue='Sex', ax=ax)
    ax.set_title('Survival Rate by Passenger Class and Sex')
    ax.set_xlabel('Passenger Class')
    ax.set_ylabel('Survival Rate')
    plt.tight_layout()
    plt.savefig(f'{out_dir}/01_survival_by_class_sex.png')
    plt.close()

    # 2. Age distribution by survival outcome
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.histplot(data=df, x='Age', hue='Survived_Label', bins=30, kde=True, ax=ax)
    ax.set_title('Age Distribution by Survival Outcome')
    ax.set_xlabel('Age')
    ax.set_ylabel('Number of Passengers')
    plt.tight_layout()
    plt.savefig(f'{out_dir}/02_age_distribution.png')
    plt.close()

    # 3. Fare distribution by class (log scale noted explicitly on the axis)
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.boxplot(data=df, x='Pclass', y='Fare', hue='Pclass', legend=False, ax=ax)
    ax.set_yscale('symlog')
    ax.set_title('Fare Distribution by Passenger Class (symlog scale)')
    ax.set_xlabel('Passenger Class')
    ax.set_ylabel('Fare, $ (symlog scale)')
    plt.tight_layout()
    plt.savefig(f'{out_dir}/03_fare_by_class.png')
    plt.close()

    # 4. Survival rate by family size (annotated with group counts)
    by_family = df.groupby('Family_Size')['Survived'].agg(['mean', 'count'])
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(by_family.index.astype(str), by_family['mean'], color='#4C72B0')
    for bar, count in zip(bars, by_family['count']):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f'n={count}', ha='center', fontsize=8)
    ax.set_title('Survival Rate by Family Size (labeled with group size n)')
    ax.set_xlabel('Family Size (SibSp + Parch + 1)')
    ax.set_ylabel('Survival Rate')
    ax.set_ylim(0, 1.15)
    plt.tight_layout()
    plt.savefig(f'{out_dir}/04_survival_by_family_size.png')
    plt.close()

    # 5. Correlation heatmap
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax)
    ax.set_title('Correlation Matrix (numeric variables)')
    plt.tight_layout()
    plt.savefig(f'{out_dir}/05_correlation_heatmap.png')
    plt.close()

    # 6. Survival rate by title (annotated with group counts)
    by_title = df.groupby('Title')['Survived'].agg(['mean', 'count']).sort_values('mean', ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(by_title.index, by_title['mean'], color='#55A868')
    for bar, count in zip(bars, by_title['count']):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f'n={count}', ha='center', fontsize=8)
    ax.set_title('Survival Rate by Title (labeled with group size n)')
    ax.set_xlabel('Title')
    ax.set_ylabel('Survival Rate')
    ax.set_ylim(0, 1.15)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{out_dir}/06_survival_by_title.png')
    plt.close()

    print(f"\nAll charts saved to {out_dir}/")


def main():
    df = load_data()
    print_summary_statistics(df)
    print_group_breakdowns(df)
    corr = print_correlations(df)
    print_anomalies(df)
    make_charts(df, corr)


if __name__ == "__main__":
    main()
