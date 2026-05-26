# Session 4 — Connecting to the Database

## Introduction

Sessions 1–3 gave us the tools and showed how to load the static survey CSV. Now we need the real enrollment data, which lives in an Oracle relational database on a GSU server. This session builds `db.py` v1 — a script that connects to Oracle, runs a query, and returns a pandas DataFrame using credentials stored safely outside the code.

Reference: Prior session — Session 3

> **VPN required.** The Oracle server is only reachable on the GSU network. Connect to the VPN before starting the code-along and before running the practice exercise.

---

## Setting Up

Open VS Code, activate your conda environment, and create a new file at `student_report/db.py`. You will build this file step by step during the code-along.

**Windows (CMD or Git Bash):**

```
conda activate student-report
```

**Mac:**

```
conda activate student-report
```

Confirm `(student-report)` appears in your terminal prompt before continuing.

---

## The Oracle Database

The workshop uses an Oracle database running on a GSU EC2 server. It holds five tables that together describe student enrollments:

| Table | Key columns |
|---|---|
| `student` | `STUDENT_ID`, `FIRST_NAME`, `LAST_NAME`, `ZIP` |
| `zipcode` | `ZIP`, `CITY`, `STATE` |
| `course` | `COURSE_NO`, `DESCRIPTION`, `COST` |
| `section` | `SECTION_ID`, `COURSE_NO` |
| `enrollment` | `STUDENT_ID`, `SECTION_ID`, `ENROLL_DATE`, `FINAL_GRADE` |

The database uses the **Oracle SQL by Example** schema (Rischert). Public synonyms are configured, so you query `student` directly — not `student.student`.

In later sessions (`db.py` v2, Session 5) you will join all five tables in a single query. Today, we start with a single table to verify the connection works.

---

## Why Credentials Never Go in Code

Before writing any Python, we need to talk about passwords. The instinct is to write something like this:

```python
conn = connect(user="student02", password="abc123", ...)
```

**Never do this.** The moment that file touches Git, the password is in the commit history — recoverable forever, even if you delete the line later. Credentials committed to a shared or public repo have caused real data breaches.

The standard solution is a `.env` file: a plain text file of `KEY=VALUE` pairs that lives only on your machine and is never committed.

---

## Setting Up .env

The repo already has `student_report/.env.example` — a committed template that shows the structure without real values:

```
ORACLE_USER=student02
ORACLE_PASSWORD=your_password_here
ORACLE_DSN=ec2-54-91-230-172.compute-1.amazonaws.com:1521/XEPDB1
```

Copy it to create your local credentials file:

```bash
cp student_report/.env.example student_report/.env
```

Open `student_report/.env` in VS Code and replace `your_password_here` with the password your instructor gave you. Leave `ORACLE_DSN` and `ORACLE_LIB_DIR` as they are — the DSN is the server address (not a secret), and `ORACLE_LIB_DIR` stays blank because we use thin mode, which needs no Oracle client installation.

Verify the file is gitignored:

```bash
cat .gitignore
```

You should see `student_report/.env` listed. That entry means Git will never stage this file, even if you run `git add .`.

---

## Building db.py

### Imports and credential loading

Open `student_report/db.py` and add the imports:

```python
from pathlib import Path
from dotenv import load_dotenv
from lightoracle import LightOracleConnection
```

`python-dotenv` reads the `.env` file and puts its contents into the environment so Python can access them. `lightoracle` is a lightweight Oracle driver wrapper — it reads the `ORACLE_*` variables automatically and returns query results as a DataFrame.

Now load the credentials:

```python
load_dotenv(Path(__file__).parent / ".env")
```

`Path(__file__).parent` always resolves to the directory that contains `db.py` — in this case, `student_report/`. This path is correct no matter which directory you run the script from.

### Connecting

Add the connection:

```python
conn = LightOracleConnection()
conn.test_connection()
```

`LightOracleConnection()` with no arguments reads `ORACLE_USER`, `ORACLE_PASSWORD`, and `ORACLE_DSN` from the environment. `test_connection()` opens a cursor and confirms the connection is alive.

Run the file:

```bash
python student_report/db.py
```

You should see:

```
Connection test successful. Cursor object: <oracledb.Cursor object at 0x...>
```

If you see `ValueError: Oracle user is required`, confirm that `student_report/.env` exists and uses `ORACLE_USER`, not the old `DB_USER` key name. If you get a network error or timeout, check that your VPN is active.

### Running your first query

`execute_query()` accepts any SQL string and returns a pandas DataFrame — the same object we worked with in Session 3.

Add this to `db.py`:

```python
df = conn.execute_query("SELECT * FROM student FETCH FIRST 5 ROWS ONLY")
print(df)
print(df.info())
```

`FETCH FIRST 5 ROWS ONLY` is Oracle's row-limiting syntax. It is equivalent to `LIMIT 5` in PostgreSQL or MySQL.

Run it again:

```bash
python student_report/db.py
```

You will see five rows from the `student` table followed by a column summary. Notice that the column names come back in uppercase (`STUDENT_ID`, `FIRST_NAME`, ...). We will normalize those to lowercase in Session 5 when we build the `get_enrollment()` function.

---

## db.py — What We've Built

Here is the complete `db.py` v1:

```python
from pathlib import Path
from dotenv import load_dotenv
from lightoracle import LightOracleConnection

load_dotenv(Path(__file__).parent / ".env")

conn = LightOracleConnection()
conn.test_connection()

df = conn.execute_query("SELECT * FROM student FETCH FIRST 5 ROWS ONLY")
print(df)
print(df.info())
```

In Session 5 we will:

1. Replace the single-table query with a five-table enrollment JOIN
2. Wrap everything in a `get_enrollment()` function
3. Normalize column names to lowercase with `.str.lower()`
4. Remove the top-level print statements so `db.py` is safe to import from `main.py`

---

## Practice Exercise

> Optional enrichment — complete during the session if time allows, or finish independently on your fork.
>
> **VPN required.**

### Your Task

1. Load `student_report/.env`
2. Connect to Oracle using `LightOracleConnection`
3. Query the first 10 rows of the `zipcode` table
4. Print the result

Run from the repo root:

```
python exercises/session_04_exercise.py
```

## Additional Resources

- [lightoracle — GSU-Analytics/lightoracle](https://github.com/GSU-Analytics/lightoracle)
- [python-dotenv documentation](https://saurabh-kumar.com/python-dotenv/)
- [GSU Oracle SQL Training](https://github.com/GSU-Analytics/oracle-sql-training) — SQL reference for the workshop schema
