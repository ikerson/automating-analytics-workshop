# Session 11 Exercise — Generating the Excel Report
#
# Task:
#   1. Load exercises/data/merged_contacts.csv (produced in the Session 8 exercise)
#   2. Load exercises/data/size_summary.csv (produced in the Session 9 exercise)
#   3. Write both DataFrames to a single Excel file exercises/data/contacts_report.xlsx
#      - Sheet 1: "Contacts"  — the merged contacts data
#      - Sheet 2: "By School Size" — the size summary
#   4. Use index=False on both sheets
#
# Run from the repo root:
#   python exercises/session_11_exercise.py

from pathlib import Path
import pandas as pd

DATA_DIR = Path('exercises') / 'data'

# TODO: Load merged_contacts.csv
# Hint: contacts = pd.read_csv(DATA_DIR / 'merged_contacts.csv')


# TODO: Load size_summary.csv
# Hint: size_summary = pd.read_csv(DATA_DIR / 'size_summary.csv')


# TODO: Write both DataFrames to contacts_report.xlsx using pd.ExcelWriter
# Use engine='openpyxl' and index=False on both sheets
# Hint: with pd.ExcelWriter(DATA_DIR / 'contacts_report.xlsx', engine='openpyxl') as writer:
#     contacts.to_excel(writer, sheet_name='Contacts', index=False)
#     size_summary.to_excel(writer, sheet_name='By School Size', index=False)


print("Saved contacts_report.xlsx")
