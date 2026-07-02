# Session 5 Exercise — Merging Three Sources

> Optional enrichment — complete during the session if time allows, or finish independently on your fork.

## Your Task

1. Load `exercises/data/outreach_contacts.csv`
2. Load `exercises/data/school_survey_2019.csv`
3. Load `exercises/data/middle_schools_2019.csv`
4. Merge contacts with survey on `student_id` (left join) — keep only `student_id` and `ncessch` from the survey
5. Normalize `ncessch` to a clean string in both DataFrames
6. Merge the result with middle schools on `ncessch` (left join)
7. Print how many contacts have no school match (`school_name` is NaN)
8. Print the first and last names of those unmatched contacts
9. Save the merged result to `exercises/data/merged_contacts.csv` (no index)

## Starter Script

Open [`session_05_exercise.py`](session_05_exercise.py) and fill in the blanks marked with `# TODO:`. If you get stuck, the completed version is at [`session_05_answer.py`](session_05_answer.py).

Run from the repo root:

```
python exercises/session_05_exercise.py
```
