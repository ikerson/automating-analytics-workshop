# Session 1 — The Problem + Tooling Overview

## Introduction

Every month, someone on your team opens SQL Developer, runs an enrollment query, downloads the results, pulls school directory data from the Urban Institute website, pastes everything into Excel, writes formulas, and manually builds a report. It takes two or more hours and introduces errors every time.

This workshop replaces that process with a single Python command. By the end of the twelve sessions, you will have built the tool yourself, from scratch, one piece at a time.

This first session is an orientation. You will see the finished tool run live, understand what each piece of the stack does, and learn how the workshop is organized.

---

## Teaching Approach

### Honest Expectations

This workshop is designed for people with no previous Python or coding experience — you do not need any prior background to participate. That said, beginner-friendly does not mean easy.

We are building a real-world automated data pipeline. That is a complex process with many moving parts: a database, a web API, data transformation logic, charts, and an Excel report — all wired together and run from a single command. You will encounter concepts that take time to absorb, and some things will not click on the first pass. That is expected and completely normal.

The learning curve is steep. The payoff is high.

### How This Workshop Teaches

Sessions follow a code-along format: the instructor writes code, you follow on your own machine. Each session adds one file or one function to the project. By Session 12, you will have built the complete pipeline yourself.

A few things to keep in mind:

- **Sessions build on each other.** Missing a session or falling behind makes the next one harder. Attendance and keeping pace matter more in a cumulative build than in a standalone class.
- **We are moving quickly.** This workshop introduces many tools and concepts — conda, Git, Oracle, REST APIs, pandas, matplotlib, openpyxl — without going deep on any of them. The goal is exposure and a working mental model, not mastery.
- **Practice exercises** at the end of most sessions give you a chance to apply what was covered independently. They are optional enrichment.
- **You will not understand everything the first time.** That is normal. The materials are designed to be returned to.

### What We Do Not Expect

We do not expect you to be able to code a complete analytics pipeline from scratch when this workshop ends. We do not expect you to memorize syntax, commands, or package names.

### What We Do Hope

- You pick up at least a few techniques that are immediately useful in your day-to-day work.
- You develop a working mental model of what an automated pipeline looks like and what each component does.
- You feel comfortable returning to the workshop materials as a reference when you want to build something new.
- You get comfortable directing an AI coding agent. The context you build in this workshop gives you enough vocabulary to ask better questions, validate the output, and catch mistakes.

### Support and Resources

All session modules, sample code, and documentation are published on the [workshop GitHub page](https://github.com/GSU-Analytics/automating-analytics-workshop) and as a Quarto book. They are yours to read, search, and reference forever.

Office hours are held directly after every session. The workshop Teams channel is open for questions and troubleshooting between sessions. There are no bad questions. Ask during sessions, in Teams, or at office hours.

---

## The Problem: A Report That Takes All Day

Here is the current workflow for producing the middle school outreach report:

| Step | Tool | Time | Pain point |
|---|---|---|---|
| Export enrollment data | SQL Developer | 15–30 min | Manual query, copy-paste to Excel |
| Download school directory | Urban Institute website | 15–20 min | Manual search, CSV export |
| Load survey data | Excel | 10 min | Separate file, manual import |
| Merge and clean | Excel (VLOOKUP / Power Query) | 30–45 min | Formula errors, mismatched IDs |
| Build aggregations | Excel (pivot tables) | 20–30 min | Rebuilding the same pivots every month |
| Create charts | Excel | 15–20 min | Manual resizing, copy-paste into report |
| Save and distribute | Email | 5–10 min | Version confusion |

Total: **2+ hours every time**, before any fixes for errors discovered later.

The problems stack up:
- A typo in a formula silently produces wrong numbers.
- Adding a new data source means rebuilding the merge by hand.
- There is no record of what changed between runs.
- No one else can reproduce the report from scratch without asking.

---

## What We'll Build

By Session 12 you will run one command:

```
python main.py --year 2019 --output reports/
```

And in under a minute, the `reports/` folder will contain:

| Output | Description |
|---|---|
| `merged.csv` | One row per student, with their former middle school's name, location, and enrollment profile |
| `top_middle_schools.png` | Horizontal bar chart — top 10 schools by student count |
| `school_size_distribution.png` | Bar chart — students grouped by school size (Small / Medium / Large) |
| `student_report.xlsx` | Five-sheet Excel workbook: Student Data, Top 10 Schools, By ZIP, By School Size, Charts |

The same command runs every month. The output is identical in structure every time. If the data changes, the report reflects it automatically.

---

## Live Demo

Your instructor will run `python main.py --year 2019 --output reports/` live. As you watch, notice:

1. **The terminal output** — each step prints what it is doing and how many records it found. No silent failures.
2. **The output folder** — four files appear in `reports/` within about a minute.
3. **The Excel workbook** — open `student_report.xlsx` and click through the five sheets. Everything the manual process produced, in one file.
4. **The source code** — the instructor will briefly scroll through the five Python files that make this work. You are going to write all of this yourself.

You do not need to follow along on your own computer today. This session is observation only.

---

## Workshop Roadmap

| Session | Topic | What you'll build |
|---|---|---|
| 0 *(before session 1)* | Before you begin | Miniconda, Git, VS Code installed; GitHub account; repo forked |
| 1 | The problem + tooling overview | (this session — observation) |
| 2 | Clone, build, and run | Clone your fork, create the conda environment, first commit and push |
| 3 | Pandas and working with data | Load and explore the survey CSV |
| 4 | Connecting to the database | `db.py` v1 — raw Oracle connection |
| 5 | Working with database results | `db.py` v2 — `pd.read_sql()`, save to CSV |
| 6 | Calling a web API | `api.py` v1 — fetch school directory |
| 7 | Working with API results | `api.py` v2 — select columns, save to CSV |
| 8 | Merging the three sources | `transform.py` v1 — three-way merge |
| 9 | Aggregations and summaries | `transform.py` v2 — groupby, pd.cut |
| 10 | Creating visualizations | `report.py` v1 — two charts |
| 11 | Generating the Excel report | `report.py` v2 — five-sheet workbook |
| 12 | The automated pipeline | `main.py` — wire it all together |
| 13 *(optional)* | Unit testing | `tests/` — pytest basics |

Sessions 4 and 5 require a connection to the GSU network. On campus, GSU WiFi is sufficient. Off campus, connect to the GSU VPN first.

---

## Additional Resources

- [Conda cheat sheet](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf)
- [Git cheat sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- *Automate the Boring Stuff with Python*, 3rd Ed. — reference book for this workshop
