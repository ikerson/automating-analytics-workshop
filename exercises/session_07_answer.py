# Session 7 Exercise — Creating Visualizations (Answer)
#
# Run from the repo root:
#   python exercises/session_07_answer.py

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = Path('exercises') / 'data'

merged = pd.read_csv(DATA_DIR / 'merged_contacts.csv')

matched = merged.dropna(subset=['school_name'])
top5 = (
    matched.groupby('school_name')
    .agg(student_count=('student_id', 'count'))
    .reset_index()
    .sort_values('student_count', ascending=False)
    .head(5)
)

fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(top5['school_name'], top5['student_count'], color='steelblue')
ax.set_xlabel("Number of Contacts")
ax.set_title("Top 5 Middle Schools by Contacts")
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(DATA_DIR / 'top_schools_chart.png')
plt.close()
print("Done.")
