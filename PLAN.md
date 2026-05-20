# Automating Data Analytics with Python — Workshop Plan

## Status (updated 2026-05-20)

| Item | Status |
|---|---|
| Session outline (12 sessions) | complete |
| Oracle EC2 server provisioned | complete — `ec2-54-91-230-172.compute-1.amazonaws.com`, accounts `student02`–`student20` verified |
| `student_report/` package scaffolded | complete — all 7 files written, `reports/` directory with `.gitkeep` |
| Implementation guide in PLAN.md | complete — full code + build sequence added |
| End-to-end pipeline verified | **pending** — run `python main.py` on VPN to confirm Oracle connection, API response columns, ZIP join match rate |
| Session 1 demo ready | **pending** — blocked on pipeline verification |
| Workshop template repo (GitHub) | not started |
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

> Every month, our office runs an enrollment summary from SQL Developer and downloads New York school district data from the Urban Institute's Education Data Portal. We combine them in Excel, compute aggregates, and paste charts into a report. It takes 2+ hours and introduces errors every time.

We will replace this with a single command:

```bash
python main.py --year 2019 --state 36 --output reports/
```

**Automated outputs:**
- A merged CSV (Oracle enrollment + Education Data API school data, joined on ZIP code)
- 2–3 saved charts (enrollment by course, student home-area school demographics)
- An Excel summary workbook

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
- Call `api.ccd_directory(2019, fips=36)` — New York school districts; call `.to_df()` on the result
- *ATBS reference*: Chapter 12 (web scraping / HTTP intro)

**Session 7 — Working with API Results**
- API JSON → `pandas.DataFrame`
- Exploring, filtering, selecting relevant columns
- Saving to CSV
- Brief discussion: what changes if the API is different?

---

### Part 3 — Combining and Transforming Data (Sessions 8–9)

**Session 8 — Merging the Two Sources**
- The join key: student ZIP → school district ZIP
- `pandas.merge()` — inner, left; inspect unmatched rows
- Cleaning mismatches (type coercion, leading zeros on ZIP)
- Write merged result to CSV

**Session 9 — Aggregations and Summary Statistics**
- `groupby()` + `agg()` — enrollment counts, averages
- Add a calculated column (e.g., percent of total)
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
