# Session 3 Exercise — Pandas Basics
#
# Task:
#   1. Load exercises/data/outreach_contacts.csv
#   2. Print the first 5 rows and a column summary
#   3. Select only these columns: student_id, first_name, last_name, phone, zip_code
#   4. Drop rows where phone is missing
#   5. Print how many rows remain
#   6. Save the result to exercises/data/outreach_contacts_cleaned.csv
#
# Run from the repo root:
#   python exercises/session_03_exercise.py

import pandas as pd

# TODO: Load outreach_contacts.csv using pd.read_csv()
# Hint: path is exercises/data/outreach_contacts.csv


# TODO: Print the first 5 rows with .head()


# TODO: Print a column summary with .info()


# TODO: Select only these columns: student_id, first_name, last_name, phone, zip_code
# Hint: df[['col1', 'col2', ...]]


# TODO: Drop rows where phone is missing
# Hint: df.dropna(subset=['phone'])


# TODO: Print how many rows remain
# Hint: len(df)


# TODO: Save the result to exercises/data/outreach_contacts_cleaned.csv
# Hint: df.to_csv('path/to/file.csv', index=False)


print("Done.")


# ---------------------------------------------------------------------------
# Answer — uncomment to check your work
# ---------------------------------------------------------------------------

# import pandas as pd
#
# df = pd.read_csv('exercises/data/outreach_contacts.csv')
# print(df.head())
# print(df.info())
#
# df = df[['student_id', 'first_name', 'last_name', 'phone', 'zip_code']]
# df = df.dropna(subset=['phone'])
# print(f"{len(df)} rows remaining after dropping missing phone numbers.")
# df.to_csv('exercises/data/outreach_contacts_cleaned.csv', index=False)
# print("Done.")
