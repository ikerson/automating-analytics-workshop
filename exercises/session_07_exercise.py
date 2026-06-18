# Session 7 Exercise — Generating the Excel Report
#
# Task:
#   1. Load exercises/data/merged_contacts.csv (produced in the Session 4 exercise)
#   2. Load exercises/data/size_summary.csv (produced in the Session 5 exercise)
#   3. Write both DataFrames to a single Excel file exercises/data/contacts_report.xlsx
#      - Sheet 1: "Contacts"  — the merged contacts data
#      - Sheet 2: "By School Size" — the size summary
#   4. Use index=False on both sheets
#
# Run from the repo root:
#   python exercises/session_07_exercise.py

___ = None  # replace each ___ with the correct value

from pathlib import Path
import pandas as pd

DATA_DIR = Path('exercises') / 'data'

# TODO: Load merged_contacts.csv
contacts = pd.read_csv(DATA_DIR / "___")

# TODO: Load size_summary.csv
size_summary = pd.read_csv(DATA_DIR / "___")

# TODO: Fill in the output filename and engine
with pd.ExcelWriter(DATA_DIR / "___", engine="___") as writer:
    # TODO: Fill in the sheet name for the contacts data
    contacts.to_excel(writer, sheet_name="___", index=False)
    # TODO: Fill in which DataFrame goes on the "By School Size" sheet
    ___.to_excel(writer, sheet_name='By School Size', index=False)

print("Saved contacts_report.xlsx")
