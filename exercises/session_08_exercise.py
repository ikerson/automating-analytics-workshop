# Session 8 Exercise — Merging the Three Sources
#
# Task:
#   1. Load exercises/data/outreach_contacts.csv (25 contacts, student IDs 101-125)
#   2. Load exercises/data/school_survey_2019.csv (school names for student IDs 101-120)
#   3. Merge the two DataFrames on student_id using a left join
#   4. Print how many contacts have no school match (school_name is NaN)
#   5. Print the first and last names of those unmatched contacts
#   6. Save the merged result to exercises/data/merged_contacts.csv (no index)
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


# TODO: Merge contacts with survey on student_id using a left join
# Hint: merged = contacts.merge(survey, on='student_id', how='left')


# TODO: Print how many contacts have no school match
# Hint: unmatched = merged[merged['school_name'].isna()]
# Hint: print(f"Contacts without a school match: {len(unmatched)}")


# TODO: Print first_name and last_name of unmatched contacts
# Hint: print(unmatched[['student_id', 'first_name', 'last_name']])


# TODO: Save the merged result to exercises/data/merged_contacts.csv (index=False)
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
#
# merged = contacts.merge(survey, on='student_id', how='left')
#
# unmatched = merged[merged['school_name'].isna()]
# print(f"Contacts without a school match: {len(unmatched)}")
# print(unmatched[['student_id', 'first_name', 'last_name']])
#
# merged.to_csv(DATA_DIR / 'merged_contacts.csv', index=False)
# print("Done.")
