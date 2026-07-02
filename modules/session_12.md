# Session 12 — Working with API Results

## Introduction

Session 11 called the CCD school directory API and confirmed the data is accessible. The result DataFrame has over 50 columns — far more than the pipeline needs. This session builds `api.py` v2: we define the 9 columns the pipeline uses, wrap the API call in a function, and verify the result. The pattern mirrors what we did in Session 10 for `db.py`: exploration code becomes a clean, importable module.

## Setting Up

Open VS Code, activate your conda environment in the terminal, and open `student_report/api.py`. This is the exploration file you built in Session 11.

In Git Bash:

```zsh
conda activate student-report
```

Confirm `(student-report)` appears in your terminal prompt before continuing.

Your current `api.py` should look like this:

```python
from educationdata import EducationDataAPI

api = EducationDataAPI()
result = api.ccd_directory(2019, fips='36,34')
print(result.count)

df = result.to_df()
print(df.head())
print()
df.info()
print()
print(df.describe())
print()
print(df.columns.tolist())
```

Today we replace this with a function that returns only the columns the pipeline needs.

## Building api.py v2

### Clearing the exploration code and defining the column list

Delete everything below the import. Then add a `CCD_COLUMNS` list that names the 9 columns the pipeline uses:

```python
from educationdata import EducationDataAPI

CCD_COLUMNS = [
    'ncessch',
    'school_name',
    'zip_mailing',
    'city_location',
    'state_location',
    'school_level',
    'enrollment',
    'lowest_grade_offered',
    'highest_grade_offered',
]
```

Storing the column list as a named constant serves two purposes: the function below stays short and readable, and any future change to the columns — adding one, removing one — happens in one place.

### Writing the function

Add `get_school_data()` below the constant:

```python
def get_school_data(year):
    api = EducationDataAPI()
    result = api.ccd_directory(year, fips='36,34')
    df = result.to_df()
    return df[CCD_COLUMNS].copy()
```

`df[CCD_COLUMNS]` selects only the 9 columns in the list. `.copy()` returns an independent DataFrame so that later operations on the result do not inadvertently modify the original API data.

The `year` parameter makes the function reusable — `get_school_data(2018)` returns 2018 data without changing anything else. The `fips='36,34'` is hardcoded because the pipeline always targets New York and New Jersey.

### Running the function

Add a `if __name__ == '__main__':` block to test the function without making `api.py` run on every import:

```python
if __name__ == '__main__':
    df = get_school_data(2019)
    print(df.shape)
    print(df.head())
    print()
    df.info()
```

Run from the repo root:

```bash
python student_report/api.py
```

After a short pause for pagination, you should see a row and column count followed by the first five rows. The DataFrame now has exactly 9 columns — a manageable size.

### Exploring the result

Add a few more lines to the `__main__` block to understand the data:

```python
if __name__ == '__main__':
    df = get_school_data(2019)
    print(df.shape)
    print(df.head())
    print()
    df.info()
    print()
    print(df['school_level'].value_counts())
```

`school_level` encodes the type of school: `1` = elementary, `2` = middle, `3` = high school, `4` = other. The value counts show how many schools of each type are in the NY and NJ results. Our students attended middle schools, so most join keys will match rows where `school_level == 2` — but we keep all rows in `api.py` and let `transform.py` handle the join logic.

Also note that `ncessch` and `zip_mailing` appear as floats — `360007702472.0`, `10001.0`. These are IDs that should be strings. `transform.py` (Session 5) normalizes them before merging.

### Saving to CSV

Add a `to_csv()` call to write the selected columns to a file:

```python
if __name__ == '__main__':
    df = get_school_data(2019)
    print(df.shape)
    print(df.head())
    print()
    df.info()
    print()
    print(df['school_level'].value_counts())
    df.to_csv('student_report/reports/schools.csv', index=False)
    print("Saved schools.csv")
```

Run again and open `student_report/reports/schools.csv`. Verify that only the 9 columns appear and that the float IDs are present. Session 5 will handle normalizing them.

## What Changes if the API Is Different?

The pipeline uses the `ccd_directory` endpoint for 2019. Swapping years is a one-character change — pass a different `year` to `get_school_data()`. The column list stays valid as long as the endpoint schema does not change across years.

If a column is ever renamed or removed by the API, `df[CCD_COLUMNS]` will raise a `KeyError`. That error is the right behavior — a silent mismatch would be worse. When that happens, run `df.columns.tolist()` to inspect what the API currently returns and update `CCD_COLUMNS` accordingly.

## api.py v2 — Complete File

Remove the `if __name__ == '__main__':` block. The final `api.py` defines one constant and one function:

```python
from educationdata import EducationDataAPI

CCD_COLUMNS = [
    'ncessch',
    'school_name',
    'zip_mailing',
    'city_location',
    'state_location',
    'school_level',
    'enrollment',
    'lowest_grade_offered',
    'highest_grade_offered',
]


def get_school_data(year):
    api = EducationDataAPI()
    result = api.ccd_directory(year, fips='36,34')
    df = result.to_df()
    return df[CCD_COLUMNS].copy()
```

`main.py` (Session 13) will call `get_school_data(year)` by importing `api.py`. There is no top-level code after the import, so the import is safe — no API call happens until `get_school_data()` is explicitly called.

> **Note:** `student_report/data/schools.csv` is a pre-committed static file generated from this function. Once `api.py` is wired into `main.py` in Session 13, every pipeline run regenerates it automatically — the static file is no longer needed for day-to-day use.

In Session 13, `main.py` wires all four modules together. `db.py` and `api.py` replace the static files in `student_report/data/` and the pipeline runs end-to-end from a single command.

## Practice Exercise

> Optional enrichment — complete during the session if time allows, or finish independently on your fork.

The starter script is at [`exercises/session_12_exercise.py`](../exercises/session_12_exercise.py). It contains instructions and fill-in-the-blank placeholders. If you get stuck, the completed version is at [`exercises/session_12_answer.py`](../exercises/session_12_answer.py).

Run from the repo root:

```
python exercises/session_12_exercise.py
```

## Additional Resources

- [EducationDataAPI — GSU-Analytics/EducationDataAPI](https://github.com/GSU-Analytics/EducationDataAPI)
- [pandas — DataFrame column selection](https://pandas.pydata.org/docs/user_guide/indexing.html)
- [pandas — DataFrame.to_csv](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html)
