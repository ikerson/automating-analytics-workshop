# student_report

Automates a middle school outreach report by pulling student enrollment from the Oracle training database, loading a survey of students' former middle schools, and enriching it with school profile data from the Urban Institute Education Data Portal — producing a merged CSV, two charts, and an Excel workbook from a single command.

## Quickstart

> **VPN required** — connect to the GSU VPN before running.

```bash
# 1. create and activate the environment (first time only)
conda env create -f environment.yml
conda activate student-report

# 2. add your database credentials (one time only)
cp .env.example .env
# open .env and fill in DB_USER and DB_PASSWORD

# 3. run the pipeline
python main.py --year 2019 --output reports/
```

Outputs written to `reports/`:
- `merged.csv` — one row per student with school profile columns
- `top_middle_schools.png` — horizontal bar chart, top 10 schools by student count
- `school_size_distribution.png` — bar chart of students by school size bucket
- `student_report.xlsx` — five sheets: Student Data, Top 10 Schools, By ZIP, By School Size, Charts

## Data Flow

```
Oracle EC2                    survey CSV                Urban Institute API
(STUDENT schema)         data/survey_middle_schools.csv  (CCD directory)
      │                              │                          │
   db.py                        read_csv()                   api.py
      │                              │                          │
  enrollment_df                 survey_df                   school_df
  (one row per                  student_id                  (NY + NJ,
  student × course)             middle_school_name          fips='36,34')
                                ncessch
      │                              │                          │
      └──────────── transform.py ────┴──────────────────────────┘
                          │
             1. deduplicate enrollment → one row per student
             2. merge students → survey on student_id
             3. merge result → CCD on ncessch
             4. assign school_size bucket (enrollment column)
             5. summarize: top 10 schools, ZIP counts, city counts, size dist.
                          │
                      report.py
               ┌──────────┴──────────┐
           charts (.png)        Excel workbook
           - top 10 schools     - Student Data
           - school size dist.  - Top 10 Schools
                                - By ZIP
                                - By School Size
                                - Charts
```

## Project Structure

```
student_report/
├── environment.yml         # conda environment (all dependencies including pytest)
├── .env.example            # credential template — copy to .env and fill in
├── .env                    # your credentials (gitignored, never committed)
├── db.py                   # Oracle query → DataFrame (loads .env)
├── api.py                  # Education Data API (NY + NJ) → DataFrame
├── transform.py            # deduplicate students, 3-way merge, aggregations
├── report.py               # charts and Excel output
├── main.py                 # CLI entry point (argparse)
├── data/
│   └── survey_middle_schools.csv  # student → middle school survey data
├── tests/                  # pytest unit tests (transform + report)
└── reports/                # generated outputs (gitignored)
```
