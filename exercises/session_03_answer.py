# Session 3 Exercise — Pandas Basics (Answer)
#
# Run from the repo root:
#   python exercises/session_03_answer.py

import pandas as pd

df = pd.read_csv('exercises/data/outreach_contacts.csv')
print(df.head())
print(df.info())

df = df[['student_id', 'first_name', 'last_name', 'phone', 'zip_code']]
df = df.dropna(subset=['phone'])
print(f"{len(df)} rows remaining after dropping missing phone numbers.")
df.to_csv('exercises/data/outreach_contacts_cleaned.csv', index=False)
print("Done.")
