# Automating Data Analytics with Python — Workshop Plan

## Status (updated 2026-05-21)

| Item | Status |
|---|---|
| Session outline (13 sessions) | complete |
| Oracle EC2 server provisioned | complete — `ec2-54-91-230-172.compute-1.amazonaws.com`, accounts `student02`–`student20` verified |
| `student_report/` package built and verified | complete (2026-05-21) — 165 students, 118 school matches, 5-sheet Excel + 2 charts confirmed |
| Unit tests | complete (2026-05-21) — 12 tests in `student_report/tests/`; `pytest` added to `environment.yml` |
| Session 1 demo ready | **pending** — prep demo script/talking points |
| Session materials development | not started |
| Participant environment tested (Windows) | not started |

## Workshop at a Glance

| | |
|---|---|
| **Audience** | GSU analysts, beginners and staff |
| **Duration** | 12 × 1-hour sessions + 1 optional session (unit testing) |
| **Tools** | conda, git, Python 3, VS Code |
| **Key packages** | `oracledb`, `pandas`, `matplotlib`, `openpyxl` |
| **Database** | Oracle EC2 server, STUDENT schema |
| **API** | Urban Institute Education Data Portal via `urban-education-data` (GSU-Analytics/EducationDataAPI) |
| **Reference book** | *Automate the Boring Stuff with Python*, 3rd Ed. |

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

## Package Structure

```
student_report/
├── environment.yml         # conda environment (all dependencies including pytest)
├── README.md
├── .env.example            # credential template — copy to .env and fill in
├── .env                    # your credentials (gitignored, never committed)
├── main.py                 # CLI entry point (argparse)
├── db.py                   # Oracle queries → DataFrame (loads .env)
├── api.py                  # Education Data API (NY + NJ) → DataFrame
├── transform.py            # deduplicate students, 3-way merge, aggregations
├── report.py               # charts + Excel output
├── generate_survey_csv.py  # one-time author script (not part of participant pipeline)
├── data/
│   └── survey_middle_schools.csv  # student → middle school survey (simulated)
├── tests/                  # pytest unit tests (transform + report)
└── reports/                # generated outputs (gitignored)

exercises/
├── data/                   # small thematic CSVs (middle school outreach universe)
│   ├── outreach_contacts.csv
│   └── school_survey_2019.csv
├── session_03_exercise.py
├── session_04_exercise.py
├── session_05_exercise.py
├── session_06_exercise.py
├── session_07_exercise.py
├── session_08_exercise.py
├── session_09_exercise.py
├── session_10_exercise.py
└── session_11_exercise.py
```

One file, one job. No classes. Functions only where they reduce repetition.

---

## Session-by-Session Outline

### Part 1 — Why, How, and Tooling (Sessions 1–3)

**Session 1 — The Problem + Tooling Overview**
- Side-by-side: the manual workflow vs. what we'll build
- Live demo of the finished package running on the command line
- Introduce the tool stack: VS Code (editor), conda (environment manager), git (version control), Python (language) — what each one does and how they fit together
- Workshop roadmap; how to follow along

**Session 2 — Setting Up the Environment (Hands-On)**
- Install conda; create and activate the environment from `environment.yml`
- VS Code: open the repo folder, install the Python extension, select the conda interpreter, run a script from the integrated terminal
- Git hands-on: `clone`, `status`, `add`, `commit` — track changes from day one
- How it all connects: write code in VS Code → conda env runs it → git records it

**Session 3 — Pandas and Working with Data**
- What is pandas? Series vs. DataFrame — the core mental model
- `pd.read_csv()` — load `data/survey_middle_schools.csv` and inspect it
- `.head()`, `.info()`, `.describe()` — understanding a new dataset
- Selecting columns, filtering rows
- Writing functions: why wrap code in a function; apply it to a simple data transformation
- *This session bridges tooling to data work — students use all of these concepts in every session that follows*

---

### Part 2 — Getting Data (Sessions 4–7)

**Session 4 — Connecting to the Database**
- What `oracledb` does; already installed in the conda environment
- Why credentials never go in code — `.env` file + `python-dotenv`; `.gitignore` keeps it out of git
- Connect to the Oracle EC2 server, run a SELECT, see raw rows
- *ATBS reference*: N/A (custom content — reference SQL training docs)

**Session 5 — Working with Database Results**
- `cursor.fetchall()` → list of tuples → `pandas.DataFrame`
- Upgrade to `pd.read_sql()` — cleaner and returns a DataFrame directly
- `.head()`, `.info()`, `.describe()` on Oracle data; normalize column names with `.str.lower()`
- Filtering, selecting columns; save to CSV

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

---

### Part 4 — Output and Automation (Sessions 10–12)

**Session 10 — Creating Visualizations**
- `matplotlib.pyplot` — horizontal bar chart (`barh`), vertical bar chart (`bar`)
- Label axes, add a title; `ax.invert_yaxis()` so the largest bar is at the top
- `plt.savefig()` → file (not just display); `plt.close()` to free memory
- *Keep to 2 chart types max*

**Session 11 — Generating the Excel Report**
- `pandas.ExcelWriter` + `openpyxl` — write multiple sheets
- Five sheets: Student Data, Top 10 Schools, By ZIP, By School Size, Charts
- Embed saved chart images using `openpyxl`
- Run the full pipeline manually end-to-end

**Session 12 — The Automated Pipeline**
- Wire `db.py`, `api.py`, `transform.py`, `report.py` together in `main.py`
- Load `data/survey_middle_schools.csv` with `pd.read_csv()`
- `argparse`: `--year`, `--output` arguments
- Run the full command: `python main.py --year 2019 --output reports/`
- Discussion: scheduling with `cron`/Task Scheduler; what's next

---

### Part 5 — Optional (Session 13)

**Session 13 — Introduction to Unit Testing** *(skip if time does not allow)*
- Why test? Catching bugs before they reach the data
- `pytest` basics: test functions, assertions, `tmp_path` fixture
- Walk through `tests/test_transform.py` — testing `get_students()` and `merge_data()`
- Run: `pytest student_report/tests/ -v`

---

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

---

## Module Documentation Structure

Each session is a standalone markdown file. The repo README links all modules and provides a minimal intro. There is no Q&A section (not relevant for this workshop).

### Per-module template

```
# [Session N] — [Session Title]

## Introduction
2–3 sentences: problem this session solves, how it fits the pipeline.
Reference: ATBS chapter | Prior session.

## Code-Along
### [Subsection]
Narrative + annotated code blocks building toward the session deliverable.

## Practice Exercise
> Optional enrichment — complete during the session if time allows,
> or finish independently on your fork.

### Your Task
2–4 concrete bullet points.
Run from the command line: python exercises/session_NN_exercise.py

### Answer
Complete working solution (at the bottom of the same exercise script).

## Additional Resources
- ATBS chapter
- Relevant package docs
```

### Exercise script format

Each `exercises/session_NN_exercise.py` is runnable as delivered. `TODO:` comments mark what participants fill in. The file structure, imports, and print statements are pre-written. Thematic data files (middle school outreach universe) live in `exercises/data/`.

### Exercise-per-session map

| Session | Topic | Exercise task | Data / source |
|---|---|---|---|
| 1 | Demo + overview | — none — | — |
| 2 | Environment setup | — none — | — |
| 3 | pandas basics | Load contacts CSV, select columns, drop rows missing phone, save cleaned file | `exercises/data/outreach_contacts.csv` |
| 4 | Oracle connect | Connect to Oracle, SELECT from `zipcode`, print first 10 rows | Oracle EC2 (VPN required) |
| 5 | pd.read_sql | Query `course` table, normalize column names, filter subset, save CSV | Oracle EC2 (VPN required) |
| 6 | API intro | Call API for a different year (2018), check row count, inspect columns | Urban Institute API |
| 7 | API columns | Select different columns, filter to middle schools (`school_level == 2`), save CSV | Urban Institute API |
| 8 | Merging | Merge two outreach CSVs on `student_id`, inspect unmatched rows, save result | `exercises/data/` |
| 9 | Aggregations | `groupby` school size bucket, average enrollment per bucket, `value_counts` on city | `exercises/data/` |
| 10 | Charts | Horizontal bar chart of top 5 contact schools, save as PNG | `exercises/data/` |
| 11 | Excel output | Write two DataFrames to separate sheets in one Excel file | `exercises/data/` |
| 12 | Pipeline | Run `python student_report/main.py --year 2019 --output student_report/reports/` | — |

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

### `GSU-Analytics/summer-training` — `github-module`
**GitHub:** `https://github.com/GSU-Analytics/summer-training/tree/main/github-module`
**Local:** `/Users/ikerson/Library/CloudStorage/OneDrive-GeorgiaStateUniversity/code/summer-training/github-module/`

A complete Git and GitHub curriculum developed for GSU summer training. Directly reusable for Session 2 of this workshop.

- **`README.md`** — Full written curriculum covering: Git/GitHub concepts, installation, basic workflow (clone → add → commit → push), repo structure (README, .gitignore, .gitkeep), collaboration (pull, merge conflicts), and GitHub project management (issues, branches, pull requests, project boards). References *Beginning Git and GitHub* (Tsitoara, 2024).
- **`outlines/`** — Two course outline documents suitable for adapting into session handouts.
- Estimated duration from source material: **4 hours** (condense to ~20 minutes for Session 2 by covering only clone, status, add, commit).

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
  result = api.ccd_directory(2019, fips='36,34')   # NY + NJ middle schools
  df = result.to_df()                               # returns pandas DataFrame
  ```
- **Return type:** `EducationDataResult` — call `.to_df()` for DataFrame, `.to_dict()` for list of dicts, `.count` for total record count. Pagination is automatic.
- **Important:** `fips='36,34'` (comma-separated string) works. `fips=[36, 34]` (Python list) returns HTTP 400.
- **Package layout:** `src/educationdata/` — `_client.py` (all endpoint methods), `_result.py` (result object), `_pagination.py` (auto-pagination)

---

### `GSU-Analytics/cs_concepts-1`
**Local:** `/Users/ikerson/Library/CloudStorage/OneDrive-GeorgiaStateUniversity/code/cs_concepts-1/`

Previous GSU workshop: *Computer Science Concepts in Python for Data Analysts*. Useful as a structural and pacing reference.

- **`section3-dev-env/`** — Windows-focused setup guide for conda, VS Code, and the Python extension. Reference this for Session 2 when testing participant environments on Windows.
- **`section6-api-project-all/`** — Contains a stepwise build model (`step01/` through `step07/`) where the project is built incrementally one file at a time. Good reference for how to pace a multi-session build project.
- **`cs_concepts.yaml`** — Conda environment used in that workshop; useful comparison for our `environment.yml`.

---

### `GSU-Analytics/lightoracle`
**GitHub:** `https://github.com/GSU-Analytics/lightoracle` (public)
**Local:** `/Users/ikerson/Library/CloudStorage/OneDrive-GeorgiaStateUniversity/code/lightoracle/`

Lightweight Oracle database connection wrapper built for GSU Analytics projects. **Not used in this workshop** — participants connect via raw `oracledb` for teaching purposes. Useful as a reference for how to abstract Oracle connections into a reusable package.

- **`lightoracle/`** — Core package; wraps `oracledb` with `.env`/config file credential loading and a simple connection interface.
- **`example.py`** — Shows the intended usage pattern: `from lightoracle import OracleConnection`.
- **`config_example.py`** — Shows how credentials are loaded from a config file or environment variables.
- Install: `pip install git+https://github.com/GSU-Analytics/lightoracle.git`

---

### `GSU-Analytics/oracle-sql-training`
**Local:** `/Users/ikerson/Library/CloudStorage/OneDrive-GeorgiaStateUniversity/code/oracle-sql-training/`

Prior GSU SQL training course. Reference for module structure and exercise design.

- **Module format:** flat markdown files (one per topic) linked from a minimal README. Each module has: Introduction, Explanation (subsections + code blocks + tables), Exercises (simple + complex problems), Additional Resources, Answers. No Q&A section in this workshop.
- **Exercise model:** exercises are open-ended SQL problems with no starter code. This workshop adapts the model to Python: each exercise is a pre-written starter script with `TODO:` comments that participants run from the command line.
- **Quarto / gh-pages:** the repo publishes docs via Quarto books on a `gh-pages` branch. This workshop will adopt the same publishing approach at the end of the development process — not a current priority.

---

## Decisions

1. **Credentials handling** ✓ — Numbered read-only account (e.g. `student02`, Service: `XEPDB1`). Credentials live in a `.env` file (gitignored); `.env.example` is the committed template. `db.py` loads credentials at runtime via `python-dotenv`. The `student` schema-owner account is NOT used — numbered accounts have SELECT-only access.
2. **Data join strategy** ✓ — Three-way merge: Oracle enrollment (deduplicated to one row per student) → survey CSV on `student_id` → CCD school directory on `ncessch`. The survey CSV (`data/survey_middle_schools.csv`) is simulated data generated by `generate_survey_csv.py` (author-only, VPN required) and committed to the repo as static data. Participants treat it as a real survey file.
3. **EducationDataAPI install** ✓ — `pip install "urban-education-data[df] @ git+https://github.com/GSU-Analytics/EducationDataAPI.git"` inside the conda environment. Distribution name is `urban-education-data`; import name is `educationdata`. Not on PyPI — install directly from GitHub.
4. **Git workflow** ✓ — Participants push to their own forks of the workshop template repo.
5. **Assessment/exercises** ✓ — Follow-along is primary. Exercises are optional enrichment. Pre-written starter scripts and thematic data files are committed to `exercises/` in the repo root. Participants fork the repo and run exercise scripts from the command line. Sessions 4 and 5 exercises require VPN. Sessions 1, 2, and 12 have no exercise script.

---

## Oracle Schema Reference

The training database uses the **Oracle SQL by Example** schema (Alice Rischert), installed in the `STUDENT` schema on `XEPDB1`. Public synonyms are configured, so participants query `course` not `student.course`.

| Table | Columns used in workshop |
|---|---|
| `student` | `STUDENT_ID`, `FIRST_NAME`, `LAST_NAME`, `ZIP` |
| `zipcode` | `ZIP`, `CITY`, `STATE` |
| `course` | `COURSE_NO`, `DESCRIPTION` (course title), `COST` |
| `section` | `SECTION_ID`, `COURSE_NO`, `START_DATE_TIME` |
| `enrollment` | `STUDENT_ID`, `SECTION_ID`, `ENROLL_DATE`, `FINAL_GRADE` |

The ZIPCODE table covers the NY metro area (123 NY ZIPs, 74 NJ, 1 GA). The enrollment query returns one row per student × course — `get_students()` in `transform.py` deduplicates to one row per student before merging.

---

## CCD Directory API Columns Used

From `EducationDataAPI().ccd_directory(year, fips='36,34')` → `.to_df()`:

| Column | Description |
|---|---|
| `ncessch` | NCES school ID — primary join key to survey CSV |
| `school_name` | School name (display only) |
| `zip_mailing` | Mailing ZIP code |
| `city_location` | City name |
| `state_location` | State abbreviation |
| `school_level` | 1=elem, 2=middle, 3=high, 4=other |
| `enrollment` | Total school enrollment — used for size bucketing |
| `lowest_grade_offered` | For display/verification |
| `highest_grade_offered` | For display/verification |

**Note:** The API returns `ncessch` and `zip_mailing` as floats (e.g., `360007702472.0`, `10001.0`). Both are normalized to clean strings in `transform.py` using `.astype(str).str.split('.').str[0]`.

---

## Build Sequence

Each row shows what gets written in that session. By Session 12 the full package exists.

| Session | Files touched | What gets added |
|---|---|---|
| 1 | — | Live demo of the finished package; tooling overview (VS Code, conda, git, Python — what each does) |
| 2 | `environment.yml` | Hands-on: `conda env create` + activate; VS Code interpreter setup; `git clone/status/add/commit` |
| 3 | `data/survey_middle_schools.csv` (read only) | `pd.read_csv()`, Series, DataFrame, `.head()`, `.info()`, `.describe()`, column selection, filtering; writing functions |
| 4 | `.env`, `db.py` (v1) | `.env` + `python-dotenv`; `oracledb.connect()`, raw `cursor.execute()`, `fetchall()` → list of tuples |
| 5 | `db.py` (v2) | Upgrade to `pd.read_sql()`; add `get_enrollment()`; `.str.lower()` normalization; save to CSV |
| 6 | `api.py` (v1) | `EducationDataAPI()`, `.ccd_directory(year, fips='36,34')`, `.to_df()`; explore columns |
| 7 | `api.py` (v2) | Column selection via `CCD_COLUMNS`; save to CSV |
| 8 | `transform.py` (v1) | `get_students()` dedup; three-way merge: students → survey on `student_id` → CCD on `ncessch`; inspect unmatched rows |
| 9 | `transform.py` (v2) | `summarize_top_schools()`, `summarize_by_zip()`, `summarize_by_size()`: `groupby`, `agg`, `pd.cut()` |
| 10 | `report.py` (v1) | `save_top_schools_chart()`, `save_size_chart()`: `barh`, `bar`, `savefig()`, `plt.close()` |
| 11 | `report.py` (v2) | `save_excel_report()`: `ExcelWriter`, `openpyxl`, 5 sheets, embed chart images |
| 12 | `main.py` | `argparse`; load survey CSV; import and call all modules; run `python main.py --year 2019 --output reports/` |
| 13 *(optional)* | `tests/` | `pytest`; `test_transform.py`, `test_report.py`; `sys.path` setup; run `pytest student_report/tests/ -v` |

---

## First Run Checklist

Before the Session 1 demo, verify the full pipeline works:

1. `conda env create -f student_report/environment.yml && conda activate student-report`
2. Copy credentials: `cp student_report/.env.example student_report/.env` — fill in `DB_USER` and `DB_PASSWORD` from `oracle-student-db/secrets/student_numbered_users.csv`
3. Confirm VPN connected to GSU network
4. `python student_report/main.py --year 2019 --output student_report/reports/`
5. Verify `student_report/reports/` contains: `merged.csv`, `top_middle_schools.png`, `school_size_distribution.png`, `student_report.xlsx`
6. Open `student_report.xlsx` and confirm 5 sheets: Student Data, Top 10 Schools, By ZIP, By School Size, Charts
