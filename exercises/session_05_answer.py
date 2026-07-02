# Session 5 Exercise — Merging Three Sources (Answer)
#
# Run from the repo root:
#   python exercises/session_05_answer.py

from pathlib import Path
import pandas as pd

DATA_DIR = Path('exercises') / 'data'

contacts = pd.read_csv(DATA_DIR / 'outreach_contacts.csv')
survey = pd.read_csv(DATA_DIR / 'school_survey_2019.csv')
schools = pd.read_csv(DATA_DIR / 'middle_schools_2019.csv')

merged = contacts.merge(survey[['student_id', 'ncessch']], on='student_id', how='left')

merged['ncessch'] = merged['ncessch'].astype(str).str.split('.').str[0]
schools['ncessch'] = schools['ncessch'].astype(str).str.split('.').str[0]

merged = merged.merge(schools, on='ncessch', how='left')

unmatched = merged[merged['school_name'].isna()]
print(f"Contacts without a school match: {len(unmatched)}")
print(unmatched[['student_id', 'first_name', 'last_name']])

merged.to_csv(DATA_DIR / 'merged_contacts.csv', index=False)
print("Done.")
