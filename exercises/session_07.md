# Session 7 Exercise — Generating the Excel Report

> Optional enrichment — complete during the session if time allows, or finish independently on your fork.

## Your Task

1. Load `exercises/data/merged_contacts.csv` (produced in the Session 4 exercise)
2. Load `exercises/data/size_summary.csv` (produced in the Session 5 exercise)
3. Write both DataFrames to a single Excel file `exercises/data/contacts_report.xlsx`
   - Sheet 1: `"Contacts"` — the merged contacts data
   - Sheet 2: `"By School Size"` — the size summary
4. Use `index=False` on both sheets

## Starter Script

Open [`session_07_exercise.py`](session_07_exercise.py) and fill in the blanks marked with `# TODO:`. Note: this exercise predefines `___ = None` at the top — a missed blank will raise a clear error rather than a silent one. If you get stuck, the completed version is at [`session_07_answer.py`](session_07_answer.py).

Run from the repo root:

```
python exercises/session_07_exercise.py
```
