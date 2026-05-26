# Session 8 — Merging the Three Sources

## Introduction

Sessions 4–7 built two data-retrieval modules: `db.py` returns the enrollment DataFrame from Oracle and `api.py` returns the CCD school directory from the Urban Institute API. The repo also includes `data/survey_middle_schools.csv`, which links each student to the NCES school ID of the middle school they attended. This session builds `transform.py` v1: two functions that connect all three sources into a single merged DataFrame — one row per student, enriched with their middle school's name, city, ZIP, and enrollment size.

Reference: Prior sessions — Sessions 5 and 7

---

## Setting Up

Open VS Code, activate your conda environment in the terminal, and create a new file at `student_report/transform.py`.

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

## The Three Sources

Before writing any code, it helps to know exactly what each dataset contributes and how they connect.

| Source | File | Join key |
|---|---|---|
| Enrollment | `student_report/reports/enrollment.csv` | `student_id` — matches survey |
| Survey | `student_report/data/survey_middle_schools.csv` | `student_id` (left) → `ncessch` (right) |
| CCD school directory | `student_report/reports/schools.csv` | `ncessch` — matches survey |

The survey CSV is the bridge: it holds each student's `student_id` and the `ncessch` (NCES school ID) of the middle school they attended. A student appears in the enrollment data even if they did not fill out the survey — in that case, no school information will be available and the merge will produce `NaN` values for all school columns.

---

## Building transform.py v1

### Starting the file

Create `student_report/transform.py` and add the import:

```python
import pandas as pd
```

That is the only import this module needs.

### get_students() — Deduplication

The enrollment DataFrame has one row per student × course enrollment. A student who took three courses appears three times. Before merging, we need exactly one row per student.

Add `get_students()`:

```python
def get_students(enrollment_df):
    return (
        enrollment_df[['student_id', 'first_name', 'last_name', 'zip', 'city', 'state']]
        .drop_duplicates(subset=['student_id'])
        .copy()
    )
```

Three things happen here:

1. **Column selection** — `enrollment_df[['student_id', ...]]` keeps only the six columns the pipeline needs, dropping `course_name`, `cost`, `enroll_date`, and `final_grade`. Those are per-enrollment details, not per-student details.
2. **Deduplication** — `.drop_duplicates(subset=['student_id'])` keeps the first row for each `student_id` and discards the rest. The six columns are all student-level data (the same value on every row for a given student), so it does not matter which enrollment row is kept.
3. **Copy** — `.copy()` returns an independent DataFrame so that later operations do not silently modify the original.

### Normalizing the join keys

Before merging, the join key columns need to be in a consistent format. Two problems come from the API data in `schools.csv`:

- `ncessch` was returned as a float: `360007702472.0`. The survey CSV stores it without the decimal: `360007702472`. These will not match unless we normalize both sides.
- `zip_mailing` was returned as a float: `10001.0`. ZIP codes are five-digit strings and need zero-padding for short codes.

The enrollment `zip` column comes from Oracle as a string but may also need zero-padding.

The normalization pattern for a float-to-clean-string conversion is:

```python
column.astype(str).str.split('.').str[0]
```

- `.astype(str)` converts `360007702472.0` → `'360007702472.0'`
- `.str.split('.')` splits on the decimal point → `['360007702472', '0']`
- `.str[0]` takes the first part → `'360007702472'`

For ZIP codes, append `.str.zfill(5)` to pad short codes with leading zeros: `'7102'` → `'07102'`.

### merge_data() — The three-way merge

Add `merge_data()` below `get_students()`:

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

    return merged
```

Walk through each section:

**Defensive copies** — The three `.copy()` calls at the top prevent the normalization steps from modifying the DataFrames that were passed in. This makes the function safe to call multiple times or from a test.

**Normalization** — The four assignment lines normalize the join key columns as described above. The normalization happens before the merge so both sides have matching formats.

**First merge — students → survey** — `students_df.merge(survey_df, on='student_id', how='left')` joins on `student_id`. `how='left'` keeps every row from `students_df`. Students who have a survey response get `middle_school_name` and `ncessch` from the survey. Students with no survey response get `NaN` in those columns.

**Second merge — result → CCD** — `merged.merge(school_df, on='ncessch', how='left')` joins the result of the first merge to the CCD school directory on `ncessch`. Students who matched the survey and whose `ncessch` exists in the CCD data get all the school columns (`school_name`, `city_location`, `zip_mailing`, `enrollment`, etc.). Students with no survey match — and therefore no `ncessch` — still get `NaN` for all school columns.

The final result is one row per student, with school data where available.

### Testing with a __main__ block

Add a `if __name__ == '__main__':` block to load the CSV files from prior sessions and test the two functions:

```python
if __name__ == '__main__':
    enrollment_df = pd.read_csv('student_report/reports/enrollment.csv')
    survey_df = pd.read_csv('student_report/data/survey_middle_schools.csv')
    school_df = pd.read_csv('student_report/reports/schools.csv')

    students = get_students(enrollment_df)
    print(f"Students (deduplicated): {len(students)}")

    merged = merge_data(students, survey_df, school_df)
    print(f"Merged rows: {len(merged)}")
    print(merged.head())
    print()
    merged.info()
```

Run from the repo root:

```bash
python student_report/transform.py
```

You should see the deduplicated student count followed by the merged row count — both numbers should be equal (one row per student). The `.info()` output will show `NaN` counts for the school columns, indicating students with no survey match.

### Inspecting unmatched rows

Add a few lines to the `__main__` block to look at students without a survey match:

```python
if __name__ == '__main__':
    enrollment_df = pd.read_csv('student_report/reports/enrollment.csv')
    survey_df = pd.read_csv('student_report/data/survey_middle_schools.csv')
    school_df = pd.read_csv('student_report/reports/schools.csv')

    students = get_students(enrollment_df)
    print(f"Students (deduplicated): {len(students)}")

    merged = merge_data(students, survey_df, school_df)
    print(f"Merged rows: {len(merged)}")
    print(merged.head())
    print()
    merged.info()
    print()

    unmatched = merged[merged['middle_school_name'].isna()]
    print(f"Students without a survey match: {len(unmatched)}")
    print(unmatched[['student_id', 'first_name', 'last_name', 'city', 'state']].head())
```

`merged['middle_school_name'].isna()` is `True` for every row where the survey join found no match. These are students who either did not complete the survey or whose record was not in the survey data. The count and a sample of names give a sense of how much school data is missing before the report is produced.

### Saving the merged result to CSV

Add a `to_csv()` call to write the merged DataFrame to a file:

```python
if __name__ == '__main__':
    enrollment_df = pd.read_csv('student_report/reports/enrollment.csv')
    survey_df = pd.read_csv('student_report/data/survey_middle_schools.csv')
    school_df = pd.read_csv('student_report/reports/schools.csv')

    students = get_students(enrollment_df)
    merged = merge_data(students, survey_df, school_df)

    print(f"Students: {len(students)}")
    print(f"Merged rows: {len(merged)}")

    unmatched = merged[merged['middle_school_name'].isna()]
    print(f"Students without a survey match: {len(unmatched)}")

    merged.to_csv('student_report/reports/merged.csv', index=False)
    print("Saved merged.csv")
```

Run again and open `student_report/reports/merged.csv`. Each row is one student. The school columns are populated where a survey match and a CCD match both exist, and `NaN` otherwise.

---

## transform.py v1 — Complete File

Remove the `if __name__ == '__main__':` block. The final `transform.py` v1 defines one import and two functions:

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

    return merged
```

`main.py` (Session 12) will call these functions by importing `transform.py`. There is no top-level code after the import, so the import is safe — no file I/O or computation happens until the functions are explicitly called.

In Session 9, we add three aggregation functions to `transform.py`: summaries by school, by ZIP, and by school size — plus `pd.cut()` to bucket school enrollment into Small / Medium / Large.

---

## Practice Exercise

> Optional enrichment — complete during the session if time allows, or finish independently on your fork.

### Your Task

Merge three outreach data files to build a contact list enriched with school information.

1. Load `exercises/data/outreach_contacts.csv` (25 contacts, student IDs 101–125)
2. Load `exercises/data/school_survey_2019.csv` (school name and NCES ID for student IDs 101–120)
3. Load `exercises/data/middle_schools_2019.csv` (NJ and NY middle school directory with enrollment and city)
4. Merge contacts with survey on `student_id` (left join) — this adds `ncessch` to each matched contact
5. Normalize `ncessch` in both DataFrames: `.astype(str).str.split('.').str[0]`
6. Merge the result with middle_schools on `ncessch` (left join) — this adds enrollment, city, and other school columns
7. Print how many contacts have no school match (i.e., `school_name` is `NaN`)
8. Print the `student_id`, first name, and last name of those unmatched contacts
9. Save the merged result to `exercises/data/merged_contacts.csv` (no index)

Run from the repo root:

```
python exercises/session_08_exercise.py
```

## Additional Resources

- [pandas — DataFrame.merge](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html)
- [pandas — DataFrame.drop_duplicates](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html)
- [pandas — Working with missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html)
- [pandas — String methods (.str accessor)](https://pandas.pydata.org/docs/user_guide/text.html)
