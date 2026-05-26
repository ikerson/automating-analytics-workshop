# Session 9 Exercise — Aggregations and Summary Statistics (Answer)
#
# Run from the repo root:
#   python exercises/session_09_answer.py

from pathlib import Path
import pandas as pd

DATA_DIR = Path('exercises') / 'data'

merged = pd.read_csv(DATA_DIR / 'merged_contacts.csv')

merged['school_size'] = pd.cut(
    merged['enrollment'],
    bins=[0, 300, 700, float('inf')],
    labels=['Small (<300)', 'Medium (300-700)', 'Large (700+)'],
)

print(merged['city_location'].value_counts())

size_summary = (
    merged.dropna(subset=['school_size'])
    .groupby('school_size', observed=True)
    .agg(student_count=('student_id', 'count'), avg_enrollment=('enrollment', 'mean'))
    .reset_index()
)
print(size_summary)

size_summary.to_csv(DATA_DIR / 'size_summary.csv', index=False)
print("Done.")
