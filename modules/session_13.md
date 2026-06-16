# Session 13 — Introduction to Unit Testing *(Optional)*

## Introduction

The pipeline works. Session 13 asks: how do we know it will keep working? Unit tests are short, automated checks that verify specific functions behave correctly. When a change to one function breaks another, tests catch the problem immediately — before it reaches the data. This session walks through the 12 tests already written in `student_report/tests/` and shows how to run them with `pytest`.

This session is optional. Skip it if time does not allow; the pipeline is complete without it.

Reference: Prior sessions — Sessions 8–11 (`transform.py` and `report.py` are the modules under test)

---

## Setting Up

Open VS Code, activate your conda environment in the terminal, and open `student_report/tests/`.

In Git Bash:

```
conda activate student-report
```

Confirm `(student-report)` appears in your terminal prompt before continuing.

Run the tests now to confirm everything passes before reading any further:

```bash
pytest student_report/tests/ -v
```

You should see 12 tests collected and all passing. If any fail, check that the conda environment is active and that `student_report/` contains the completed `transform.py` and `report.py` files from prior sessions.

---

## Why Test?

The pipeline merges data from three sources and runs a chain of transformations. If `merge_data()` stops normalizing `ncessch` correctly, the join silently produces zero matches — and the report is wrong with no error message. If `save_top_schools_chart()` fails to close the figure, memory usage grows with every run. These are bugs that would be invisible until someone noticed the output looked wrong.

Unit tests are functions that call your code with known inputs and assert that the output matches what you expect. A passing test suite is evidence that each function works in isolation. When you add a feature or change a function, re-running the tests tells you immediately if something broke.

The tests in this project cover `transform.py` and `report.py`. `db.py` and `api.py` are excluded because their behavior depends on live external systems — a database connection and a network call — which are outside the scope of unit testing.

---

## Pytest Basics

Pytest is a testing framework for Python. It collects and runs test functions automatically, reports failures with clear messages, and provides fixtures for managing test data.

A test function has two requirements: its name starts with `test_`, and it contains one or more `assert` statements. Pytest runs the function; if any assertion fails, the test fails. If the function completes without error, the test passes.

```python
def test_something():
    result = 2 + 2
    assert result == 4
```

Run a directory of tests with:

```bash
pytest student_report/tests/ -v
```

`-v` (verbose) prints one line per test with its name and result, rather than just a dot per test.

---

## The Test Files

The `tests/` directory contains three files:

```
student_report/tests/
├── __init__.py        # empty — marks tests/ as a Python package
├── test_transform.py  # 9 tests for transform.py
└── test_report.py     # 3 tests for report.py
```

`__init__.py` is empty. Its presence makes `tests/` a Python package, which allows pytest to discover and import the test files reliably.

### sys.path setup

Both test files begin with the same three lines:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

When pytest runs from the repo root, Python does not automatically know where `transform.py` and `report.py` live. `__file__` is the test file's own path; `.parent` is `student_report/tests/`; `.parent.parent` is `student_report/`. Inserting that directory at position 0 in `sys.path` tells Python to look there first when resolving imports — so `from transform import ...` finds `student_report/transform.py`.

### Fixtures

A fixture is a function decorated with `@pytest.fixture` that provides test data. Any test function that lists a fixture's name as a parameter receives its return value automatically — pytest handles the wiring.

```python
@pytest.fixture
def enrollment_df():
    return pd.DataFrame({
        'student_id': [1, 1, 2],
        'first_name': ['Alice', 'Alice', 'Bob'],
        ...
    })

def test_get_students_deduplicates(enrollment_df):
    result = get_students(enrollment_df)
    assert len(result) == 2
```

The `enrollment_df` fixture builds a small DataFrame: two students, but student 1 appears twice (two enrollments). The test calls `get_students()` and asserts the result has exactly 2 rows — confirming deduplication works.

Fixtures keep test data defined once and reused across multiple tests. If the expected input format ever changes, you update the fixture and every test that uses it reflects the change automatically.

---

## test_transform.py — Walkthrough

`test_transform.py` contains 9 tests covering all five functions in `transform.py`.

### Testing get_students()

```python
def test_get_students_deduplicates(enrollment_df):
    result = get_students(enrollment_df)
    assert len(result) == 2

def test_get_students_columns(enrollment_df):
    result = get_students(enrollment_df)
    assert list(result.columns) == ['student_id', 'first_name', 'last_name', 'zip', 'city', 'state']
```

Two separate assertions: one for row count (deduplication worked), one for column names (no extra columns slipped through). Keeping them in separate test functions means a failure points to exactly what went wrong.

### Testing merge_data() — correct values

```python
def test_merge_data_school_size_bucket(enrollment_df, survey_df, school_df):
    students = get_students(enrollment_df)
    result = merge_data(students, survey_df, school_df).set_index('student_id')
    assert str(result.loc[1, 'school_size']) == 'Medium (300-700)'
    assert str(result.loc[2, 'school_size']) == 'Small (<300)'
```

The fixture data has school enrollments of 450 (Medium) and 250 (Small). This test checks that `pd.cut()` assigned the correct bucket to each student. `str(...)` converts the `Categorical` value to a plain string for comparison.

### Testing merge_data() — edge cases

```python
def test_merge_data_zip_padding(school_df):
    students = pd.DataFrame({
        'student_id': [3],
        'zip': ['7030'],  # missing leading zero
        ...
    })
    result = merge_data(students, survey, school_df)
    assert result.iloc[0]['school_name'] == 'Hoboken Middle School'
```

This test constructs its own input — a student whose ZIP is `'7030'` instead of `'07030'`. Without the `.str.zfill(5)` normalization in `merge_data()`, the join would fail silently and `school_name` would be `NaN`. The assertion confirms the match still succeeds after padding.

```python
def test_merge_data_unmatched_student(enrollment_df, school_df):
    survey = pd.DataFrame({'student_id': [1], ...})  # only student 1
    students = get_students(enrollment_df)
    result = merge_data(students, survey, school_df)
    row2 = result[result['student_id'] == 2].iloc[0]
    assert pd.isna(row2['middle_school_name'])
```

Student 2 has no survey entry. The left join should produce `NaN` for `middle_school_name` — not an error, and not a dropped row. The test confirms the unmatched student survives the merge with `NaN` school data.

### Testing the summarize functions

```python
def test_summarize_top_schools_columns(enrollment_df, survey_df, school_df):
    students = get_students(enrollment_df)
    merged = merge_data(students, survey_df, school_df)
    result = summarize_top_schools(merged)
    assert 'middle_school_name' in result.columns
    assert 'student_count' in result.columns
    assert len(result) <= 10
```

The three summarize tests follow the same pattern: build the merged DataFrame from fixtures, call the function, and check that the result has the expected columns and shape. They do not assert specific values because the aggregate results are fully determined by the fixture data — checking columns and row count is sufficient to confirm the functions produce the right structure.

---

## test_report.py — Walkthrough

`test_report.py` has one additional setup line not present in `test_transform.py`:

```python
import matplotlib
matplotlib.use('Agg')
```

`matplotlib.use('Agg')` switches to the Agg rendering backend, which writes to files without needing a display. Tests run in headless environments — a terminal, a CI server — where there is no screen to open a window on. Without this line, the chart functions would attempt to display an interactive window and fail. This call must appear before `import matplotlib.pyplot` or any import that pulls in pyplot.

### The tmp_path fixture

```python
def test_save_top_schools_chart(top_schools_df, tmp_path):
    path = save_top_schools_chart(top_schools_df, tmp_path)
    assert path.exists()
    assert path.suffix == '.png'
```

`tmp_path` is a built-in pytest fixture — no import needed. It provides a temporary directory as a `Path` object. The directory is created fresh for each test and deleted automatically when the test finishes. Passing it to `save_top_schools_chart()` as `output_dir` means the chart is written to a throwaway location rather than the real `reports/` directory.

The assertions check that the returned path exists on disk and has a `.png` extension.

### Testing the Excel workbook

```python
def test_save_excel_report_sheets(merged_df, top_schools_df, zip_summary_df, size_df, tmp_path):
    from openpyxl import load_workbook
    chart1 = save_top_schools_chart(top_schools_df, tmp_path)
    chart2 = save_size_chart(size_df, tmp_path)
    path = save_excel_report(merged_df, top_schools_df, zip_summary_df, size_df, [chart1, chart2], tmp_path)
    wb = load_workbook(path)
    assert wb.sheetnames == ['Student Data', 'Top 10 Schools', 'By ZIP', 'By School Size', 'Charts']
```

This test calls `save_top_schools_chart()` and `save_size_chart()` first to produce real PNG files, then passes those paths to `save_excel_report()`. After the function returns, it opens the workbook with `openpyxl` and asserts the sheet names match exactly — in the correct order. If a sheet is missing, renamed, or created in the wrong order, this assertion fails.

---

## Running the Tests

Run all tests with verbose output:

```bash
pytest student_report/tests/ -v
```

Expected output:

```
collected 12 items

student_report/tests/test_transform.py::test_get_students_deduplicates PASSED
student_report/tests/test_transform.py::test_get_students_columns PASSED
student_report/tests/test_transform.py::test_merge_data_row_count PASSED
student_report/tests/test_transform.py::test_merge_data_school_size_bucket PASSED
student_report/tests/test_transform.py::test_merge_data_zip_padding PASSED
student_report/tests/test_transform.py::test_merge_data_unmatched_student PASSED
student_report/tests/test_transform.py::test_summarize_top_schools_columns PASSED
student_report/tests/test_transform.py::test_summarize_by_zip_columns PASSED
student_report/tests/test_transform.py::test_summarize_by_size_columns PASSED
student_report/tests/test_report.py::test_save_top_schools_chart PASSED
student_report/tests/test_report.py::test_save_size_chart PASSED
student_report/tests/test_report.py::test_save_excel_report_sheets PASSED

12 passed in ...s
```

Run a single test file:

```bash
pytest student_report/tests/test_transform.py -v
```

Run a single test by name:

```bash
pytest student_report/tests/test_transform.py::test_merge_data_zip_padding -v
```

---

## Additional Resources

- [pytest — Getting started](https://docs.pytest.org/en/stable/getting-started.html)
- [pytest — Fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [pytest — tmp_path fixture](https://docs.pytest.org/en/stable/how-to/tmp_path.html)
- [matplotlib — Non-interactive backends](https://matplotlib.org/stable/users/explain/figure/backends.html)
