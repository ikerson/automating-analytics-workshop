# Session 9 Exercise — Aggregations and Summary Statistics
#
# Task:
#   1. Load exercises/data/merged_contacts.csv (produced in the Session 8 exercise)
#   2. Use pd.cut() on the enrollment column to create a school_size column
#      Bins: [0, 300, 700, inf]  Labels: ['Small (<300)', 'Medium (300-700)', 'Large (700+)']
#   3. Print value_counts() on city_location — how many contacts attended schools in each city?
#   4. Use groupby('school_size', observed=True) and .agg() to compute student count
#      and average enrollment per size bucket
#   5. Save the size summary to exercises/data/size_summary.csv (no index)
#
# Run from the repo root:
#   python exercises/session_09_exercise.py

from pathlib import Path
import pandas as pd

DATA_DIR = Path('exercises') / 'data'

# TODO: Load merged_contacts.csv
merged = pd.read_csv(DATA_DIR / "___")

# TODO: Create a school_size column — fill in the column name and the three labels
merged['school_size'] = pd.cut(
    merged["___"],
    bins=[0, 300, 700, float('inf')],
    labels=["___", "___", "___"],
)

# TODO: Print value_counts() on the city column
print(merged["___"].value_counts())

# TODO: Fill in the groupby column and the two aggregation columns
size_summary = (
    merged.dropna(subset=['school_size'])
    .groupby("___", observed=True)
    .agg(student_count=("___", "count"), avg_enrollment=("___", "mean"))
    .reset_index()
)
print(size_summary)

# TODO: Save the size summary — no row index
size_summary.to_csv(DATA_DIR / "___", index=False)
print("Done.")
