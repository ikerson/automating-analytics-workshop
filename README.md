# Automating Data Analytics with Python

This workshop is designed for GSU analysts who want to replace a time-consuming manual reporting workflow with a single Python command. Over 14 sessions (12 core hours), participants build a working Python package from scratch — connecting to an Oracle database, calling a web API, merging and summarizing data, and producing charts and an Excel workbook automatically. Session 14 (optional) introduces unit testing.

**[Read the workshop book →](https://GSU-Analytics.github.io/automating-analytics-workshop/)**

The finished product:

```
python main.py --year 2019 --output reports/
```

## Sessions

### Before the Workshop

0. [Session 0 — Before You Begin](modules/session_00.md)  
   Install Miniconda, Git, VS Code, and create a GitHub account before Session 1. Includes setup verification steps and instructions for forking the workshop repo.

### Part 1 — Why, How, and Tooling

1. [Session 1 — The Problem + Tooling Overview](modules/session_01.md)  
   Side-by-side comparison of the manual workflow and what we will build. Live demo of the finished package. Introduction to the tool stack: Python, conda, Git, and VS Code.

2. [Session 2 — Setting Up the Environment](modules/session_02.md)  
   Clone your fork, create the conda environment, configure VS Code, and make your first Git commit.

### Part 2 — Working with Provided Data (Phase 1)

3. [Session 3 — Python Foundations](modules/session_03.md)  
   A one-hour primer on core Python: variables, data types, lists, dictionaries, loops, conditionals, and functions. Complete before Session 4 if you are new to Python.

4. [Session 4 — Pandas and Working with Data](modules/session_04.md)  
   Load and inspect a CSV with pandas. Select columns, filter rows, and write a reusable function.

5. [Session 5 — Merging the Three Sources](modules/session_05.md)  
   Deduplicate enrollment data. Perform a three-way merge: students → survey on `student_id` → school directory on `ncessch`. All three source files are pre-committed to `student_report/data/`.

6. [Session 6 — Aggregations and Summary Statistics](modules/session_06.md)  
   Compute top schools, ZIP counts, and school size distribution using `groupby`, `agg`, and `pd.cut`.

7. [Session 7 — Creating Visualizations](modules/session_07.md)  
   Build a horizontal bar chart and a vertical bar chart with matplotlib. Save them as PNG files.

8. [Session 8 — Generating the Excel Report](modules/session_08.md)  
   Write a five-sheet Excel workbook with `pandas.ExcelWriter` and embed the chart images with `openpyxl`.

### Part 3 — Automating Data Collection (Phase 2)

9. [Session 9 — Connecting to the Database](modules/session_09.md)  
   Connect to the Oracle training server with `lightoracle`. Store credentials in a `.env` file. Run a SELECT query and see the results.

10. [Session 10 — Working with Database Results](modules/session_10.md)  
    Build the full five-table enrollment query in `get_enrollment()`. Normalize column names and save enrollment data to CSV.

11. [Session 11 — Calling a Web API](modules/session_11.md)  
    Introduction to APIs and JSON. Call the Urban Institute Education Data Portal to fetch NY and NJ middle school directory data.

12. [Session 12 — Working with API Results](modules/session_12.md)  
    Select the columns you need from the API response and save to CSV.

### Part 4 — Automation

13. [Session 13 — The Automated Pipeline](modules/session_13.md)  
    Wire all modules together in `main.py` using `argparse`. Run the full pipeline end-to-end.

### Part 5 — Optional

14. [Session 14 — Introduction to Unit Testing](modules/session_14.md) *(optional)*  
    Write and run `pytest` tests for the transform and report modules.

---

## Exercises

Sessions 3–12 each include a practice exercise. Run all scripts from the repo root with the conda environment active.

| Session | Topic | Exercise | Answer |
|---|---|---|---|
| 3 | Python Foundations | [session_03_exercise.py](exercises/session_03_exercise.py) | [session_03_answer.py](exercises/session_03_answer.py) |
| 4 | Pandas and Working with Data | [session_04_exercise.py](exercises/session_04_exercise.py) | [session_04_answer.py](exercises/session_04_answer.py) |
| 5 | Merging the Three Sources | [session_05_exercise.py](exercises/session_05_exercise.py) | [session_05_answer.py](exercises/session_05_answer.py) |
| 6 | Aggregations and Summary Statistics | [session_06_exercise.py](exercises/session_06_exercise.py) | [session_06_answer.py](exercises/session_06_answer.py) |
| 7 | Creating Visualizations | [session_07_exercise.py](exercises/session_07_exercise.py) | [session_07_answer.py](exercises/session_07_answer.py) |
| 8 | Generating the Excel Report | [session_08_exercise.py](exercises/session_08_exercise.py) | [session_08_answer.py](exercises/session_08_answer.py) |
| 9 | Connecting to the Database ¹ | [session_09_exercise.py](exercises/session_09_exercise.py) | [session_09_answer.py](exercises/session_09_answer.py) |
| 10 | Working with Database Results ¹ | [session_10_exercise.py](exercises/session_10_exercise.py) | [session_10_answer.py](exercises/session_10_answer.py) |
| 11 | Calling a Web API | [session_11_exercise.py](exercises/session_11_exercise.py) | [session_11_answer.py](exercises/session_11_answer.py) |
| 12 | Working with API Results | [session_12_exercise.py](exercises/session_12_exercise.py) | [session_12_answer.py](exercises/session_12_answer.py) |

¹ GSU network required (on-campus WiFi or VPN).

---

## Resources

- *Automate the Boring Stuff with Python*, 3rd Ed. — reference book for this workshop (free online with GSU credentials via O'Reilly)
- [Python Environment Setup Guide](https://github.com/GSU-Analytics/python_guides/wiki/Python-Environment-Setup)
- [Conda cheat sheet](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf)
- [Git cheat sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [pandas documentation](https://pandas.pydata.org/docs/)
