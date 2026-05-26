# Session 11 Exercise — Generating the Excel Report (Answer)
#
# Run from the repo root:
#   python exercises/session_11_answer.py

from pathlib import Path
import pandas as pd

DATA_DIR = Path('exercises') / 'data'

contacts = pd.read_csv(DATA_DIR / 'merged_contacts.csv')
size_summary = pd.read_csv(DATA_DIR / 'size_summary.csv')

with pd.ExcelWriter(DATA_DIR / 'contacts_report.xlsx', engine='openpyxl') as writer:
    contacts.to_excel(writer, sheet_name='Contacts', index=False)
    size_summary.to_excel(writer, sheet_name='By School Size', index=False)

print("Saved contacts_report.xlsx")
