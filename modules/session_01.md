# Session 1 — The Problem + Tooling Overview

## Introduction

Every month, someone on your team opens SQL Developer, runs an enrollment query, downloads the results, pulls school directory data from the Urban Institute website, pastes everything into Excel, writes formulas, and manually builds a report. It takes two or more hours and introduces errors every time.

This workshop replaces that process with a single Python command. By the end of the twelve sessions, you will have built the tool yourself, from scratch, one piece at a time.

This first session is an orientation. You will see the finished tool run live, understand what each piece of the stack does, and learn how the workshop is organized.

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

## The Tool Stack

This workshop uses four tools. Each one has a specific job; none of them overlap.

### Python

Python is the programming language. It is what reads data, transforms it, and writes the output files. You do not need to install Python separately — it comes bundled with Miniconda (below).

### Miniconda (conda)

Miniconda is an environment manager. It lets you create isolated environments — a named set of packages at specific versions — so that this project's dependencies do not interfere with anything else on your computer.

Every project in this workshop runs inside the `student-report` conda environment, which is defined in `environment.yml`. Creating the environment from that file guarantees that every participant runs the exact same version of every package.

> **Mac note:** conda works the same on Mac. The commands are identical; you will use Terminal instead of Command Prompt.

### Git

Git is version control. It records every change you make to your code, so you can see what you changed, when, and why — and undo it if something breaks.

In this workshop, you will use Git to:
- Get your own copy of the workshop code (fork + clone)
- Save your work as you go (commit)
- Keep your copy up to date if the workshop repo changes (pull)

### Visual Studio Code (VS Code)

VS Code is the code editor. It is where you will read and write Python files. It has a built-in terminal so you can run commands without switching windows, and it integrates with both conda (to select the right Python interpreter) and Git (to see what you have changed).

### How They Fit Together

```
Write code       Run code          Track changes
in VS Code  →  conda env runs it  →  git records it
```

VS Code is the surface you work on. Conda provides the Python environment that executes your code. Git saves a history of your work. These three tools are the foundation of professional Python development — not just for this workshop.

---

## Workshop Roadmap

| Session | Topic | What you'll build |
|---|---|---|
| 1 | The problem + tooling overview | (this session — observation) |
| 2 | Environment setup | Conda environment, VS Code, first Git commit |
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

Sessions 4 and 5 require a VPN connection to the GSU network.

---

## How to Follow Along

All workshop code lives in a single GitHub repository. You will work in your own fork — a personal copy of the repo tied to your GitHub account. Changes you make stay in your fork and do not affect anyone else's copy.

### Step 1 — Create a GitHub account

If you do not already have one, go to [github.com](https://github.com), click **Sign Up**, and follow the instructions.

### Step 2 — Fork the workshop repo

1. Go to the workshop repository on GitHub: `https://github.com/GSU-Analytics/automating-analytics-workshop`
2. Click the **Fork** button in the upper right.
3. Accept the defaults and click **Create fork**.

Your fork will be at: `https://github.com/YOUR-USERNAME/automating-analytics-workshop`

You will clone your fork to your computer in Session 2.

### Step 3 — Confirm your tools are installed

Before Session 2, verify that the following are installed on your machine. You should have received setup instructions prior to the workshop.

**Windows:** Open Command Prompt (`Win + R`, type `cmd`, press Enter) and run:

```
conda --version
git --version
```

Both commands should print a version number with no errors. If either fails, bring your laptop to Session 2 and your instructor will help you get set up.

**Mac:** Open Terminal and run the same two commands.

---

## Additional Resources

- [Miniconda installation guide](https://docs.conda.io/projects/miniconda/en/latest/miniconda-other-installer-links.html)
- [Git download](https://git-scm.com/downloads)
- [VS Code download](https://code.visualstudio.com/download)
- [Conda cheat sheet](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf)
- [Git cheat sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- *Automate the Boring Stuff with Python*, 3rd Ed. — reference book for this workshop
