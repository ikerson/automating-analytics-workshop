# Session 9 — Working with Database Results

## Introduction

Session 8 confirmed the Oracle connection works and ran a single-table query. This session builds `db.py` v2: we replace the top-level exploration code with a five-table enrollment JOIN wrapped in a reusable function, and normalize the column names so the rest of the pipeline can use them consistently. The finished `db.py` is a module — it defines a function rather than running code at the top level — so it can be safely imported in later sessions without triggering a database query.

> **GSU network required.** The Oracle server is only reachable on the GSU network. On campus, GSU WiFi is sufficient. If you are working off campus, connect to the GSU VPN before starting the code-along and before running the practice exercise.

## Setting Up

Open VS Code, activate your conda environment in the terminal, and open `student_report/db.py`. This is the file you built in Session 8.

In Git Bash:

```zsh
conda activate student-report
```

Confirm `(student-report)` appears in your terminal prompt before continuing.

Your current `db.py` should look like this:

```python
from pathlib import Path
from dotenv import load_dotenv
from lightoracle import LightOracleConnection

load_dotenv(Path(__file__).parent / ".env")

conn = LightOracleConnection()
conn.test_connection()

df = conn.execute_query("SELECT * FROM student FETCH FIRST 5 ROWS ONLY")
print(df)
print(df.info())
```

The lines after `load_dotenv(...)` are top-level statements — they run every time this file is imported by another script, not just when you run it directly. That was fine for exploring the connection in Session 8. Today we restructure `db.py` so it defines a function instead of running code, and replace the single-table query with the full enrollment data we actually need.

## The Enrollment Query

The workshop pipeline needs data from five tables in the Oracle database:

| Table | What it contributes |
|---|---|
| `student` | Name, student ID, ZIP code |
| `zipcode` | City and state for each ZIP |
| `enrollment` | Which student is enrolled in which section |
| `section` | Which course each section belongs to |
| `course` | Course name and cost |

Joining all five tables produces one row for every course a student has enrolled in. A student enrolled in three courses appears three times. `transform.py` (Session 4) will deduplicate this down to one row per student before merging.

The complete SQL:

```sql
SELECT
    s.STUDENT_ID,
    s.FIRST_NAME,
    s.LAST_NAME,
    s.ZIP,
    z.CITY,
    z.STATE,
    c.DESCRIPTION  AS COURSE_NAME,
    c.COST,
    e.ENROLL_DATE,
    e.FINAL_GRADE
FROM student s
JOIN zipcode    z ON s.ZIP        = z.ZIP
JOIN enrollment e ON s.STUDENT_ID = e.STUDENT_ID
JOIN section  sec ON e.SECTION_ID = sec.SECTION_ID
JOIN course     c ON sec.COURSE_NO = c.COURSE_NO
```

This is the query the pipeline uses. Each alias (`s`, `z`, `e`, `sec`, `c`) is shorthand for the table name — `s.STUDENT_ID` means the `STUDENT_ID` column from the `student` table. The `JOIN ... ON` clauses link each pair of tables on their shared key column.

## Building db.py v2

### Clearing the exploration code

Open `student_report/db.py`. Delete everything below the `load_dotenv(...)` line — the `conn`, `conn.test_connection()`, `df`, and `print()` lines. Leave the imports and `load_dotenv(...)` in place.

Your file should now be:

```python
from pathlib import Path
from dotenv import load_dotenv
from lightoracle import LightOracleConnection

load_dotenv(Path(__file__).parent / ".env")
```

### Defining the query as a constant

Add the enrollment query as a module-level string constant named `ENROLLMENT_QUERY`:

```python
from pathlib import Path
from dotenv import load_dotenv
from lightoracle import LightOracleConnection

load_dotenv(Path(__file__).parent / ".env")

ENROLLMENT_QUERY = """
    SELECT
        s.STUDENT_ID,
        s.FIRST_NAME,
        s.LAST_NAME,
        s.ZIP,
        z.CITY,
        z.STATE,
        c.DESCRIPTION  AS COURSE_NAME,
        c.COST,
        e.ENROLL_DATE,
        e.FINAL_GRADE
    FROM student s
    JOIN zipcode    z ON s.ZIP        = z.ZIP
    JOIN enrollment e ON s.STUDENT_ID = e.STUDENT_ID
    JOIN section  sec ON e.SECTION_ID = sec.SECTION_ID
    JOIN course     c ON sec.COURSE_NO = c.COURSE_NO
"""
```

Storing the SQL as a named constant keeps the function short and makes the query easy to find and edit without touching any Python logic. The triple-quoted string `""" ... """` lets the SQL span multiple lines.

### Writing the function

Now add `get_enrollment()` below the constant:

```python
def get_enrollment():
    conn = LightOracleConnection()
    df = conn.execute_query(ENROLLMENT_QUERY)
    df.columns = df.columns.str.lower()
    return df
```

Three things happen inside this function:

1. A new connection opens — it reads `ORACLE_USER`, `ORACLE_PASSWORD`, and `ORACLE_DSN` from the environment that `load_dotenv(...)` set up at the top of the file
2. The query runs and returns a DataFrame
3. `df.columns.str.lower()` normalizes all column names to lowercase

Oracle returns column names in uppercase (`STUDENT_ID`, `FIRST_NAME`, ...). Lowercase names are easier to type and match the convention used by the rest of the pipeline. After this line, every column is `student_id`, `first_name`, and so on.

### Running the function

To test `get_enrollment()` without making `db.py` run code on every import, add a `if __name__ == '__main__':` block at the bottom:

```python
if __name__ == '__main__':
    df = get_enrollment()
    print(df.head())
    print()
    df.info()
```

`if __name__ == '__main__':` is a Python convention: the indented block only executes when you run the file directly (`python student_report/db.py`). When another script imports `db.py`, the block is skipped entirely. This is the standard way to make a file both runnable for testing and safe to import.

Run it:

```bash
python student_report/db.py
```

You should see the first five rows of the enrollment result followed by a column summary. The column names will be lowercase. If you see a student ID repeated across rows, that is correct — each row is one enrollment, and students enrolled in multiple courses appear multiple times.

### Exploring the result

Add `.describe()` to the `__main__` block and re-run:

```python
if __name__ == '__main__':
    df = get_enrollment()
    print(df.head())
    print()
    df.info()
    print()
    print(df.describe())
```

`.describe()` reports summary statistics for numeric columns. Look at `student_id`, `cost`, and `final_grade`. Note the row count in `.info()` — it is larger than the number of students because each enrollment is its own row. Session 4 will deduplicate this to one row per student.

### Saving the result to CSV

Add a `to_csv()` call to write the result to a file:

```python
if __name__ == '__main__':
    df = get_enrollment()
    print(df.head())
    print()
    df.info()
    print()
    print(df.describe())
    df.to_csv('student_report/reports/enrollment.csv', index=False)
    print("Saved enrollment.csv")
```

Run again:

```bash
python student_report/db.py
```

Open `student_report/reports/enrollment.csv` in VS Code or Excel and verify that the column names are lowercase and the data looks correct. This file is in `reports/`, which is gitignored — it is generated output, not source code.

## db.py v2 — Complete File

When you are finished exploring, remove the `if __name__ == '__main__':` block. Before deleting the block, make sure you have run `python student_report/db.py` at least once and confirmed `enrollment.csv` was saved. The final `db.py` defines one constant and one function:

```python
from pathlib import Path
from dotenv import load_dotenv
from lightoracle import LightOracleConnection

load_dotenv(Path(__file__).parent / ".env")

ENROLLMENT_QUERY = """
    SELECT
        s.STUDENT_ID,
        s.FIRST_NAME,
        s.LAST_NAME,
        s.ZIP,
        z.CITY,
        z.STATE,
        c.DESCRIPTION  AS COURSE_NAME,
        c.COST,
        e.ENROLL_DATE,
        e.FINAL_GRADE
    FROM student s
    JOIN zipcode    z ON s.ZIP        = z.ZIP
    JOIN enrollment e ON s.STUDENT_ID = e.STUDENT_ID
    JOIN section  sec ON e.SECTION_ID = sec.SECTION_ID
    JOIN course     c ON sec.COURSE_NO = c.COURSE_NO
"""


def get_enrollment():
    conn = LightOracleConnection()
    df = conn.execute_query(ENROLLMENT_QUERY)
    df.columns = df.columns.str.lower()
    return df
```

`main.py` (Session 12) will call `get_enrollment()` by importing `db.py`. Because there is no top-level code after `load_dotenv(...)`, the import is safe — no database query happens until `get_enrollment()` is explicitly called.

> **Note:** `student_report/data/enrollment.csv` is a pre-committed static file generated from this function. Once `db.py` is wired into `main.py` in Session 12, every pipeline run regenerates it automatically from the live Oracle database — the static file is no longer needed for day-to-day use.

In Session 10, we shift to the API side of the data flow. `db.py` stays exactly as it is.

## Practice Exercise

> Optional enrichment — complete during the session if time allows, or finish independently on your fork.
>
> **GSU network required** (GSU WiFi on campus, or VPN if off campus).

The starter script is at [`exercises/session_09_exercise.py`](../exercises/session_09_exercise.py). It contains instructions and fill-in-the-blank placeholders. If you get stuck, the completed version is at [`exercises/session_09_answer.py`](../exercises/session_09_answer.py).

Run from the repo root:

```
python exercises/session_09_exercise.py
```

## Additional Resources

- [lightoracle — GSU-Analytics/lightoracle](https://github.com/GSU-Analytics/lightoracle)
- [python-dotenv documentation](https://saurabh-kumar.com/python-dotenv/)
- [pandas — DataFrame.to_csv](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html)
- [GSU Oracle SQL Training](https://github.com/GSU-Analytics/oracle-sql-training) — SQL reference for the workshop schema
