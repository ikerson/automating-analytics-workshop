# Session 3 — Pandas and Working with Data

## Introduction

Every session from here on involves loading, inspecting, and transforming data. This session introduces pandas — the Python library that makes all of that possible — using the survey CSV that sits at the heart of the workshop pipeline. You will learn the four operations you will use in every session that follows: loading a file, inspecting what is in it, selecting columns, and filtering rows. You will also write your first reusable function.

Reference: Prior session — Session 2

---

## Setting Up

Open VS Code, activate your conda environment in the terminal, and open or clear `scratch.py` in the repo root. You will build the code-along script in that file, running it after each addition.

In Git Bash:

```
conda activate student-report
```

Confirm `(student-report)` appears in your terminal prompt before continuing.

---

## What Is pandas?

pandas is a Python library for working with tabular data. When you load a CSV, pandas gives you a **DataFrame** — a table with named columns and numbered rows, similar to an Excel worksheet.

A single column of a DataFrame is called a **Series** — a list of values with an index. You will mostly work with DataFrames, but understanding the distinction matters because many operations return a Series and some expect one.

```
DataFrame                        Series (one column)
┌─────────────┬──────────────┐   ┌──────────────┐
│ student_id  │ school_name  │   │ school_name  │
├─────────────┼──────────────┤   ├──────────────┤
│ 124         │ Bloomfield   │   │ Bloomfield   │
│ 353         │ Bloomfield   │   │ Bloomfield   │
│ 157         │ Carteret     │   │ Carteret     │
└─────────────┴──────────────┘   └──────────────┘
```

---

## Loading a CSV

Add this to `scratch.py` and run it:

```python
import pandas as pd

df = pd.read_csv('student_report/data/survey_middle_schools.csv')
print(df)
```

Run from the repo root:

```
python scratch.py
```

You should see a table with three columns — `student_id`, `middle_school_name`, and `ncessch` — and several rows.

> **Always run scripts from the repo root.** If you run from a different directory, relative file paths like `student_report/data/...` will not resolve.

### Controlling column data types

By default, pandas infers each column's type from its values. Run `.info()` to see what it chose:

```python
print(df.info())
```

Notice that `ncessch` is loaded as `int64` — a number. That looks fine until you compare it to another dataset where the same ID is stored as a string like `"340183001982"`. Type mismatches silently produce empty merges.

Fix this at load time by specifying `dtype`:

```python
df = pd.read_csv(
    'student_report/data/survey_middle_schools.csv',
    dtype={'ncessch': str}
)
```

Run `.info()` again — `ncessch` is now `object` (pandas' label for strings). This is exactly how `main.py` loads this file. Any time you load a file with an ID column that is all digits, force it to string.

---

## Inspecting a Dataset

Three methods give you a quick picture of any DataFrame.

### `.head()`

Returns the first 5 rows (or however many you pass):

```python
print(df.head())
print(df.head(10))
```

Use this first every time you load a new file.

### `.info()`

Prints column names, non-null counts, and data types:

```python
df.info()
```

The non-null count is important: if a column has fewer non-null values than total rows, some values are missing (`NaN`). You will deal with missing data in the merge step.

### `.describe()`

Computes summary statistics for numeric columns:

```python
print(df.describe())
```

For this dataset, only `student_id` is numeric, so you will see its count, mean, min, and max. On richer datasets, `.describe()` immediately shows whether values are in a plausible range.

---

## Selecting Columns

Select one column using bracket notation — this returns a **Series**:

```python
print(df['middle_school_name'])
```

Select multiple columns by passing a list — this returns a **DataFrame**:

```python
print(df[['student_id', 'middle_school_name']])
```

Note the double brackets: the outer `[ ]` is the selection operator; the inner `[ ]` is a Python list of column names.

You can assign the result to a new variable:

```python
names_only = df[['student_id', 'middle_school_name']]
print(names_only.head())
```

Column selection is how every module in this pipeline trims down a wide DataFrame to only the columns it actually needs. In `transform.py`, `get_students()` selects six columns from the full Oracle enrollment result before doing anything else with the data.

---

## Filtering Rows

Filter rows by writing a condition inside `[ ]`. The condition must compare a column to a value and return `True` or `False` for each row.

```python
target_school = df[df['middle_school_name'] == 'Bloomfield Middle School']
print(target_school)
```

pandas evaluates `df['middle_school_name'] == 'Bloomfield Middle School'` row by row, producing a column of `True`/`False` values called a **boolean mask**. Placing that mask inside `df[ ]` keeps only the rows where the condition is `True`.

Combine conditions with `&` (and) or `|` (or). Wrap each condition in parentheses:

```python
nj_schools = df[
    (df['middle_school_name'] == 'Bloomfield Middle School') |
    (df['middle_school_name'] == 'Carteret Middle School')
]
print(nj_schools)
```

---

## Writing a Function

So far, every operation has been written as a standalone line. When you need to repeat the same steps — or when a block of code has a clear single purpose — wrap it in a function.

Here is a function that takes the survey DataFrame and returns a count of students per school, sorted from most to least:

```python
def count_by_school(df):
    counts = df.groupby('middle_school_name').size().reset_index(name='student_count')
    return counts.sort_values('student_count', ascending=False)
```

Add this to `scratch.py` and call it:

```python
result = count_by_school(df)
print(result.head(10))
```

This is a simplified preview of `summarize_top_schools()` in `transform.py`, which you will build in Session 9. The structure is the same: a function accepts a DataFrame, performs a transformation, and returns a new DataFrame.

### Why functions?

- **Reuse.** Call `count_by_school(df)` anywhere instead of rewriting four lines every time.
- **Naming.** `count_by_school(df)` says exactly what it does. Four anonymous lines do not.
- **Testability.** In Session 13, you will write unit tests that call functions directly and check their output.

A good rule of thumb: if a block of code has a name you can give it in plain English, it belongs in a function.

---

## The Other Two Sources

The pipeline uses three CSV files in total. You just explored the survey CSV. The other two are also in `student_report/data/`.

### enrollment.csv

```python
enrollment_df = pd.read_csv('student_report/data/enrollment.csv')
print(enrollment_df.head())
enrollment_df.info()
```

A few things to notice:
- Column names are lowercase — a normalization step that `db.py` applies when it queries Oracle.
- There are more rows than students. A student enrolled in three courses appears three times — one row per enrollment. Session 4 will deduplicate this to one row per student before merging.
- `student_id` is the key that links this file to the survey.

This file was exported from the Oracle training database. In Sessions 8–9 you will write the Python code that generates it automatically.

### schools.csv

```python
school_df = pd.read_csv('student_report/data/schools.csv')
print(school_df.head())
school_df.info()
```

A few things to notice:
- `ncessch` and `zip_mailing` appear as floats — `360007702472.0`, `10001.0`. These are IDs that should be strings. This is a quirk of how the Urban Institute API returns them; `transform.py` normalizes them in Session 4 before merging.
- `school_level` encodes the school type: `2.0` means middle school.
- There are thousands of rows — every NY and NJ school in the 2019 CCD directory.

This file was downloaded from the Urban Institute Education Data Portal. In Sessions 10–11 you will write the Python code that generates it automatically.

### Why these files are here

In Phase 1, `enrollment.csv` and `schools.csv` represent data that someone on your team collected by hand before the workshop — the same steps in the old workflow that together took 30–50 minutes. You will work with them directly. Phase 2 (Sessions 8–11) builds the automation that eliminates those manual steps entirely.

---

## Practice Exercise

> Optional enrichment — complete during the session if time allows, or finish independently on your fork.

The starter script is at `exercises/session_03_exercise.py`. It contains instructions and fill-in-the-blank placeholders. If you get stuck, the completed version is at `exercises/session_03_answer.py`.

Run from the repo root:

```
python exercises/session_03_exercise.py
```

## Additional Resources

- [pandas documentation](https://pandas.pydata.org/docs/)
- [pandas cheat sheet (DataCamp)](https://www.datacamp.com/cheat-sheet/pandas-cheat-sheet-for-data-science-in-python)
- [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
