# Automating Data Analytics with Python

This workshop is designed for GSU analysts who want to replace a time-consuming manual reporting workflow with a single Python command. Over twelve one-hour sessions, participants build a working Python package from scratch — connecting to an Oracle database, calling a web API, merging and summarizing data, and producing charts and an Excel workbook automatically. Session 13 (optional) introduces unit testing.

The finished product:

```
python main.py --year 2019 --output reports/
```

## Sessions

### Part 1 — Why, How, and Tooling

1. [Session 1 — The Problem + Tooling Overview](modules/session_01.md)  
   Side-by-side comparison of the manual workflow and what we will build. Live demo of the finished package. Introduction to the tool stack: Python, conda, Git, and VS Code.

2. [Session 2 — Setting Up the Environment](modules/session_02.md)  
   Clone your fork, create the conda environment, configure VS Code, and make your first Git commit.

3. [Session 3 — Pandas and Working with Data](modules/session_03.md)  
   Load and inspect a CSV with pandas. Select columns, filter rows, and write a reusable function.

### Part 2 — Getting Data

4. [Session 4 — Connecting to the Database](modules/session_04.md)  
   Connect to the Oracle training server with `oracledb`. Store credentials in a `.env` file. Run a SELECT query and see the results.

5. [Session 5 — Working with Database Results](modules/session_05.md)  
   Upgrade to `pd.read_sql()`. Normalize column names and save enrollment data to CSV.

6. [Session 6 — Calling a Web API](modules/session_06.md)  
   Introduction to APIs and JSON. Call the Urban Institute Education Data Portal to fetch NY and NJ middle school directory data.

7. [Session 7 — Working with API Results](modules/session_07.md)  
   Select the columns you need from the API response and save to CSV.

### Part 3 — Combining and Transforming Data

8. [Session 8 — Merging the Three Sources](modules/session_08.md)  
   Deduplicate enrollment data. Perform a three-way merge: students → survey on `student_id` → school directory on `ncessch`.

9. [Session 9 — Aggregations and Summary Statistics](modules/session_09.md)  
   Compute top schools, ZIP counts, and school size distribution using `groupby`, `agg`, and `pd.cut`.

### Part 4 — Output and Automation

10. [Session 10 — Creating Visualizations](modules/session_10.md)  
    Build a horizontal bar chart and a vertical bar chart with matplotlib. Save them as PNG files.

11. [Session 11 — Generating the Excel Report](modules/session_11.md)  
    Write a five-sheet Excel workbook with `pandas.ExcelWriter` and embed the chart images with `openpyxl`.

12. [Session 12 — The Automated Pipeline](modules/session_12.md)  
    Wire all modules together in `main.py` using `argparse`. Run the full pipeline end-to-end.

### Part 5 — Optional

13. [Session 13 — Introduction to Unit Testing](modules/session_13.md) *(optional)*  
    Write and run `pytest` tests for the transform and report modules.

---

## Resources

- *Automate the Boring Stuff with Python*, 3rd Ed. — reference book for this workshop (free online with GSU credentials via O'Reilly)
- [Python Environment Setup Guide](https://github.com/GSU-Analytics/python_guides/wiki/Python-Environment-Setup)
- [Conda cheat sheet](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf)
- [Git cheat sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [pandas documentation](https://pandas.pydata.org/docs/)
