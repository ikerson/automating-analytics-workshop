# Session 6 Exercise — Aggregations and Summary Statistics

> Optional enrichment — complete during the session if time allows, or finish independently on your fork.

## Your Task

1. Load `exercises/data/merged_contacts.csv` (produced in the Session 5 exercise)
2. Use `pd.cut()` on the `enrollment` column to create a `school_size` column
   - Bins: `[0, 300, 700, inf]`  Labels: `['Small (<300)', 'Medium (300-700)', 'Large (700+)']`
3. Print `value_counts()` on `city_location` — how many contacts attended schools in each city?
4. Use `groupby('school_size', observed=True)` and `.agg()` to compute student count and average enrollment per size bucket
5. Save the size summary to `exercises/data/size_summary.csv` (no index)

## Starter Script

Open [`session_06_exercise.py`](session_06_exercise.py) and fill in the blanks marked with `# TODO:`. If you get stuck, the completed version is at [`session_06_answer.py`](session_06_answer.py).

Run from the repo root:

```
python exercises/session_06_exercise.py
```
