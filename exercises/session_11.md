# Session 11 Exercise — Calling the Education Data API

> Optional enrichment — complete during the session if time allows, or finish independently on your fork.

## Your Task

1. Create an `EducationDataAPI` instance
2. Call `ccd_directory` for the year `2018` with `fips='36,34'`
3. Print `result.count` — how many schools are returned?
4. Convert to a DataFrame with `.to_df()`
5. Print `.head()` and `.info()`
6. Print the list of column names

## Starter Script

Open [`session_11_exercise.py`](session_11_exercise.py) and fill in the blanks marked with `# TODO:`. Note: `fips` must be a comma-separated string (`'36,34'`), not a Python list. If you get stuck, the completed version is at [`session_11_answer.py`](session_11_answer.py).

Run from the repo root:

```
python exercises/session_11_exercise.py
```
