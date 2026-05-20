# Automating Data Analytics with Python — Workshop Plan

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
├── environment.yml       # conda environment
├── README.md
├── config.py             # DB credentials, API base URL
├── main.py               # CLI entry point (argparse)
├── db.py                 # Oracle queries → DataFrame
├── api.py                # Education Data API calls → DataFrame
├── transform.py          # merge + aggregate
└── report.py             # charts + Excel output
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
- Reading credentials from `config.py` (never hardcode)
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

- **PyPI name:** `urban-education-data` — **Install within conda environment:**
  ```bash
  pip install "git+https://github.com/GSU-Analytics/EducationDataAPI.git[df]"
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

1. **Credentials handling** ✓ — Shared `student`/`learn` account (Service: `XEPDB1`). All participants use the same login; `config.py` holds one set of credentials.
2. **ZIP code join** ✓ — The ZIPCODE table is the Oracle SQL by Example training schema centered on the NY metro area (123 NY ZIPs, 74 NJ, 1 GA). API filter changed from `fips=13` (Georgia) to `fips=36` (New York) so the join produces real matches.
3. **EducationDataAPI install** ✓ — `pip install "git+https://github.com/GSU-Analytics/EducationDataAPI.git[df]"` inside the conda environment. Repo is public; no PyPI publish required for the workshop.
4. **Git workflow** ✓ — Participants push to their own forks of the workshop template repo.
5. **Assessment/exercises** ✓ — Follow-along only. No per-session exercises.
