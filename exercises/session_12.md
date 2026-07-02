# Session 12 Exercise — Working with API Results

> Optional enrichment — complete during the session if time allows, or finish independently on your fork.

## Your Task

1. Create an `EducationDataAPI` instance and call `ccd_directory(2019, fips='36,34')`
2. Convert to a DataFrame with `.to_df()`
3. Select this subset of columns: `ncessch`, `school_name`, `city_location`, `state_location`, `school_level`, `enrollment`
4. Filter to middle schools only: rows where `school_level == 2`
5. Print how many middle schools remain
6. Save the filtered result to `exercises/data/middle_schools_2019_filtered.csv` (no index)

## Starter Script

Open [`session_12_exercise.py`](session_12_exercise.py) and fill in the blanks marked with `# TODO:`. If you get stuck, the completed version is at [`session_12_answer.py`](session_12_answer.py).

Run from the repo root:

```
python exercises/session_12_exercise.py
```
