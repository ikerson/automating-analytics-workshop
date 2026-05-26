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
# Hint: merged = pd.read_csv(DATA_DIR / 'merged_contacts.csv')


# TODO: Create a school_size column using pd.cut() on the enrollment column
# Hint: merged['school_size'] = pd.cut(
#     merged['enrollment'],
#     bins=[0, 300, 700, float('inf')],
#     labels=['Small (<300)', 'Medium (300-700)', 'Large (700+)'],
# )


# TODO: Print value_counts() on city_location
# Hint: print(merged['city_location'].value_counts())


# TODO: groupby school_size, aggregate student count and average enrollment
# Use observed=True to include only categories that appear in the data
# Hint: size_summary = (
#     merged.dropna(subset=['school_size'])
#     .groupby('school_size', observed=True)
#     .agg(student_count=('student_id', 'count'), avg_enrollment=('enrollment', 'mean'))
#     .reset_index()
# )
# Hint: print(size_summary)


# TODO: Save size_summary to exercises/data/size_summary.csv (index=False)
# Hint: size_summary.to_csv(DATA_DIR / 'size_summary.csv', index=False)


print("Done.")


# ---------------------------------------------------------------------------
# Answer — uncomment to check your work
# ---------------------------------------------------------------------------

# from pathlib import Path
# import pandas as pd
#
# DATA_DIR = Path('exercises') / 'data'
#
# merged = pd.read_csv(DATA_DIR / 'merged_contacts.csv')
#
# merged['school_size'] = pd.cut(
#     merged['enrollment'],
#     bins=[0, 300, 700, float('inf')],
#     labels=['Small (<300)', 'Medium (300-700)', 'Large (700+)'],
# )
#
# print(merged['city_location'].value_counts())
#
# size_summary = (
#     merged.dropna(subset=['school_size'])
#     .groupby('school_size', observed=True)
#     .agg(student_count=('student_id', 'count'), avg_enrollment=('enrollment', 'mean'))
#     .reset_index()
# )
# print(size_summary)
#
# size_summary.to_csv(DATA_DIR / 'size_summary.csv', index=False)
# print("Done.")
