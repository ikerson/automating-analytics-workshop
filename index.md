# Preface {.unnumbered}

Welcome to *Automating Data Analytics with Python*, a twelve-session workshop for GSU analysts.

This workshop replaces a time-consuming manual reporting workflow — running SQL queries, downloading spreadsheets, and assembling charts and tables in Excel — with a single Python command:

```
python main.py --year 2019 --output reports/
```

By the end of the twelve core sessions, you will have built a working Python package from scratch that connects to an Oracle database, calls a public web API, merges and summarizes the data, and produces two charts and a five-sheet Excel workbook automatically.

## How This Book Is Organized

The workshop is structured in two phases.

**Phase 1 (Sessions 3–7)** — three CSV files are pre-committed to the repo, representing data that someone on your team would have exported by hand. You will build the full pipeline that transforms them and produces the report. The payoff — charts, Excel, a merged dataset — comes first.

**Phase 2 (Sessions 8–11)** — you automate where those CSV files come from by connecting directly to the Oracle database and calling the Urban Institute Education Data API.

**Session 12** wires all four modules together into a single command-line entry point. The code you wrote in Phase 1 does not change — it is exactly what the automated pipeline calls.

The **Exercises** section at the end of this book mirrors Sessions 3–11. Each page states the task and the command to run the starter script. Exercises are optional enrichment — complete them during the session if time allows, or finish independently on your fork.

## Prerequisites

No prior Python experience is required. You will need:

- A Windows computer (the setup guide in Session 0 covers Windows only)
- A free GitHub account
- Access to the GSU network for Sessions 8 and 9 (on-campus WiFi is sufficient; VPN is required only if working off campus)

## Source Materials

This workshop references [*Automate the Boring Stuff with Python*, 3rd Edition](https://automatetheboringstuff.com/), by Al Sweigart. The full text is free online and also available through O'Reilly with GSU credentials.
