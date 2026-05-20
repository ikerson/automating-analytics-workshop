# student_report

Automates the monthly student enrollment report by pulling data from the Oracle training database and the Urban Institute Education Data Portal, merging them on ZIP code, and producing a merged CSV, two charts, and an Excel workbook — all from a single command.

## Quickstart

> **VPN required** — connect to the GSU VPN before running.

```bash
# 1. create and activate the environment (first time only)
conda env create -f environment.yml
conda activate student-report

# 2. add your database credentials (one time only)
cp student_report/.env.example student_report/.env
# open student_report/.env and fill in your DB_USER, DB_PASSWORD, and DB_DSN address

# 3. run the pipeline
python main.py --year 2019 --state 36 --output reports/
```

Outputs written to `reports/`:
- `merged.csv` — Oracle enrollment joined with NY school data
- `enrollment_by_course.png` — bar chart of students per course
- `students_by_school_area.png` — horizontal bar chart, top 10 schools by ZIP match
- `student_report.xlsx` — three data sheets + embedded charts

## Project Structure

```
student_report/
├── environment.yml   # conda environment (all dependencies)
├── .env.example      # credential template — copy to .env and fill in
├── .env              # your credentials (gitignored, never committed)
├── db.py             # Oracle query → DataFrame (loads .env)
├── api.py            # Education Data API call → DataFrame
├── transform.py      # merge on ZIP + aggregations
├── report.py         # charts and Excel output
├── main.py           # CLI entry point (argparse)
└── reports/          # generated outputs (gitignored)
```
