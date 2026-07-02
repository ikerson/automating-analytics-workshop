# Session 4 Exercise — Pandas Basics
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
#   python exercises/session_04_exercise.py

import pandas as pd

# TODO: Load the CSV file
df = pd.read_csv("___")

# 2. Inspect the data
print(df.head())
print(df.info())

# TODO: Select only the five columns listed in the task
df = df[["___", "___", "___", "___", "___"]]

# TODO: Drop rows where phone is missing
df = df.dropna(subset=["___"])

print(f"{len(df)} rows remaining after dropping missing phone numbers.")

# TODO: Save the result — no row index
df.to_csv("___", index=False)

print("Done.")
