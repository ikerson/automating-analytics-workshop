# Session 8 Exercise — Merging Three Sources
#
# Task:
#   1. Load exercises/data/outreach_contacts.csv
#   2. Load exercises/data/school_survey_2019.csv
#   3. Load exercises/data/middle_schools_2019.csv
#   4. Merge contacts with survey on student_id (left join) — only keep student_id and ncessch from survey
#   5. Normalize ncessch to a clean string in both DataFrames
#   6. Merge result with middle_schools on ncessch (left join)
#   7. Print how many contacts have no school match (school_name is NaN)
#   8. Print the first and last names of those unmatched contacts
#   9. Save the merged result to exercises/data/merged_contacts.csv (no index)
#
# Run from the repo root:
#   python exercises/session_08_exercise.py

from pathlib import Path
import pandas as pd

DATA_DIR = Path('exercises') / 'data'

# TODO: Load the three CSV files
contacts = pd.read_csv(DATA_DIR / "___")
survey = pd.read_csv(DATA_DIR / "___")
schools = pd.read_csv(DATA_DIR / "___")

# TODO: Merge contacts with survey — we only need student_id and ncessch from survey
merged = contacts.merge(survey[['student_id', 'ncessch']], on="___", how="___")

# 5. Normalize ncessch — stored as a float, strip the decimal
merged['ncessch'] = merged['ncessch'].astype(str).str.split('.').str[0]
schools['ncessch'] = schools['ncessch'].astype(str).str.split('.').str[0]

# TODO: Merge result with schools — fill in the join key and join type
merged = merged.merge(schools, on="___", how="___")

# TODO: Find contacts with no school match and print them
unmatched = merged[merged["___"].isna()]
print(f"Contacts without a school match: {len(unmatched)}")
print(unmatched[['student_id', 'first_name', 'last_name']])

# TODO: Save the merged result — no row index
merged.to_csv(DATA_DIR / "___", index=False)
print("Done.")
