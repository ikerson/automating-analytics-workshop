# Session 12 — The Automated Pipeline

## Introduction

Sessions 4–7 built the data transformation and reporting modules (`transform.py` and `report.py`). Sessions 8–11 built the data collection modules (`db.py` and `api.py`). Each module has been tested individually. This session builds `main.py`: a short script that imports all four modules and calls them in sequence, turning the manual multi-step process into a single command.

## Setting Up

Open VS Code and activate your conda environment in the terminal.

In the Explorer pane, right-click the `student_report/` folder and choose **New File**. Name it `main.py`.

In the terminal:

```zsh
conda activate student-report
```

Confirm `(student-report)` appears in your terminal prompt before continuing.

> **GSU network required.** `main.py` calls `get_enrollment()` from `db.py`, which connects to the Oracle server on the GSU network. On campus, GSU WiFi is sufficient. If you are working off campus, connect to the GSU VPN first.

## Building main.py

### Imports

Start the file with the imports:

```python
import argparse
from pathlib import Path
import pandas as pd
from db import get_enrollment
from api import get_school_data
from transform import get_students, merge_data, summarize_top_schools, summarize_by_zip, summarize_by_size
from report import save_top_schools_chart, save_size_chart, save_excel_report
```

The first three lines import from the Python standard library and from `pandas`. The last four import from the four modules built in this workshop — `db`, `api`, `transform`, and `report` — by name, without a package prefix.

Python finds these imports because running `python student_report/main.py` from the repo root automatically adds `student_report/` to the module search path. That makes `db`, `api`, `transform`, and `report` importable by name, exactly like any installed package.

### The main() function

Add the `main()` function below the imports:

```python
def main(args):
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    print("Fetching enrollment data from Oracle...")
    enrollment_df = get_enrollment()
    students_df = get_students(enrollment_df)
    print(f"  {len(students_df)} students")

    print("Loading middle school survey data...")
    survey_path = Path(__file__).parent / "data" / "survey_middle_schools.csv"
    survey_df = pd.read_csv(survey_path, dtype={'student_id': int, 'ncessch': str})
    print(f"  {len(survey_df)} survey records")

    print(f"Fetching school data from API (year={args.year}, fips='36,34')...")
    school_df = get_school_data(args.year)
    print(f"  {len(school_df)} school records")

    print("Merging and summarizing...")
    merged_df = merge_data(students_df, survey_df, school_df)
    top_schools = summarize_top_schools(merged_df)
    zip_summary = summarize_by_zip(merged_df)
    size_summary = summarize_by_size(merged_df)

    merged_csv = output / "merged.csv"
    merged_df.to_csv(merged_csv, index=False)
    print(f"  Saved {merged_csv}")

    print("Generating charts...")
    chart1 = save_top_schools_chart(top_schools, output)
    chart2 = save_size_chart(size_summary, output)

    print("Generating Excel report...")
    excel_path = save_excel_report(
        merged_df, top_schools, zip_summary, size_summary,
        [chart1, chart2], output,
    )

    print(f"\nDone. Outputs in {output}/")
    print(f"  {merged_csv.name}")
    print(f"  {chart1.name}")
    print(f"  {chart2.name}")
    print(f"  {excel_path.name}")
```

Walk through each section:

**`output = Path(args.output); output.mkdir(parents=True, exist_ok=True)`** — resolves the output directory path and creates it if it does not exist. `parents=True` creates any missing parent directories. `exist_ok=True` means no error is raised if the directory already exists.

**`get_enrollment()` → `get_students()`** — queries Oracle for the full enrollment dataset, then deduplicates to one row per student. The print statement confirms how many students were found.

**`Path(__file__).parent / "data" / "survey_middle_schools.csv"`** — loads the survey CSV relative to `main.py`'s location, not the current working directory. `__file__` is the path of the script being run; `.parent` is the directory it lives in. This path resolves correctly regardless of where you run the command from.

**`dtype={'student_id': int, 'ncessch': str}`** — tells pandas to read `student_id` as an integer and `ncessch` as a string. Reading `ncessch` as a string from the start prevents pandas from converting it to a float, which would require the normalization step `transform.py` applies to API data.

**`get_school_data(args.year)`** — calls the CCD directory API for the year passed on the command line. Pagination is handled automatically by the `EducationDataAPI` client.

**Merge and summarize** — calls the five `transform.py` functions in the same order they were built. Each function receives the DataFrame(s) it needs and returns a clean result.

**`merged_df.to_csv(merged_csv, index=False)`** — saves the merged DataFrame as a flat CSV. This is an intermediate output the team can open in Excel independently of the workbook.

**`save_top_schools_chart` / `save_size_chart`** — each function returns the path of the file it saved. Those paths are collected into a list and passed to `save_excel_report`.

**`save_excel_report(..., [chart1, chart2], output)`** — writes the five-sheet workbook and embeds both charts on the Charts sheet.

**Final print block** — reports exactly which files were written and where, so the user knows where to look.

### argparse — the command-line interface

When you type a command like `python student_report/main.py --year 2019`, Python receives everything after `python` as a plain list of strings:

```python
['student_report/main.py', '--year', '2019']
```

Every value in that list is a string — including `'2019'`. `argparse` is the standard library module that turns that raw list into named Python values your function can actually use. It handles the string-to-integer conversion, supplies default values for anything you omit, and generates a `--help` message automatically.

Add the entry point at the bottom of the file:

```python
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate middle school outreach report."
    )
    parser.add_argument('--year', type=int, default=2019, help='CCD data year (default: 2019)')
    parser.add_argument('--output', type=str, default='reports/', help='Output directory (default: reports/)')
    args = parser.parse_args()
    main(args)
```

**`argparse.ArgumentParser`** — creates the parser object. The `description` text appears at the top of the `--help` output.

**`add_argument('--year', type=int, default=2019, ...)`** — registers `--year` as an optional argument. The `--` prefix is the convention for named arguments you can pass in any order or leave out entirely. `type=int` tells argparse to convert the string `'2019'` to the integer `2019` before storing it. `default=2019` means the argument can be omitted and the pipeline will still run with that value.

**`add_argument('--output', ...)`** — registers `--output` the same way. No `type` is specified, so the value stays a string, which is what `Path()` expects.

**`parse_args()`** — reads the raw list, matches each `--name value` pair to a registered argument, applies type conversions and defaults, and returns a *namespace object* — a simple container where each argument becomes an attribute. After this line, `args` looks like:

```python
Namespace(year=2019, output='reports/')
```

`args.year` and `args.output` are then available as plain attributes inside `main()`.

**`if __name__ == "__main__":`** — this guard ensures the argparse block only runs when `main.py` is executed directly. When another script does `from main import something`, this block is skipped — which prevents argparse from trying to read command-line arguments at import time.

## Running the Pipeline

Run the complete pipeline from the repo root:

```bash
python student_report/main.py --year 2019 --output student_report/reports/
```

You should see progress output similar to:

```
Fetching enrollment data from Oracle...
  165 students
Loading middle school survey data...
  240 survey records
Fetching school data from API (year=2019, fips='36,34')...
  7439 school records
Merging and summarizing...
  Saved student_report/reports/merged.csv
Generating charts...
Generating Excel report...

Done. Outputs in student_report/reports/
  merged.csv
  top_middle_schools.png
  school_size_distribution.png
  student_report.xlsx
```

Open `student_report/reports/` and verify all four output files are present. Open `student_report.xlsx` and confirm five sheets: Student Data, Top 10 Schools, By ZIP, By School Size, Charts.

To run with a different year or output directory:

```bash
python student_report/main.py --year 2018 --output student_report/reports/2018/
```

To see all available options:

```bash
python student_report/main.py --help
```

## main.py — Complete File

```python
import argparse
from pathlib import Path
import pandas as pd
from db import get_enrollment
from api import get_school_data
from transform import get_students, merge_data, summarize_top_schools, summarize_by_zip, summarize_by_size
from report import save_top_schools_chart, save_size_chart, save_excel_report


def main(args):
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    print("Fetching enrollment data from Oracle...")
    enrollment_df = get_enrollment()
    students_df = get_students(enrollment_df)
    print(f"  {len(students_df)} students")

    print("Loading middle school survey data...")
    survey_path = Path(__file__).parent / "data" / "survey_middle_schools.csv"
    survey_df = pd.read_csv(survey_path, dtype={'student_id': int, 'ncessch': str})
    print(f"  {len(survey_df)} survey records")

    print(f"Fetching school data from API (year={args.year}, fips='36,34')...")
    school_df = get_school_data(args.year)
    print(f"  {len(school_df)} school records")

    print("Merging and summarizing...")
    merged_df = merge_data(students_df, survey_df, school_df)
    top_schools = summarize_top_schools(merged_df)
    zip_summary = summarize_by_zip(merged_df)
    size_summary = summarize_by_size(merged_df)

    merged_csv = output / "merged.csv"
    merged_df.to_csv(merged_csv, index=False)
    print(f"  Saved {merged_csv}")

    print("Generating charts...")
    chart1 = save_top_schools_chart(top_schools, output)
    chart2 = save_size_chart(size_summary, output)

    print("Generating Excel report...")
    excel_path = save_excel_report(
        merged_df, top_schools, zip_summary, size_summary,
        [chart1, chart2], output,
    )

    print(f"\nDone. Outputs in {output}/")
    print(f"  {merged_csv.name}")
    print(f"  {chart1.name}")
    print(f"  {chart2.name}")
    print(f"  {excel_path.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate middle school outreach report."
    )
    parser.add_argument('--year', type=int, default=2019, help='CCD data year (default: 2019)')
    parser.add_argument('--output', type=str, default='reports/', help='Output directory (default: reports/)')
    args = parser.parse_args()
    main(args)
```

## What's Next

The pipeline now runs end-to-end with a single command. A few directions to consider from here:

**Scheduling** — instead of running the command manually each month, the pipeline can be scheduled to run automatically.

On Windows, Task Scheduler provides scheduling through a GUI. Create a new task, set the trigger to monthly, and set the action to run `conda run -n student-report python student_report/main.py --year 2019 --output student_report\reports\` from the repo root directory.

**Year parameter** — the `--year` argument makes it straightforward to generate reports for prior years without changing the code.

**Session 13 (optional)** — if time allows, Session 13 introduces `pytest` and walks through the unit tests in `student_report/tests/`. The tests cover `transform.py` and `report.py` and can be run with:

```bash
pytest student_report/tests/ -v
```

## Additional Resources

- [Python — argparse](https://docs.python.org/3/library/argparse.html)
- [Python — pathlib](https://docs.python.org/3/library/pathlib.html)
- [Python — `__file__` and module paths](https://docs.python.org/3/reference/import.html)
- *Automate the Boring Stuff with Python*, 3rd Ed. — Chapter 10 (organizing files)
