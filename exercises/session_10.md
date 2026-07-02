# Session 10 Exercise — Working with Database Results

> Optional enrichment — complete during the session if time allows, or finish independently on your fork.
>
> **GSU network required** (GSU WiFi on campus, or VPN if off campus).

## Your Task

1. Load `student_report/.env`
2. Connect to Oracle using `LightOracleConnection`
3. Query all rows from the `course` table
4. Normalize column names to lowercase
5. Filter to courses with `cost > 1000`
6. Save the filtered result to `exercises/data/courses_over_1000.csv` (no index)
7. Print how many courses remain after filtering

## Starter Script

Open [`session_10_exercise.py`](session_10_exercise.py) and fill in the blanks marked with `# TODO:`. If you get stuck, the completed version is at [`session_10_answer.py`](session_10_answer.py).

Run from the repo root:

```
python exercises/session_10_exercise.py
```
