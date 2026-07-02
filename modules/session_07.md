# Session 7 — Creating Visualizations

## Introduction

`transform.py` is complete. The pipeline now produces three summary DataFrames — top schools, by ZIP, and by school size — plus the full merged DataFrame. This session builds `report.py` v1: two functions that turn those summaries into saved chart files. By the end of the session, two `.png` files are written to the reports directory and the chart-generation layer of the pipeline is done.

## Setting Up

Open VS Code and activate your conda environment in the terminal.

In the Explorer pane, right-click the `student_report/` folder and choose **New File**. Name it `report.py`.

In the terminal:

```zsh
conda activate student-report
```

Confirm `(student-report)` appears in your terminal prompt before continuing.

> **No VPN or prior sessions required.** The `__main__` block imports from `transform.py` and loads the pre-committed CSV files from `student_report/data/`.

## Building report.py v1

### Starting the file

Create `student_report/report.py` and add the imports:

```python
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
```

`matplotlib` is already installed in the conda environment. `pd` and `Path` are included because the `__main__` block uses them; neither is used by the two chart functions directly.

### save_top_schools_chart()

Add `save_top_schools_chart()` below the imports:

```python
def save_top_schools_chart(top_schools_df, output_dir):
    path = Path(output_dir) / "top_middle_schools.png"
    fig, ax = plt.subplots(figsize=(10, 6)) # <1>
    ax.barh(                                  # <2>
        top_schools_df['middle_school_name'], # <2>
        top_schools_df['student_count'],      # <2>
        color='steelblue'                     # <2>
    )                                         # <2>
    ax.set_xlabel("Number of Students") # <3>
    ax.set_title("Top 10 Middle Schools by Student Count") # <4>
    ax.invert_yaxis() # <5>
    plt.tight_layout() # <6>
    plt.savefig(path) # <7>
    plt.close() # <8>
    return path # <9>
```

1. Creates a figure and a single set of axes. `fig` is the overall container; `ax` is the drawing area where the chart is placed. `figsize=(10, 6)` sets the width and height in inches — wide enough to show school names without overlap.
2. Draws a horizontal bar chart. The first argument is the y-axis labels (`middle_school_name`), the second is the bar lengths (`student_count`). Horizontal bars are the right choice here because school names are long strings that would overlap on a vertical chart's x-axis.
3. Labels the x-axis. On a horizontal bar chart the x-axis carries the numeric values, so this is the axis that needs a unit label.
4. Adds a title above the chart.
5. By default `barh` places the first row at the bottom of the chart. After sorting descending in `summarize_top_schools()`, the school with the highest count is in the first row — which would end up at the bottom without this call. `invert_yaxis()` flips the order so the largest bar appears at the top, which is the natural reading direction for a ranked list.
6. Adjusts spacing so axis labels and the title are not clipped at the figure edges. It should be called after all labels are set and before saving.
7. Writes the figure to a file. The format is inferred from the file extension (`.png`). The file is written to `output_dir` regardless of the current working directory.
8. Releases the figure from memory. Without this call, every chart created in a session accumulates in memory, and matplotlib will print a warning after 20 open figures. Always call `plt.close()` immediately after saving.
9. Returns the saved file path so the caller (later, `main.py`) can log or display it.

### save_size_chart()

Add `save_size_chart()` below `save_top_schools_chart()`. The structure mirrors `save_top_schools_chart()` with a few differences:

```python
def save_size_chart(size_df, output_dir):
    path = Path(output_dir) / "school_size_distribution.png"
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(                                   # <1>
        size_df['school_size'].astype(str),   # <2>
        size_df['student_count'],
        color='teal'
    )
    ax.set_xlabel("School Size")
    ax.set_ylabel("Number of Students")       # <3>
    ax.set_title("Students by Middle School Size")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path
```

1. **`ax.bar()` instead of `ax.barh()`** — vertical bars. The three size category labels are short (`Small`, `Medium`, `Large`) and fit comfortably on a horizontal x-axis, so there is no reason to rotate the chart.
2. **`size_df['school_size'].astype(str)`** — `school_size` is a pandas `Categorical` column (created by `pd.cut()` in Session 6). matplotlib does not know how to place categorical tick marks automatically, so converting to plain strings produces clean, evenly spaced labels on the x-axis.
3. **`ax.set_ylabel("Number of Students")`** — a vertical chart carries the numeric values on the y-axis, which now needs the unit label. The x-axis label (`ax.set_xlabel`) describes the categories.

No `invert_yaxis()` call — the three size bins are not a ranked list, so the default bottom-to-top direction is fine.

### Testing with a __main__ block

Add a `if __name__ == '__main__':` block that imports from `transform.py` and produces both charts:

```python
if __name__ == '__main__':
    from transform import get_students, merge_data, summarize_top_schools, summarize_by_size

    enrollment_df = pd.read_csv('student_report/data/enrollment.csv')
    survey_df = pd.read_csv('student_report/data/survey_middle_schools.csv')
    school_df = pd.read_csv('student_report/data/schools.csv')

    students = get_students(enrollment_df)
    merged = merge_data(students, survey_df, school_df)
    top_schools = summarize_top_schools(merged)
    size_summary = summarize_by_size(merged)

    output_dir = 'student_report/reports'
    chart1 = save_top_schools_chart(top_schools, output_dir)
    chart2 = save_size_chart(size_summary, output_dir)
    print(f"Saved: {chart1}")
    print(f"Saved: {chart2}")
```

The `from transform import ...` line works because running `python student_report/report.py` adds the `student_report/` directory to Python's module search path automatically, making `transform.py` importable by name.

Run from the repo root:

```bash
python student_report/report.py
```

You should see two file paths printed. Open `student_report/reports/` and confirm that `top_middle_schools.png` and `school_size_distribution.png` were created or updated. Open each file to verify the charts look right — the horizontal bar chart should show schools ranked largest at the top; the vertical bar chart should show three labeled columns.

## report.py v1 — Complete File

Remove the `if __name__ == '__main__':` block. The final `report.py` v1 defines three imports and two functions:

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
```

`main.py` (Session 13) will call both functions by importing `report.py`. There is no top-level code after the imports, so the import is safe — no file I/O or computation happens until the functions are explicitly called.

In Session 8, we add `save_excel_report()` to `report.py`: a function that writes the full five-sheet Excel workbook and embeds the saved chart images.

## Practice Exercise

> Optional enrichment — complete during the session if time allows, or finish independently on your fork.

The starter script is at [`exercises/session_07_exercise.py`](../exercises/session_07_exercise.py). It contains instructions and fill-in-the-blank placeholders. If you get stuck, the completed version is at [`exercises/session_07_answer.py`](../exercises/session_07_answer.py).

Run from the repo root:

```
python exercises/session_07_exercise.py
```

## Additional Resources

- [matplotlib — Horizontal bar chart (barh)](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.barh.html)
- [matplotlib — Bar chart (bar)](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.bar.html)
- [matplotlib — savefig](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html)
- [matplotlib — Pyplot tutorial](https://matplotlib.org/stable/tutorials/pyplot.html)
- *Automate the Boring Stuff with Python*, 3rd Ed. — Chapter 17 (working with files and directories)
