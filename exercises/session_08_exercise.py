# Session 8 Exercise — Merging Three Sources
#
# Task:
#   1. Load exercises/data/outreach_contacts.csv
#   2. Load exercises/data/school_survey_2019.csv
#   3. Load exercises/data/middle_schools_2019.csv
#   4. Merge contacts with survey on student_id (left join)
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

# TODO: Load outreach_contacts.csv
# Hint: contacts = pd.read_csv(DATA_DIR / 'outreach_contacts.csv')


# TODO: Load school_survey_2019.csv
# Hint: survey = pd.read_csv(DATA_DIR / 'school_survey_2019.csv')


# TODO: Load middle_schools_2019.csv
# Hint: schools = pd.read_csv(DATA_DIR / 'middle_schools_2019.csv')


# TODO: Merge contacts with survey on student_id (left join)
# Hint: merged = contacts.merge(survey, on='student_id', how='left')


# TODO: Normalize ncessch to a clean string in both DataFrames
# ncessch may be stored as a float (e.g. 340183001982.0) — strip the decimal
# Hint: merged['ncessch'] = merged['ncessch'].astype(str).str.split('.').str[0]
# Hint: schools['ncessch'] = schools['ncessch'].astype(str).str.split('.').str[0]


# TODO: Merge result with schools on ncessch (left join)
# Hint: merged = merged.merge(schools, on='ncessch', how='left')


# TODO: Print how many contacts have no school match (school_name is NaN)
# Hint: unmatched = merged[merged['school_name'].isna()]
# Hint: print(f"Contacts without a school match: {len(unmatched)}")


# TODO: Print student_id, first_name, and last_name of unmatched contacts
# Hint: print(unmatched[['student_id', 'first_name', 'last_name']])


# TODO: Save to exercises/data/merged_contacts.csv (index=False)
# Hint: merged.to_csv(DATA_DIR / 'merged_contacts.csv', index=False)


print("Done.")


# ---------------------------------------------------------------------------
# Answer — uncomment to check your work
# ---------------------------------------------------------------------------

# from pathlib import Path
# import pandas as pd
#
# DATA_DIR = Path('exercises') / 'data'
#
# contacts = pd.read_csv(DATA_DIR / 'outreach_contacts.csv')
# survey = pd.read_csv(DATA_DIR / 'school_survey_2019.csv')
# schools = pd.read_csv(DATA_DIR / 'middle_schools_2019.csv')
#
# merged = contacts.merge(survey, on='student_id', how='left')
#
# merged['ncessch'] = merged['ncessch'].astype(str).str.split('.').str[0]
# schools['ncessch'] = schools['ncessch'].astype(str).str.split('.').str[0]
#
# merged = merged.merge(schools, on='ncessch', how='left')
#
# unmatched = merged[merged['school_name'].isna()]
# print(f"Contacts without a school match: {len(unmatched)}")
# print(unmatched[['student_id', 'first_name', 'last_name']])
#
# merged.to_csv(DATA_DIR / 'merged_contacts.csv', index=False)
# print("Done.")
