# Automating Data Analytics with Python — Workshop Plan

## Status (updated 2026-05-21)

| Item | Status |
|---|---|
| Session outline (12 sessions) | complete |
| Oracle EC2 server provisioned | complete — `ec2-54-91-230-172.compute-1.amazonaws.com`, accounts `student02`–`student20` verified |
| `student_report/` package scaffolded | complete — `.env`/`python-dotenv` for credentials, `student02` read-only account, `urban-education-data` install fixed |
| Implementation guide in PLAN.md | complete — full code + build sequence added |
| Workshop template repo (GitHub) | complete — https://github.com/GSU-Analytics/automating-analytics-workshop (private) |
| Refactor to middle school outreach story | complete (2026-05-21) — `api.py`, `transform.py`, `report.py`, `main.py` rewritten; `generate_survey_csv.py` added |
| Survey CSV generated and committed | **pending** — run `python student_report/generate_survey_csv.py` on VPN, then commit `student_report/data/survey_middle_schools.csv` |
| End-to-end pipeline verified | complete (2026-05-21) — 165 students, 118 school matches, 5-sheet Excel + 2 charts confirmed |
| Session 1 demo ready | **pending** — pipeline verified; prep demo script/talking points |
| Participant environment tested (Windows) | not started |

## Workshop at a Glance

| | |
|---|---|
| **Audience** | GSU analysts, beginners and staff |
| **Duration** | 12 × 1-hour sessions (flexible delivery) |
| **Tools** | conda, git, Python 3, VS Code |
| **Key packages** | `oracledb`, `requests`, `pandas`, `matplotlib`, `openpyxl` |
| **Database** | Oracle EC2 server, STUDENT schema (existing) |
| **API** | Urban Institute Education Data Portal via `urban-education-data` (GSU-Analytics/EducationDataAPI) |
| **Reference book** | *Automate the Boring Stuff with Python*, 3rd Ed. (+ workbook) |

---

## The Scenario Being Automated

> Every month, our office runs an enrollment summary from SQL Developer, pulls school directory data from the Urban Institute's Education Data Portal for New York and New Jersey, and merges it with survey data on where our students attended middle school — all in Excel. We compute aggregates and paste charts into a report. It takes 2+ hours and introduces errors every time.

We will replace this with a single command:

```bash
python main.py --year 2019 --output reports/
```

**Automated outputs:**
- A merged CSV (Oracle students + survey → CCD school profile, one row per student)
- 2 saved charts (top 10 middle schools by student count, school size distribution)
- An Excel workbook with 5 sheets for outreach targeting

---

## Package Structure (Minimal)

```
student_report/
├── environment.yml   # conda environment
├── README.md
├── .env.example      # credential template — copy to .env and fill in
├── .env              # your credentials (gitignored, never committed)
├── main.py           # CLI entry point (argparse)
├── db.py             # Oracle queries → DataFrame (loads .env)
├── api.py            # Education Data API calls → DataFrame
├── transform.py      # merge + aggregate
└── report.py         # charts + Excel output
```

One file, one job. No classes. Functions only where they reduce repetition.

---

## Session-by-Session Outline

### Part 1 — Why and How (Sessions 1–3)

**Session 1 — The Problem We're Solving**
- Side-by-side: the manual workflow vs. what we'll build
- Live demo of the finished package running on the command line
- Workshop roadmap, repo setup with `git clone`
- *ATBS reference*: Chapter 1 (Python basics motivation)

**Session 2 — Setting Up the Environment**
- Install conda, create environment from `environment.yml`
- Activate environment, confirm packages
- VS Code + Python extension orientation
- `git` basics: `status`, `add`, `commit`
- *ATBS reference*: Appendix B (running programs)

**Session 3 — Python Essentials for Analysts**
- Variables, strings, numbers, lists, dicts — only what we'll use
- Defining and calling functions
- Reading from a file with `open()` and `csv`
- *ATBS reference*: Chapters 4–5 (lists, dicts)

---

### Part 2 — Getting Data (Sessions 4–7)

**Session 4 — Connecting to the Database**
- What `oracledb` does; install in environment
- Why credentials never go in code — `.env` file + `python-dotenv`; `.gitignore` keeps it out of git
- Connect to the Oracle EC2 server, run a SELECT, see raw rows
- *ATBS reference*: N/A (custom content — reference SQL training docs)

**Session 5 — Working with Database Results**
- `cursor.fetchall()` → list of tuples → `pandas.DataFrame`
- `.head()`, `.info()`, `.describe()` — understanding your data
- Filtering and selecting columns
- Saving to CSV

**Session 6 — Calling a Web API**
- What is an API? What is JSON?
- `requests.get()`, `.status_code`, `.json()`
- Explore the `urban-education-data` package (`EducationDataAPI`, GSU-Analytics)
- Call `api.ccd_directory(2019, fips='36,34')` — NY and NJ middle school directory; call `.to_df()` on the result
- *ATBS reference*: Chapter 12 (web scraping / HTTP intro)

**Session 7 — Working with API Results**
- API JSON → `pandas.DataFrame`
- Exploring, filtering, selecting relevant columns (`ncessch`, `school_name`, `zip_mailing`, `enrollment`, etc.)
- Saving to CSV
- Brief discussion: what changes if the API is different?

---

### Part 3 — Combining and Transforming Data (Sessions 8–9)

**Session 8 — Merging the Three Sources**
- The story: admissions wants to target middle schools where current students grew up
- Introduce `data/survey_middle_schools.csv` — simulated survey data linking student IDs to NCES school IDs
- Deduplication: `drop_duplicates(subset=['student_id'])` — one row per student before merging
- Three-way merge: students → survey on `student_id`, then → CCD on `ncessch`
- Inspect unmatched rows (students with no survey match)
- Write merged result to CSV

**Session 9 — Aggregations and Summary Statistics**
- `groupby()` + `agg()` — top schools by student count, ZIP counts
- `pd.cut()` — bucketing school enrollment into Small / Medium / Large
- `observed=True` on categorical groupby (pandas ≥2.0)
- `value_counts()` for quick distributions
- *ATBS reference*: none directly — refer to pandas docs

---

### Part 4 — Output and Automation (Sessions 10–12)

**Session 10 — Creating Visualizations**
- `matplotlib.pyplot` — bar chart, line chart
- Label axes, add a title
- `plt.savefig()` → file (not just display)
- *ATBS reference*: none — matplotlib docs; keep to 2 chart types max

**Session 11 — Generating the Excel Report**
- `pandas.ExcelWriter` + `openpyxl` — write multiple sheets
- One sheet per table: raw merged data, summary aggregates
- Embed saved chart images using `openpyxl`
- Run the full pipeline manually end-to-end

**Session 12 — The Automated Pipeline**
- Wire `db.py`, `api.py`, `transform.py`, `report.py` together in `main.py`
- `argparse`: `--year`, `--state`, `--output` arguments
- Run the full command: `python main.py --year 2019 --state 36 --output reports/`
- Discussion: scheduling with `cron`/Task Scheduler; what's next

---

## Data Flow

```
Oracle EC2                    Urban Institute API
(STUDENT schema)              (Education Data Portal)
      │                               │
   db.py                          api.py
      │                               │
  DataFrame                      DataFrame
      │                               │
      └──────── transform.py ─────────┘
                     │
               merged DataFrame
              (joined on ZIP code)
                     │
              report.py
            ┌────────┴────────┐
        charts (.png)    Excel workbook
```

---

## Reference Resources

### `oracle-student-db` (local)
**Path:** `/Users/ikerson/Library/CloudStorage/OneDrive-GeorgiaStateUniversity/code/oracle-student-db/`

The deployment and provisioning repo for the Oracle EC2 training server used in this workshop.

- **EC2 instance:** `ec2-54-91-230-172.compute-1.amazonaws.com`, Oracle Linux 8, Oracle 21c XE
- **SSH access:** `ssh -i "secrets/oracle-student-db.pem" ec2-user@ec2-54-91-230-172.compute-1.amazonaws.com`
- **Key files:**
  - `README.md` — full EC2 launch + Oracle install + listener config guide
  - `create_student_schema_and_readonly_users_with_audit.sql` — creates `student` schema and numbered read-only accounts (`student02`–`student20`) with random passwords logged to `sys.student_user_audit_log`
  - `grantStudentAccess.sql` — grants SELECT on all STUDENT tables to numbered accounts
  - `createStudentSynonyms.sql` — public synonyms so participants query `course` not `student.course`
  - `secrets/oracle-student-db.pem` — RSA key for SSH
  - `secrets/student_numbered_users.csv` — participant username/password list
- **Management scripts** (`scripts/`): `oracle_connect.py` (connection library), `test_student_access.py` (verify all accounts), `cleanup_keyring.py` (reset stored credentials)
- **VPN required** for all connections

#### User Hierarchy (verified May 2026)

| Account | Role | Service | Purpose |
|---|---|---|---|
| `sys` | SYSDBA | XE (root) | Full DBA — run provisioning scripts here |
| `sys` | SYSDBA | XEPDB1 | PDB-scoped admin — run training scripts here |
| `student` | CONNECT + RESOURCE | XEPDB1 | Schema owner; creates and owns all training tables. **Workshop shared account: `student`/`learn`** ✓ |
| `student02`–`student20` | CONNECT only | XEPDB1 | Read-only SELECT on STUDENT schema via grants + public synonyms. All 19 accounts verified ✓ |

`student01` does not exist — re-run the provisioning script if that account is needed.

**Password policy:** `PASSWORD_LIFE_TIME` set to `UNLIMITED` on the DEFAULT profile in XEPDB1 (fixed May 2026 after ORA-28001 expiration). If accounts expire again in the future, reset via:
```sql
-- SSH in, then:
sqlplus sys/SSAdbadmin2025@localhost:1521/XEPDB1 as sysdba
ALTER USER student IDENTIFIED BY learn ACCOUNT UNLOCK;
-- For numbered accounts: ALTER USER student02 IDENTIFIED BY X9P90XHFKG ACCOUNT UNLOCK;
```

---

### `GSU-Analytics/summer-training` — `sql-interactive-module`
**GitHub:** `https://github.com/GSU-Analytics/summer-training/tree/main/sql-interactive-module`
**Local:** `/Users/ikerson/Library/CloudStorage/OneDrive-GeorgiaStateUniversity/code/summer-training/sql-interactive-module/`

SQL training materials developed for GSU's summer professional development series. Useful as a reference for SQL session pacing and exercise design.

- **`oracle-live-ad-schema/`** — Full documentation of the AD (Academic) schema from Oracle Live SQL, including 15-table ER diagram, column-level descriptions, and sample queries. The schema models students, faculty, courses, departments, enrollment, attendance, and exam results — a good structural reference for the STUDENT schema used in this workshop.
- **`quick-start-guide/`** — Transcript of the LinkedIn Learning "Quick Start Guide to SQL" course, useful as a recommended pre-reading resource for participants with no SQL background.
- **`sql-by-example-book/`** — Reference materials from *Oracle SQL by Example, 4th Edition*.

---

### `GSU-Analytics/summer-training` — `github-module`
**GitHub:** `https://github.com/GSU-Analytics/summer-training/tree/main/github-module`
**Local:** `/Users/ikerson/Library/CloudStorage/OneDrive-GeorgiaStateUniversity/code/summer-training/github-module/`

A complete Git and GitHub curriculum developed for GSU summer training. Directly reusable for Session 2 of this workshop.

- **`README.md`** — Full written curriculum covering: Git/GitHub concepts, installation, basic workflow (clone → add → commit → push), repo structure (README, .gitignore, .gitkeep), collaboration (pull, merge conflicts), and GitHub project management (issues, branches, pull requests, project boards). References *Beginning Git and GitHub* (Tsitoara, 2024).
- **`outlines/`** — Two course outline documents (`Git and GitHub Course Outline (Simplified).docx`, `Git_and_GitHub_Course_Outline.docx`) suitable for adapting into session handouts.
- Estimated duration from source material: **4 hours** (can be condensed to the ~20 minutes needed in Session 2 of this workshop by covering only clone, status, add, commit).

---

### `GSU-Analytics/EducationDataAPI` — `eddata_api`
**GitHub:** `https://github.com/GSU-Analytics/EducationDataAPI` (public)
**Local:** `/Users/ikerson/Library/CloudStorage/OneDrive-GeorgiaStateUniversity/code/eddata_api/`

Python client for the Urban Institute Education Data Portal. Completely redesigned — all phases complete except PyPI publish.

- **Not on PyPI** — install directly from GitHub within the conda environment:
  ```bash
  pip install "urban-education-data[df] @ git+https://github.com/GSU-Analytics/EducationDataAPI.git"
  ```
- **Import and usage (Session 6):**
  ```python
  from educationdata import EducationDataAPI
  api = EducationDataAPI()
  result = api.ccd_directory(2019, fips=36)   # New York school districts
  df = result.to_df()                          # returns pandas DataFrame
  ```
- **Return type:** `EducationDataResult` — call `.to_df()` for DataFrame, `.to_dict()` for list of dicts, `.count` for total record count. Pagination is automatic.
- **Package layout:** `src/educationdata/` — `_client.py` (all endpoint methods), `_result.py` (result object), `_pagination.py` (auto-pagination)
- **Managed with:** `uv` (dev); participants use `pip install` inside their conda env

---

## Decisions

1. **Credentials handling** ✓ — Numbered read-only account (e.g. `student02`, Service: `XEPDB1`). Credentials live in a `.env` file at the repo root (gitignored); `.env.example` is the committed template. `db.py` loads credentials at runtime via `python-dotenv`. The `student` schema-owner account is NOT used — numbered accounts have SELECT-only access.
2. **ZIP code join** ✓ — The ZIPCODE table is the Oracle SQL by Example training schema centered on the NY metro area (123 NY ZIPs, 74 NJ, 1 GA). API filter changed from `fips=13` (Georgia) to `fips=36` (New York) so the join produces real matches.
3. **EducationDataAPI install** ✓ — `pip install "urban-education-data[df] @ git+https://github.com/GSU-Analytics/EducationDataAPI.git"` inside the conda environment. Distribution name is `urban-education-data`; import name is `educationdata`. Not on PyPI — install directly from GitHub.
4. **Git workflow** ✓ — Participants push to their own forks of the workshop template repo.
5. **Assessment/exercises** ✓ — Follow-along only. No per-session exercises.

---

## Final Package — Implementation Guide

The code below is the **finished `student_report/` package** — what gets demoed at the top of Session 1 and what attendees build toward over 12 sessions. All files live at the repo root; the package is not installable, just run directly with `python main.py`.

> **VPN required** — the Oracle EC2 server is only reachable on the GSU VPN.

---

### Oracle Schema Reference

The training database uses the **Oracle SQL by Example** schema (Alice Rischert), installed in the `STUDENT` schema on `XEPDB1`. Public synonyms are configured, so participants query `course` not `student.course`.

| Table | Columns used in workshop |
|---|---|
| `student` | `STUDENT_ID`, `FIRST_NAME`, `LAST_NAME`, `ZIP` |
| `zipcode` | `ZIP`, `CITY`, `STATE` |
| `course` | `COURSE_NO`, `DESCRIPTION` (course title), `COST` |
| `section` | `SECTION_ID`, `COURSE_NO`, `START_DATE_TIME` |
| `enrollment` | `STUDENT_ID`, `SECTION_ID`, `ENROLL_DATE`, `FINAL_GRADE` |

The ZIPCODE table covers the NY metro area (123 NY ZIPs, 74 NJ, 1 GA) — this is why the API state filter is `fips=36` (New York), so the ZIP join produces real matches.

---

### CCD Directory API Columns Used

From `EducationDataAPI().ccd_directory(year, fips=36)` → `.to_df()`:

| Column | Description |
|---|---|
| `ncessch` | NCES school ID |
| `school_name` | School name |
| `zip_mailing` | Mailing ZIP code (join key → `student.ZIP`) |
| `enrollment` | Total school enrollment |
| `city_location` | City |
| `state_location` | State abbreviation |

> **Verify column names** — run `df.columns.tolist()` on a live API response before finalizing. The column `zip_mailing` is standard in CCD directory v2019 but confirm on first run.

---

### `environment.yml`

```yaml
name: student-report
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3.11
  - pip
  - pip:
    - oracledb>=2.0
    - pandas>=2.0
    - matplotlib>=3.7
    - openpyxl>=3.1
    - "urban-education-data[df] @ git+https://github.com/GSU-Analytics/EducationDataAPI.git"
```

Create and activate:
```bash
conda env create -f environment.yml
conda activate student-report
```

---

### `.env.example` (committed) / `.env` (gitignored)

Both files live in `student_report/`.

```
DB_USER=student02
DB_PASSWORD=your_password_here
```

Copy `.env.example` to `.env` and fill in the numbered account credentials from the distributed CSV (`secrets/student_numbered_users.csv` in `oracle-student-db`). The `.env` file is listed in `.gitignore` — passwords never enter git history.

Introduced in **Session 4** as the first security lesson: credentials go in `.env`, not in code.

---

### `db.py`

```python
import os
from pathlib import Path
import oracledb
import pandas as pd
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

_USER = os.getenv("DB_USER")
_PASSWORD = os.getenv("DB_PASSWORD")
_DSN = "ec2-54-91-230-172.compute-1.amazonaws.com:1521/XEPDB1"

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
    with oracledb.connect(user=_USER, password=_PASSWORD, dsn=_DSN) as conn:
        df = pd.read_sql(ENROLLMENT_QUERY, conn)
    df.columns = df.columns.str.lower()
    return df
```

**Notes:**
- `oracledb` runs in thin mode by default (no Oracle Instant Client required).
- `.columns.str.lower()` normalizes Oracle's uppercase column names so they match the lowercase API output.
- Built in **Session 4** (raw connect + cursor) then upgraded in **Session 5** (pd.read_sql).

---

### `api.py`

```python
from educationdata import EducationDataAPI

CCD_COLUMNS = [
    'ncessch', 'school_name', 'zip_mailing',
    'enrollment', 'city_location', 'state_location',
]

def get_school_data(year, state_fips):
    api = EducationDataAPI()
    result = api.ccd_directory(year, fips=state_fips)
    df = result.to_df()
    return df[CCD_COLUMNS].copy()
```

**Notes:**
- `EducationDataAPI()` handles pagination automatically.
- Selecting only `CCD_COLUMNS` keeps the DataFrame manageable (the raw response has ~70 columns).
- Built in **Session 6** (basic call) then refined in **Session 7** (column selection, save to CSV).

---

### `transform.py`

```python
import pandas as pd

def merge_data(enrollment_df, school_df):
    enrollment_df = enrollment_df.copy()
    school_df = school_df.copy()
    enrollment_df['zip'] = enrollment_df['zip'].astype(str).str.zfill(5)
    school_df['zip_mailing'] = school_df['zip_mailing'].astype(str).str.zfill(5)
    return enrollment_df.merge(
        school_df,
        left_on='zip',
        right_on='zip_mailing',
        how='left',
    )

def summarize_by_course(df):
    return (
        df.groupby('course_name')
        .agg(student_count=('student_id', 'count'), avg_cost=('cost', 'mean'))
        .reset_index()
        .sort_values('student_count', ascending=False)
    )

def summarize_by_school(df):
    matched = df.dropna(subset=['school_name'])
    return (
        matched.groupby('school_name')
        .agg(
            student_count=('student_id', 'count'),
            school_enrollment=('enrollment', 'first'),
        )
        .reset_index()
        .sort_values('student_count', ascending=False)
        .head(10)
    )
```

**Notes:**
- `.str.zfill(5)` pads ZIP codes to 5 digits — a common mismatch when one source stores `"07030"` and another stores `7030`.
- `how='left'` keeps all Oracle students; unmatched rows get NaN for school columns (NJ/GA ZIPs).
- `merge_data` built in **Session 8**; `summarize_*` functions built in **Session 9**.

---

### `report.py`

```python
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


def save_enrollment_chart(summary_df, output_dir):
    path = Path(output_dir) / "enrollment_by_course.png"
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(summary_df['course_name'], summary_df['student_count'], color='steelblue')
    ax.set_xlabel("Course")
    ax.set_ylabel("Number of Students")
    ax.set_title("Student Enrollment by Course")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def save_school_chart(school_summary_df, output_dir):
    path = Path(output_dir) / "students_by_school_area.png"
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(
        school_summary_df['school_name'],
        school_summary_df['student_count'],
        color='teal',
    )
    ax.set_xlabel("Number of Students")
    ax.set_title("Students by Nearby School (Top 10 by ZIP Match)")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def save_excel_report(merged_df, course_summary_df, school_summary_df, chart_paths, output_dir):
    from openpyxl import load_workbook
    from openpyxl.drawing.image import Image as XLImage

    path = Path(output_dir) / "student_report.xlsx"
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        merged_df.to_excel(writer, sheet_name='Merged Data', index=False)
        course_summary_df.to_excel(writer, sheet_name='By Course', index=False)
        school_summary_df.to_excel(writer, sheet_name='By School Area', index=False)

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

**Notes:**
- `plt.close()` after each save prevents figure accumulation in memory.
- Charts built in **Session 10**; Excel output (including image embed) built in **Session 11**.

---

### `main.py`

```python
import argparse
from pathlib import Path
from db import get_enrollment
from api import get_school_data
from transform import merge_data, summarize_by_course, summarize_by_school
from report import save_enrollment_chart, save_school_chart, save_excel_report


def main(args):
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    print("Fetching enrollment data from Oracle...")
    enrollment_df = get_enrollment()
    print(f"  {len(enrollment_df)} enrollment records")

    print(f"Fetching school data from API (year={args.year}, state={args.state})...")
    school_df = get_school_data(args.year, args.state)
    print(f"  {len(school_df)} school records")

    print("Merging and summarizing...")
    merged_df = merge_data(enrollment_df, school_df)
    course_summary = summarize_by_course(merged_df)
    school_summary = summarize_by_school(merged_df)

    merged_csv = output / "merged.csv"
    merged_df.to_csv(merged_csv, index=False)
    print(f"  Saved {merged_csv}")

    print("Generating charts...")
    chart1 = save_enrollment_chart(course_summary, output)
    chart2 = save_school_chart(school_summary, output)

    print("Generating Excel report...")
    excel_path = save_excel_report(
        merged_df, course_summary, school_summary,
        [chart1, chart2], output,
    )

    print(f"\nDone. Outputs in {output}/")
    print(f"  {merged_csv.name}")
    print(f"  {chart1.name}")
    print(f"  {chart2.name}")
    print(f"  {excel_path.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate student enrollment and school data report."
    )
    parser.add_argument(
        '--year', type=int, default=2019,
        help='CCD data year (default: 2019)',
    )
    parser.add_argument(
        '--state', type=int, default=36,
        help='State FIPS code (default: 36 = New York)',
    )
    parser.add_argument(
        '--output', type=str, default='reports/',
        help='Output directory (default: reports/)',
    )
    args = parser.parse_args()
    main(args)
```

Built in **Session 12** — the final step that wires everything together.

---

### Build Sequence (Session-by-Session)

Each row shows what gets written in that session. By Session 12 the full package exists.

| Session | Files touched | What gets added |
|---|---|---|
| 1 | — | Live demo of the finished package; no code written |
| 2 | `environment.yml` | Create conda env; activate; confirm packages install |
| 3 | — | Python essentials: variables, strings, lists, dicts, functions |
| 4 | `.env`, `db.py` (v1) | `.env` + `python-dotenv`; `oracledb.connect()`, raw `cursor.execute()`, `fetchall()` → list of tuples |
| 5 | `db.py` (v2) | Upgrade to `pd.read_sql()`; add `get_enrollment()`; save to CSV |
| 6 | `api.py` (v1) | `EducationDataAPI()`, `.ccd_directory()`, `.to_df()`; explore columns |
| 7 | `api.py` (v2) | Column selection via `CCD_COLUMNS`; save to CSV |
| 8 | `transform.py` (v1) | `merge_data()`: ZIP coercion, `pd.merge()`, inspect unmatched rows |
| 9 | `transform.py` (v2) | `summarize_by_course()`, `summarize_by_school()`: `groupby` + `agg` |
| 10 | `report.py` (v1) | `save_enrollment_chart()`, `save_school_chart()`: bar charts + `savefig` |
| 11 | `report.py` (v2) | `save_excel_report()`: `ExcelWriter`, `openpyxl`, embed chart images |
| 12 | `main.py` | `argparse`; import and call all modules; run `python main.py --year 2019 --state 36 --output reports/` |

---

### First Run Checklist

Before the Session 1 demo, verify the full pipeline works:

1. `conda env create -f student_report/environment.yml && conda activate student-report`
2. Copy credentials: `cp student_report/.env.example student_report/.env` — fill in `DB_USER` and `DB_PASSWORD` from `oracle-student-db/secrets/student_numbered_users.csv`
3. Confirm VPN connected to GSU network
4. `python student_report/main.py --year 2019 --state 36 --output student_report/reports/`
5. Verify `student_report/reports/` contains: `merged.csv`, `enrollment_by_course.png`, `students_by_school_area.png`, `student_report.xlsx`
6. Open `student_report.xlsx` and confirm three data sheets + one Charts sheet with both images
6. If `zip_mailing` key error in `api.py`: run `api.ccd_directory(2019, fips=36).to_df().columns.tolist()` and update `CCD_COLUMNS` accordingly

---

## Refactor Plan: Middle School Outreach Analysis

**Status:** Complete (2026-05-21). All code changes implemented. Remaining step: run `generate_survey_csv.py` on VPN and commit the CSV.

### Background and Motivation

The current pipeline joins Oracle enrollment records (student × course) to the CCD school directory on ZIP code. This produces 1,569 rows for ~165 students because each student is enrolled in multiple courses and each ZIP contains many schools — a many-to-many join explosion. The output is confusing and unmotivated.

This refactor replaces that join with a realistic outreach-targeting story:

> **The admissions team wants to start early outreach programs at junior high schools to build interest in the university before students reach high school. They have survey data on which middle schools current college students attended. They want to identify the top schools by student count, and understand the geographic and size profile of those schools, so they can prioritize outreach visits.**

The new pipeline introduces a **CSV bridge file** (`data/survey_middle_schools.csv`) that links Oracle student IDs to CCD middle school names. This file is described as "collected via student survey" — it's realistic simulated data, appropriate for a beginner workshop.

### New Data Flow

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
           - top 10 schools     - Raw Student Data
           - school size dist.  - Middle School Summary
                                - Top 10 Schools
                                - Size Distribution
                                - Charts
```

---

### Step 1 — Generate the Survey CSV (one-time script)

**File to create:** `student_report/generate_survey_csv.py`

This script is run **once** by the workshop author, not by participants. It produces `student_report/data/survey_middle_schools.csv`, which is then committed to the repo as static "survey" data. Participants never run this script — they interact with the CSV as if it were real survey data collected offline.

**What the script does:**

1. Connect to Oracle (using `.env` credentials), query all students in NY or NJ states:
   ```sql
   SELECT s.student_id, s.zip AS zip_code, z.city, z.state
   FROM student s JOIN zipcode z ON s.zip = z.zip
   WHERE z.state IN ('NY', 'NJ')
   ```
   (There is also 1 GA student in the database — exclude them since there are no matching CCD schools nearby.)

2. Normalize Oracle column names with `.columns.str.lower()` (Oracle returns uppercase). Use `s.zip AS zip_code` in the SQL to avoid the `zip` → `zip_code` rename issue that caused a `KeyError` during feasibility testing.

3. Call `EducationDataAPI().ccd_directory(2019, fips='36,34')` — the comma-separated string `'36,34'` fetches both New York (FIPS 36) and New Jersey (FIPS 34) in a single call. This was verified to work during feasibility testing and returns ~3,000+ school records. Call `.to_df()` on the result.

4. Normalize the CCD `zip_mailing` column: `ccd['zip_mailing'] = ccd['zip_mailing'].astype(str).str.split('.').str[0].str.zfill(5)`. This handles the float→string conversion issue (the API sometimes returns ZIP as a float like `10001.0`).

5. Filter CCD to `school_level in [2, 4]`:
   - `school_level == 2` = explicitly middle school
   - `school_level == 4` = charter/other grade span (many NYC charter schools that serve 6–8 fall here)
   - Do NOT include `school_level == 1` (elementary) or `school_level == 3` (high school)

6. Filter CCD to schools whose `zip_mailing` is in the set of student ZIP codes.

7. Apply the name filter (see **Name Filter Specification** section below) to remove schools whose names clearly indicate they are elementary or high schools even if `school_level` says otherwise.

8. For each student, build the list of plausible schools in their ZIP. Randomly assign one school. Use `random.seed(42)` for reproducibility so the CSV is deterministic.

9. Students with no plausible school in their ZIP (there are ~83 of them across ~45 ZIPs) get an empty `middle_school_name` and empty `ncessch`. These nulls are acceptable — they will show up as `NaN` in the merged DataFrame and be dropped/labeled "Unknown" in the analysis.

10. Write output to `student_report/data/survey_middle_schools.csv`.

**Output CSV columns:**
| Column | Type | Description |
|---|---|---|
| `student_id` | int | Oracle STUDENT.STUDENT_ID (join key to Oracle) |
| `middle_school_name` | str | CCD school_name (display only) |
| `ncessch` | str | NCES school ID (join key to CCD — use this, not school_name, to avoid name duplicates) |

**After running this script:** commit `student_report/data/survey_middle_schools.csv` to the repo. Add `student_report/generate_survey_csv.py` to the repo but note in comments that it is a one-time data-generation utility, not part of the workshop pipeline.

**Important:** Create the `student_report/data/` directory and add a `.gitkeep` if it does not already exist.

---

### Name Filter Specification

The feasibility script at `/tmp/check_middle_schools.py` established the initial filter. This refactor **relaxes** it to allow IS ##, MS ##, JHS ##, and MIDDLE-named schools through.

**Keep (do NOT exclude):**
- `IS \d+` / `I.S. \d+` — Intermediate School (IS 71, IS 218, etc.). In the NYC public school system, "IS" = Intermediate School = grades 6–8. These are genuine junior highs.
- `MS \d+` / `M.S. \d+` — Middle School. Self-evidently a middle school.
- `JHS \d+` / `J.H.S. \d+` — Junior High School. Self-evidently a junior high.
- Any name containing `MIDDLE` (e.g., "YOUNG MIDDLE SCHOOL", "BROOKLYN MIDDLE ACADEMY") — the word "middle" is a strong positive signal.
- Ambiguous names like "YOUNG WOMENS LEADERSHIP SCHOOL - ASTORIA" — these pass through because they don't match any exclusion pattern. This is intentional and acceptable for a simulated dataset.

**Exclude (these clearly indicate NOT a middle school):**
- `^PS \d+`, `^P\.S\. \d+`, `^P\.S\.\d+` — Public School numbered (PS 122, PS 6) — almost always elementary
- `^HS \d+`, `^H\.S\. \d+` — High School numbered
- `ELEMENTARY` anywhere in the name
- `EARLY CHILDHOOD` anywhere in the name
- `PRIMARY` anywhere in the name
- `\bHIGH SCHOOL\b` anywhere in the name
- `HIGH SCH\b` anywhere in the name
- `\bHS\b` as a standalone word (avoid false positives: "NHS", "PHYSICS" — use word boundary `\b`)

**Updated Python filter function:**
```python
import re

def is_plausible_middle_school(name):
    name_upper = str(name).upper()
    bad_patterns = [
        r'^PS \d+', r'^P\.S\. \d+', r'^P\.S\.\d+',   # elementary numbered
        r'^HS \d+', r'^H\.S\. \d+',                    # high school numbered
        r'ELEMENTARY',
        r'EARLY CHILDHOOD',
        r'PRIMARY',
        r'\bHIGH SCHOOL\b',
        r'HIGH SCH\b',
        r'\bHS\b',
    ]
    for pat in bad_patterns:
        if re.search(pat, name_upper):
            return False
    return True
```

Note: `IS ##`, `MS ##`, `JHS ##`, and `MIDDLE` are now ALLOWED (their exclusion patterns have been removed from the previous version).

---

### Step 2 — `api.py` Changes

**Goal:** Pull CCD data for both NY and NJ, and expand the columns returned to include school profile fields needed for the analysis.

**Change 1 — Remove `state_fips` parameter, hardcode NY+NJ:**
```python
# OLD
def get_school_data(year, state_fips):
    api = EducationDataAPI()
    result = api.ccd_directory(year, fips=state_fips)

# NEW
def get_school_data(year):
    api = EducationDataAPI()
    result = api.ccd_directory(year, fips='36,34')
```

The `fips='36,34'` string is confirmed to work. Do not use a list — `fips=[36, 34]` returns HTTP 400. The comma-separated string is the correct form.

**Change 2 — Expand `CCD_COLUMNS`:**
```python
CCD_COLUMNS = [
    'ncessch',            # NCES school ID — primary join key to survey CSV
    'school_name',        # display name
    'zip_mailing',        # ZIP code — used for ZIP/city analysis
    'city_location',      # city name — used for city analysis
    'state_location',     # state abbreviation
    'school_level',       # 1=elem, 2=middle, 3=high, 4=other — for reference
    'enrollment',         # total school enrollment — used for size bucketing
    'lowest_grade_offered',   # for display/verification
    'highest_grade_offered',  # for display/verification
]
```

**Verify these column names exist** by running `api.ccd_directory(2019, fips='36,34').to_df().columns.tolist()` on a live response before finalizing. The column names have been stable across CCD API versions but should be confirmed.

---

### Step 3 — `db.py` Changes (minimal)

**Keep the existing `ENROLLMENT_QUERY` and `get_enrollment()` function unchanged.** The multi-table Oracle join (student → zipcode → enrollment → section → course) is the core SQL teaching example for Sessions 4–5 and should not be removed.

The query returns one row per student × course combination (a student enrolled in 2 courses = 2 rows). This is expected and intentional — the deduplication to one row per student now happens in `transform.py` as a deliberate step, which becomes its own teaching moment.

**No changes needed to `db.py`.**

---

### Step 4 — `transform.py` Rewrite

This file changes the most. The old functions (`merge_data`, `summarize_by_course`, `summarize_by_school`) are replaced with new ones that reflect the outreach story.

**New function: `get_students(enrollment_df)`**

Deduplicate the enrollment DataFrame to one row per student, keeping only the student-level columns (not course data):

```python
def get_students(enrollment_df):
    return (
        enrollment_df[['student_id', 'first_name', 'last_name', 'zip', 'city', 'state']]
        .drop_duplicates(subset=['student_id'])
        .copy()
    )
```

**Important:** Use `drop_duplicates(subset=['student_id'])` not just `.drop_duplicates()`. The enrollment query joins to multiple courses, so the same student appears multiple times with different course/grade values — we want exactly one row per student_id.

**New function: `merge_data(students_df, survey_df, school_df)`**

Three-way merge: students → survey → CCD.

```python
def merge_data(students_df, survey_df, school_df):
    students_df = students_df.copy()
    survey_df = survey_df.copy()
    school_df = school_df.copy()

    # Normalize ZIP
    students_df['zip'] = students_df['zip'].astype(str).str.zfill(5)
    school_df['zip_mailing'] = (
        school_df['zip_mailing'].astype(str).str.split('.').str[0].str.zfill(5)
    )
    # Normalize ncessch to string (API may return it as int or float)
    survey_df['ncessch'] = survey_df['ncessch'].astype(str).str.split('.').str[0]
    school_df['ncessch'] = school_df['ncessch'].astype(str).str.split('.').str[0]

    # Step 1: students → survey (left join — keeps students with no survey match)
    merged = students_df.merge(survey_df, on='student_id', how='left')

    # Step 2: merged → school profile (left join — keeps students with no school match)
    merged = merged.merge(school_df, on='ncessch', how='left')

    # Step 3: add school_size bucket
    merged['school_size'] = pd.cut(
        merged['enrollment'],
        bins=[0, 300, 700, float('inf')],
        labels=['Small (<300)', 'Medium (300-700)', 'Large (700+)'],
    )

    return merged
```

**Why normalize ncessch:** The CCD API sometimes returns `ncessch` as a float (e.g., `360007702472.0`). The survey CSV stores it as generated by the script, which may also have the float issue. Both sides must be normalized to plain integer-string before the join or the merge will silently fail (0 matches).

**New function: `summarize_top_schools(merged_df)`**

```python
def summarize_top_schools(merged_df):
    matched = merged_df.dropna(subset=['middle_school_name'])
    return (
        matched.groupby(['middle_school_name', 'city_location', 'zip_mailing', 'school_size'])
        .agg(student_count=('student_id', 'count'), school_enrollment=('enrollment', 'first'))
        .reset_index()
        .sort_values('student_count', ascending=False)
        .head(10)
    )
```

**New function: `summarize_by_zip(merged_df)`**

```python
def summarize_by_zip(merged_df):
    matched = merged_df.dropna(subset=['zip_mailing'])
    return (
        matched.groupby(['zip_mailing', 'city_location'])
        .agg(student_count=('student_id', 'count'))
        .reset_index()
        .sort_values('student_count', ascending=False)
    )
```

**New function: `summarize_by_size(merged_df)`**

```python
def summarize_by_size(merged_df):
    return (
        merged_df.groupby('school_size', observed=True)
        .agg(student_count=('student_id', 'count'))
        .reset_index()
    )
```

Note: `observed=True` is required in pandas ≥2.0 when grouping by a `Categorical` (which `pd.cut` produces). Without it, pandas emits a FutureWarning.

**School size bucket thresholds:**
| Bucket | Enrollment range | Rationale |
|---|---|---|
| Small | < 300 | Smaller community schools, neighborhood-level reach |
| Medium | 300–700 | Typical NYC neighborhood middle school |
| Large | > 700 | Large consolidated or magnet schools |

---

### Step 5 — `report.py` Rewrite

Replace the two old charts and old Excel structure with outreach-focused output.

**New function: `save_top_schools_chart(top_schools_df, output_dir)`**

Horizontal bar chart, top 10 schools by student count. Use school name on Y axis.

```python
def save_top_schools_chart(top_schools_df, output_dir):
    path = Path(output_dir) / "top_middle_schools.png"
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_schools_df['middle_school_name'], top_schools_df['student_count'], color='steelblue')
    ax.set_xlabel("Number of Students")
    ax.set_title("Top 10 Middle Schools by Student Count")
    ax.invert_yaxis()   # largest bar at top
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path
```

**New function: `save_size_chart(size_df, output_dir)`**

Pie or bar chart showing distribution of students across school size buckets. Bar is simpler and more beginner-friendly:

```python
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

**Updated function: `save_excel_report(...)`**

Excel workbook with 5 sheets:
1. **Student Data** — the merged DataFrame (one row per student), all columns
2. **Top 10 Schools** — `top_schools_df`
3. **By ZIP** — `zip_summary_df`
4. **By School Size** — `size_df`
5. **Charts** — embed both chart images

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

---

### Step 6 — `main.py` Changes

**Remove the `--state` argument.** The API now always fetches NY+NJ via `fips='36,34'` hardcoded in `api.py`. Keeping `--state` would be misleading since passing `--state 13` (Georgia) would be ignored. Remove it cleanly.

**Add CSV loading step** between the Oracle fetch and the API fetch:

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

**Important:** Load `survey_df` with `dtype={'student_id': int, 'ncessch': str}`. Without the dtype spec, pandas may read `ncessch` as a float and `student_id` inconsistently, causing silent join failures.

---

### Step 7 — Run `generate_survey_csv.py` and Commit the CSV

After all code changes are in place:

1. Connect to VPN
2. `conda activate student-report`
3. `python student_report/generate_survey_csv.py`
4. Inspect `student_report/data/survey_middle_schools.csv` — verify it has ~240 rows, `student_id` is integer, `ncessch` is a string like `360007702472`, roughly 65% of rows have a non-null `middle_school_name`
5. Commit the CSV as `data/survey_middle_schools.csv`

---

### Expected Output After Refactor

**`reports/merged.csv`:** ~240 rows (one per NY+NJ student). Columns include student_id, name, zip, city, state, middle_school_name, ncessch, city_location, zip_mailing, state_location, school_level, enrollment, school_size, lowest_grade_offered, highest_grade_offered. ~157 rows will have a non-null school; ~83 will be null.

**`reports/top_middle_schools.png`:** Horizontal bar chart, top 10 middle schools by student count.

**`reports/school_size_distribution.png`:** Bar chart, students by school size bucket.

**`reports/student_report.xlsx`:** 5 sheets — Student Data, Top 10 Schools, By ZIP, By School Size, Charts.

**Run command after refactor:**
```bash
python student_report/main.py --year 2019 --output student_report/reports/
```
(Note: `--state` argument has been removed.)

---

### Pitfalls to Avoid

1. **`ncessch` type mismatch** — The CCD API returns `ncessch` as a float-encoded integer (e.g., `360007702472.0`). The survey CSV generation script may or may not cast it. Both sides of the merge must be normalized to a clean string (e.g., `'360007702472'`) using `.astype(str).str.split('.').str[0]`. If the join produces 0 matches, this is almost certainly why.

2. **Oracle uppercase columns** — `pd.read_sql()` returns column names in uppercase (`STUDENT_ID`, `ZIP`, etc.). Always call `.columns.str.lower()` immediately after `pd.read_sql()`. The `db.py` function already does this — do not remove it.

3. **`zip_mailing` as float** — Same issue as `ncessch`. The CCD API returns ZIPs as floats (`10001.0`). Use `.astype(str).str.split('.').str[0].str.zfill(5)`. This normalization must happen in both `generate_survey_csv.py` AND `transform.py`.

4. **`fips` must be a string** — `api.ccd_directory(2019, fips='36,34')` works. `fips=[36, 34]` (a Python list) returns HTTP 400. `fips=36` (integer for just NY) also works. Only the comma-separated multi-state form requires the string type.

5. **`pd.cut` with `observed=True`** — When using `groupby` on a `Categorical` column (output of `pd.cut`), always pass `observed=True` to avoid FutureWarning and suppress empty-category rows in the output.

6. **`drop_duplicates` before survey merge** — The Oracle enrollment query returns one row per student × course. Merging 5 course rows per student × 1 survey row = 5 output rows per student (still an explosion, just smaller). Use `drop_duplicates(subset=['student_id'])` in `get_students()` before any merge.

7. **`generate_survey_csv.py` requires VPN** — The script connects to both Oracle (VPN-gated) and the Education Data API (public). It must be run on the GSU VPN. Once the CSV is committed, the main pipeline only uses the committed file and does not re-call `generate_survey_csv.py`.

8. **Do not change `db.py`** — The multi-table enrollment query is a teaching asset for Sessions 4–5. The deduplication in `get_students()` in `transform.py` is intentional and becomes a teaching moment ("a student can take many courses — we deduplicate before merging with survey data").

9. **Update the session outline** — Sessions 6–9 reference the old ZIP-join story and "school district" framing. Update the scenario description in those sessions to reference the survey CSV and middle school outreach story. The code steps remain the same; only the narrative changes.

10. **Update the scenario paragraph at the top of PLAN.md** — The current scenario says "download New York school district data." After the refactor it should say something like: "pull school directory data for NY and NJ, merge it with a survey of where our students went to middle school, and produce an outreach targeting report."
