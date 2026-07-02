# Session 7 — Generating the Excel Report

## Introduction

Sessions 5 and 6 produced five DataFrames and two chart files. This session builds `report.py` v2: `save_excel_report()`, a function that writes a five-sheet Excel workbook and embeds the saved charts as images on a dedicated sheet. After this session, `transform.py` and `report.py` are both complete and you will run them end-to-end to produce the full Phase 1 output.

## Setting Up

Open VS Code, activate your conda environment in the terminal, and open `student_report/report.py`.

In Git Bash:

```zsh
conda activate student-report
```

Confirm `(student-report)` appears in your terminal prompt before continuing.

> **No VPN or prior sessions required.** The `__main__` block imports from `transform.py` and loads the pre-committed CSV files from `student_report/data/`. It also requires the two chart `.png` files saved in Session 6. Make sure `top_middle_schools.png` and `school_size_distribution.png` exist in `student_report/reports/` before running.

## Building report.py v2

### Adding save_excel_report()

`save_excel_report()` takes five inputs and an output directory: the full merged DataFrame, the three summary DataFrames, and a list of chart file paths.

Add the function below `save_size_chart()`:

```python
def save_excel_report(merged_df, top_schools_df, zip_summary_df, size_df, chart_paths, output_dir):
    from openpyxl import load_workbook
    from openpyxl.drawing.image import Image as XLImage

    path = Path(output_dir) / "student_report.xlsx"
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        merged_df.to_excel(writer, sheet_name='Student Data', index=False)
        top_schools_df.to_excel(writer, sheet_name='Top 10 Schools', index=False)
        zip_summary_df.to_excel(writer, sheet_name='By ZIP', index=False)
        size_df.to_excel(writer, sheet_name='By School Size', index=False)

    wb = load_workbook(path)
    ws = wb.create_sheet('Charts')
    row = 1
    for chart_path in chart_paths:
        img = XLImage(str(chart_path))
        ws.add_image(img, f'A{row}')
        row += 30
    wb.save(path)
    return path
```

This function has two distinct phases. Walk through each one.

### Phase 1 — Writing the four data sheets

```python
with pd.ExcelWriter(path, engine='openpyxl') as writer:
    merged_df.to_excel(writer, sheet_name='Student Data', index=False)
    top_schools_df.to_excel(writer, sheet_name='Top 10 Schools', index=False)
    zip_summary_df.to_excel(writer, sheet_name='By ZIP', index=False)
    size_df.to_excel(writer, sheet_name='By School Size', index=False)
```

**`pd.ExcelWriter(path, engine='openpyxl')`** — opens an Excel file for writing. `engine='openpyxl'` specifies the library that handles the `.xlsx` format. Using it as a context manager (`with ... as writer:`) guarantees the file is saved and closed when the block exits, even if an error occurs mid-write.

**`.to_excel(writer, sheet_name=..., index=False)`** — each call writes one DataFrame to one sheet. `sheet_name` sets the tab label. `index=False` prevents pandas from writing the row numbers (0, 1, 2, …) as an extra column in the spreadsheet.

When the `with` block exits, the file is written to disk with four sheets.

### Phase 2 — Adding the Charts sheet

```python
wb = load_workbook(path)
ws = wb.create_sheet('Charts')
row = 1
for chart_path in chart_paths:
    img = XLImage(str(chart_path))
    ws.add_image(img, f'A{row}')
    row += 30
wb.save(path)
```

`pd.ExcelWriter` does not support inserting images — it is a DataFrame-to-sheet writer, nothing more. To embed charts, we reopen the file with `openpyxl` directly.

**`load_workbook(path)`** — opens the `.xlsx` file that ExcelWriter just saved, returning a workbook object with the four existing sheets intact.

**`wb.create_sheet('Charts')`** — appends a new empty sheet named `Charts` to the workbook.

**`XLImage(str(chart_path))`** — loads a PNG file as an Excel image object. `str(chart_path)` is needed because `XLImage` expects a string path, not a `Path` object.

**`ws.add_image(img, f'A{row}')`** — places the image with its top-left corner anchored at cell `A{row}`. The first chart lands at `A1`; each subsequent chart is placed 30 rows lower (`row += 30`) to avoid overlap.

**`wb.save(path)`** — writes the modified workbook back to the same file, overwriting the version that ExcelWriter saved. The final file has five sheets.

The two `from openpyxl import ...` lines appear inside the function rather than at the top of the file. `openpyxl` is only needed by this one function, so placing the imports here keeps the dependency visible alongside the code that uses it.

### Testing with a __main__ block

Add a `if __name__ == '__main__':` block:

```python
if __name__ == '__main__':
    from transform import get_students, merge_data, summarize_top_schools, summarize_by_zip, summarize_by_size

    enrollment_df = pd.read_csv('student_report/data/enrollment.csv')
    survey_df = pd.read_csv('student_report/data/survey_middle_schools.csv')
    school_df = pd.read_csv('student_report/data/schools.csv')

    students = get_students(enrollment_df)
    merged = merge_data(students, survey_df, school_df)
    top_schools = summarize_top_schools(merged)
    zip_summary = summarize_by_zip(merged)
    size_summary = summarize_by_size(merged)

    output_dir = 'student_report/reports'
    chart_paths = [
        Path(output_dir) / 'top_middle_schools.png',
        Path(output_dir) / 'school_size_distribution.png',
    ]

    path = save_excel_report(merged, top_schools, zip_summary, size_summary, chart_paths, output_dir)
    print(f"Saved: {path}")
```

Run from the repo root:

```bash
python student_report/report.py
```

Open `student_report/reports/student_report.xlsx` and verify five sheets: Student Data, Top 10 Schools, By ZIP, By School Size, Charts. The Charts sheet should show both chart images stacked vertically.

### Running Phase 1 End-to-End

With `transform.py` and `report.py` both complete, run them in sequence from the repo root to produce every output file:

```bash
python student_report/transform.py
python student_report/report.py
```

After the second command, `student_report/reports/` should contain:

```
merged.csv
top_middle_schools.png
school_size_distribution.png
student_report.xlsx
```

Open `student_report.xlsx` and confirm all five sheets are present. You have just produced the same outputs as the manual process — from the command line, in seconds, with no Excel formulas.

### What's Next: Phase 2

`enrollment.csv` and `schools.csv` in `student_report/data/` represent data that someone collected by hand before this workshop — enrollment exported from SQL Developer, school directory downloaded from the Urban Institute website. The Python pipeline you built in Phase 1 consumes these files exactly as the manual process would.

Phase 2 eliminates the manual steps. Sessions 8–11 build `db.py` and `api.py` — the two modules that replace those static files with live queries. When `main.py` wires everything together in Session 12, you will run one command that fetches fresh data, transforms it, and produces the full report automatically.

The code you wrote in Phase 1 does not change. `transform.py` and `report.py` are exactly what `main.py` will call.

## report.py v2 — Complete File

Remove the `if __name__ == '__main__':` block. The final `report.py` defines three imports and three functions:

```python
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


def save_top_schools_chart(top_schools_df, output_dir):
    path = Path(output_dir) / "top_middle_schools.png"
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_schools_df['middle_school_name'], top_schools_df['student_count'], color='steelblue')
    ax.set_xlabel("Number of Students")
    ax.set_title("Top 10 Middle Schools by Student Count")
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def save_size_chart(size_df, output_dir):
    path = Path(output_dir) / "school_size_distribution.png"
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(size_df['school_size'].astype(str), size_df['student_count'], color='teal')
    ax.set_xlabel("School Size")
    ax.set_ylabel("Number of Students")
    ax.set_title("Students by Middle School Size")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def save_excel_report(merged_df, top_schools_df, zip_summary_df, size_df, chart_paths, output_dir):
    from openpyxl import load_workbook
    from openpyxl.drawing.image import Image as XLImage

    path = Path(output_dir) / "student_report.xlsx"
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        merged_df.to_excel(writer, sheet_name='Student Data', index=False)
        top_schools_df.to_excel(writer, sheet_name='Top 10 Schools', index=False)
        zip_summary_df.to_excel(writer, sheet_name='By ZIP', index=False)
        size_df.to_excel(writer, sheet_name='By School Size', index=False)

    wb = load_workbook(path)
    ws = wb.create_sheet('Charts')
    row = 1
    for chart_path in chart_paths:
        img = XLImage(str(chart_path))
        ws.add_image(img, f'A{row}')
        row += 30
    wb.save(path)
    return path
```

`report.py` is now complete. Run `python student_report/transform.py` followed by `python student_report/report.py` to produce all Phase 1 outputs. In Session 12, `main.py` wires all four modules together so that a single command does this end-to-end with no manual steps.

## Practice Exercise

> Optional enrichment — complete during the session if time allows, or finish independently on your fork.

The starter script is at [`exercises/session_07_exercise.py`](../exercises/session_07_exercise.py). It contains instructions and fill-in-the-blank placeholders. If you get stuck, the completed version is at [`exercises/session_07_answer.py`](../exercises/session_07_answer.py).

Run from the repo root:

```
python exercises/session_07_exercise.py
```

## Additional Resources

- [pandas — ExcelWriter](https://pandas.pydata.org/docs/reference/api/pandas.ExcelWriter.html)
- [pandas — DataFrame.to_excel](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html)
- [openpyxl — Working with images](https://openpyxl.readthedocs.io/en/stable/images.html)
- [openpyxl — Tutorial](https://openpyxl.readthedocs.io/en/stable/tutorial.html)
