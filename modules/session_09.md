# Session 9 — Aggregations and Summary Statistics

## Introduction

Session 8 produced a merged DataFrame: one row per student, enriched with their middle school's name, city, ZIP, and enrollment figure where a survey match existed. The data is now ready to summarize. This session builds `transform.py` v2: four additions — an enrollment size bucket column added to `merge_data()`, and three new functions that compute the summaries the report needs. At the end of this session, `transform.py` is complete.

Reference: Prior session — Session 8

---

## Setting Up

Open VS Code, activate your conda environment in the terminal, and open `student_report/transform.py`.

**Windows (CMD or Git Bash):**

```
conda activate student-report
```

**Mac:**

```
conda activate student-report
```

Confirm `(student-report)` appears in your terminal prompt before continuing.

> **This session does not require VPN or an API call.** The `__main__` block loads from the CSV files you saved in Sessions 5 and 7. Make sure `student_report/reports/enrollment.csv` and `student_report/reports/schools.csv` exist before running `transform.py`.

---

## Building transform.py v2

### Bucketing school enrollment with pd.cut()

The merged DataFrame has an `enrollment` column — the total number of students at each middle school. Raw enrollment figures are useful for sorting, but the report needs to group schools into three readable categories: Small, Medium, and Large. `pd.cut()` does this: it takes a continuous numeric column and divides it into labeled bins.

Update `merge_data()` to add the `school_size` assignment before the `return` statement:

```python
def merge_data(students_df, survey_df, school_df):
    students_df = students_df.copy()
    survey_df = survey_df.copy()
    school_df = school_df.copy()

    students_df['zip'] = students_df['zip'].astype(str).str.zfill(5)
    school_df['zip_mailing'] = (
        school_df['zip_mailing'].astype(str).str.split('.').str[0].str.zfill(5)
    )
    survey_df['ncessch'] = survey_df['ncessch'].astype(str).str.split('.').str[0]
    school_df['ncessch'] = school_df['ncessch'].astype(str).str.split('.').str[0]

    merged = students_df.merge(survey_df, on='student_id', how='left')
    merged = merged.merge(school_df, on='ncessch', how='left')

    merged['school_size'] = pd.cut(
        merged['enrollment'],
        bins=[0, 300, 700, float('inf')],
        labels=['Small (<300)', 'Medium (300-700)', 'Large (700+)'],
    )

    return merged
```

Walk through the `pd.cut()` call:

- **`merged['enrollment']`** — the input series. Students with no survey match have `NaN` enrollment; `pd.cut()` leaves those rows as `NaN` in the output column.
- **`bins=[0, 300, 700, float('inf')]`** — three intervals: (0, 300], (300, 700], (700, ∞). Each value in the list is the right edge of the bin it closes.
- **`labels=['Small (<300)', 'Medium (300-700)', 'Large (700+)']`** — one label per bin. The result is a pandas `Categorical` column — a dtype that stores a fixed, ordered set of possible values rather than arbitrary strings.

The new `school_size` column travels with the DataFrame into the summarize functions below.

### summarize_top_schools()

Add `summarize_top_schools()` below `merge_data()`:

```python
def summarize_top_schools(merged_df):
    matched = merged_df.dropna(subset=['middle_school_name'])
    return (
        matched.groupby(['middle_school_name', 'city_location', 'zip_mailing', 'school_size'])
        .agg(student_count=('student_id', 'count'), school_enrollment=('enrollment', 'first'))
        .reset_index()
        .sort_values('student_count', ascending=False)
        .head(10)
    )
```

Walk through each step:

**`.dropna(subset=['middle_school_name'])`** — students with no survey match have `NaN` for `middle_school_name`. Dropping them before grouping prevents a `NaN` group from appearing in the result.

**`.groupby([...])`** — groups by four columns that together identify a school. Including `city_location`, `zip_mailing`, and `school_size` in the groupby key carries them into the result without a separate join — every student at the same school has the same values for those columns, so grouping on them is safe and keeps the result readable.

**`.agg(student_count=..., school_enrollment=...)`** — named aggregation syntax: each keyword argument becomes a column name in the result. `('student_id', 'count')` counts the rows in the group; `('enrollment', 'first')` retrieves the enrollment figure — the same on every row in the group, so `'first'` is sufficient.

**`.reset_index()`** — after a groupby, the group keys become the index. `.reset_index()` promotes them back to regular columns so the result is a flat DataFrame.

**`.sort_values('student_count', ascending=False).head(10)`** — sort from largest to smallest and keep the top 10.

### summarize_by_zip()

Add `summarize_by_zip()` below `summarize_top_schools()`:

```python
def summarize_by_zip(merged_df):
    matched = merged_df.dropna(subset=['zip_mailing'])
    return (
        matched.groupby(['zip_mailing', 'city_location'])
        .agg(student_count=('student_id', 'count'))
        .reset_index()
        .sort_values('student_count', ascending=False)
    )
```

This follows the same pattern as `summarize_top_schools()` but groups by ZIP code and city instead of school name. The result answers a geographic question: which ZIP codes do the most students come from?

`zip_mailing` is the school's mailing ZIP — it identifies the neighborhood where the middle school sits, which is the relevant geography for outreach targeting.

### summarize_by_size()

Add `summarize_by_size()` below `summarize_by_zip()`:

```python
def summarize_by_size(merged_df):
    return (
        merged_df.groupby('school_size', observed=True)
        .agg(student_count=('student_id', 'count'))
        .reset_index()
    )
```

**`observed=True`** is required when grouping by a `Categorical` column — which is what `pd.cut()` produces. Without it, pandas includes a row for every possible category label even if no students belong to it, and raises a `FutureWarning` in pandas versions before 2.0. `observed=True` tells pandas to include only categories that actually appear in the data.

This function does not call `.dropna()` before grouping. Students with `NaN` enrollment have `NaN` school_size and are automatically excluded from all bins — no extra filtering is needed.

### Testing with a __main__ block

Add a `if __name__ == '__main__':` block to run all five functions and inspect the results:

```python
if __name__ == '__main__':
    enrollment_df = pd.read_csv('student_report/reports/enrollment.csv')
    survey_df = pd.read_csv('student_report/data/survey_middle_schools.csv')
    school_df = pd.read_csv('student_report/reports/schools.csv')

    students = get_students(enrollment_df)
    merged = merge_data(students, survey_df, school_df)

    top_schools = summarize_top_schools(merged)
    print("Top 10 schools:")
    print(top_schools)
    print()

    zip_summary = summarize_by_zip(merged)
    print("By ZIP:")
    print(zip_summary.head())
    print()

    size_summary = summarize_by_size(merged)
    print("By school size:")
    print(size_summary)
```

Run from the repo root:

```bash
python student_report/transform.py
```

The top schools table shows the 10 middle schools with the highest student counts, ranked largest first. The size summary should show three rows — one per bucket — with no empty categories. If a `FutureWarning` appears, verify that `observed=True` is present in `summarize_by_size()`.

---

## transform.py v2 — Complete File

Remove the `if __name__ == '__main__':` block. The final `transform.py` defines one import and five functions:

```python
import pandas as pd


def get_students(enrollment_df):
    return (
        enrollment_df[['student_id', 'first_name', 'last_name', 'zip', 'city', 'state']]
        .drop_duplicates(subset=['student_id'])
        .copy()
    )


def merge_data(students_df, survey_df, school_df):
    students_df = students_df.copy()
    survey_df = survey_df.copy()
    school_df = school_df.copy()

    students_df['zip'] = students_df['zip'].astype(str).str.zfill(5)
    school_df['zip_mailing'] = (
        school_df['zip_mailing'].astype(str).str.split('.').str[0].str.zfill(5)
    )
    survey_df['ncessch'] = survey_df['ncessch'].astype(str).str.split('.').str[0]
    school_df['ncessch'] = school_df['ncessch'].astype(str).str.split('.').str[0]

    merged = students_df.merge(survey_df, on='student_id', how='left')
    merged = merged.merge(school_df, on='ncessch', how='left')

    merged['school_size'] = pd.cut(
        merged['enrollment'],
        bins=[0, 300, 700, float('inf')],
        labels=['Small (<300)', 'Medium (300-700)', 'Large (700+)'],
    )

    return merged


def summarize_top_schools(merged_df):
    matched = merged_df.dropna(subset=['middle_school_name'])
    return (
        matched.groupby(['middle_school_name', 'city_location', 'zip_mailing', 'school_size'])
        .agg(student_count=('student_id', 'count'), school_enrollment=('enrollment', 'first'))
        .reset_index()
        .sort_values('student_count', ascending=False)
        .head(10)
    )


def summarize_by_zip(merged_df):
    matched = merged_df.dropna(subset=['zip_mailing'])
    return (
        matched.groupby(['zip_mailing', 'city_location'])
        .agg(student_count=('student_id', 'count'))
        .reset_index()
        .sort_values('student_count', ascending=False)
    )


def summarize_by_size(merged_df):
    return (
        merged_df.groupby('school_size', observed=True)
        .agg(student_count=('student_id', 'count'))
        .reset_index()
    )
```

`transform.py` is now complete. `main.py` (Session 12) will call all five functions by importing this module. There is no top-level code after the import, so the import is safe — no file I/O or computation happens until the functions are explicitly called.

In Session 10, we build `report.py` v1: the two chart functions that visualize the top schools and size distribution summaries.

---

## Practice Exercise

> Optional enrichment — complete during the session if time allows, or finish independently on your fork.

### Your Task

Summarize the merged contacts file from Session 8 by school size and city.

1. Load `exercises/data/merged_contacts.csv` (produced in the Session 8 exercise)
2. Use `pd.cut()` on the `enrollment` column to create a `school_size` column — use the same bins and labels as the pipeline: `[0, 300, 700, float('inf')]` and `['Small (<300)', 'Medium (300-700)', 'Large (700+)']`
3. Print `value_counts()` on `city_location` — how many contacts attended schools in each city?
4. Use `groupby('school_size', observed=True)` and `.agg()` to compute student count and average enrollment per size bucket
5. Save the size summary to `exercises/data/size_summary.csv` (no index)

Run from the repo root:

```
python exercises/session_09_exercise.py
```

### Answer

The complete working solution is at the bottom of `exercises/session_09_exercise.py`, commented out. Uncomment it to check your work.

---

## Additional Resources

- [pandas — pd.cut](https://pandas.pydata.org/docs/reference/api/pandas.cut.html)
- [pandas — DataFrame.groupby](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html)
- [pandas — GroupBy.agg](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.aggregate.html)
- [pandas — Series.value_counts](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
- [pandas — Categorical data](https://pandas.pydata.org/docs/user_guide/categorical.html)
