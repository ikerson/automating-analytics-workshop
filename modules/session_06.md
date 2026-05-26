# Session 6 — Calling a Web API

## Introduction

Session 5 finished the database side of the pipeline — `db.py` can now return the full enrollment DataFrame. This session starts the API side: we look at what a web API is, make a raw HTTP request to see the structure, then use the `urban-education-data` package to call the Urban Institute's CCD school directory and inspect what comes back. The result is `api.py` v1 — exploration code that confirms we can reach the API and understand the data. Session 7 will refactor it into a reusable function.

Reference: *Automate the Boring Stuff with Python*, Chapter 12 (Making HTTP Requests)

---

## Setting Up

Open VS Code, activate your conda environment in the terminal, and create a new file at `student_report/api.py`. You will build this file step by step during the code-along.

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

## What Is an API?

In the manual workflow, someone visits a website, finds the right download link, and saves the file. A **web API** (Application Programming Interface) is a way for programs to request the same data programmatically — no browser, no clicking, no manual download.

An API exposes one or more **endpoints**: specific URLs that return data in a structured format. You send an HTTP GET request (the same kind of request a browser sends when you type a URL) and the server responds with data, usually formatted as **JSON**.

**JSON** (JavaScript Object Notation) is a text format for structured data. It looks like a Python dictionary:

```json
{
  "ncessch": 360007702472,
  "school_name": "PS 1 The Bergen",
  "city_location": "New York",
  "state_location": "NY",
  "enrollment": 312
}
```

Each school in the CCD directory is one JSON object. The API returns a list of these objects, one per school.

---

## Making a Raw HTTP Request

The `requests` library is the standard Python tool for making HTTP requests. It is installed automatically as a dependency of the `urban-education-data` package in your conda environment.

Add this to `api.py` and run it:

```python
import requests

url = 'https://educationdata.urban.org/api/v1/schools/ccd/directory/2019/?fips=36&per_page=1'
response = requests.get(url)
print(response.status_code)
print(response.json())
```

Run from the repo root:

```bash
python student_report/api.py
```

You should see `200` (HTTP OK) followed by a JSON object. The `.json()` method parses the response body into a Python dictionary. The structure will look like:

```
{
  'count': 1740,
  'next': 'https://educationdata.urban.org/api/v1/...',
  'previous': None,
  'results': [{ ... one school record ... }]
}
```

The `count` field tells you how many total records match the query (1,740 New York schools in 2019). The `results` list contains the actual records — only one here because we asked for `per_page=1`. Getting all 1,740 records would require paginating through each page of results.

Delete this exploration code. The `urban-education-data` package handles pagination for you — you never need to page through results manually.

---

## The urban-education-data Package

The `urban-education-data` package is a Python client for the Urban Institute Education Data Portal, built and maintained by GSU Analytics. It is already installed in your conda environment via `environment.yml`.

It wraps the raw HTTP calls and automatic pagination into a single method call:

```python
from educationdata import EducationDataAPI

api = EducationDataAPI()
result = api.ccd_directory(2019, fips='36,34')
```

`fips='36,34'` requests schools in both New York (36) and New Jersey (34). The result is an `EducationDataResult` object — not yet a DataFrame. To get a DataFrame, call `.to_df()`:

```python
df = result.to_df()
```

The package fetches all pages automatically. For NY and NJ middle schools in 2019, that is several thousand records — the call may take a few seconds.

> **Important:** `fips='36,34'` must be a comma-separated **string**. Passing a Python list (`fips=[36, 34]`) returns an HTTP 400 error. This is a quirk of how the API parses the parameter.

---

## Building api.py v1

### Calling the API

Replace the contents of `api.py` with:

```python
from educationdata import EducationDataAPI

api = EducationDataAPI()
result = api.ccd_directory(2019, fips='36,34')
print(result.count)
```

`result.count` is the total number of records returned — useful for a quick sanity check before pulling everything into a DataFrame.

Run it:

```bash
python student_report/api.py
```

You should see a number in the thousands. This is the total count of NY and NJ schools matching the CCD directory for 2019.

### Converting to a DataFrame

Now convert the result and inspect it:

```python
from educationdata import EducationDataAPI

api = EducationDataAPI()
result = api.ccd_directory(2019, fips='36,34')
print(result.count)

df = result.to_df()
print(df.head())
print()
df.info()
```

Run again. After a short pause for pagination, you will see the first five rows and a column summary. The DataFrame has many columns — over 50. The next session will narrow it to the 9 columns the pipeline actually uses.

### Exploring the columns

Add `.describe()` and a column list to get a better picture:

```python
from educationdata import EducationDataAPI

api = EducationDataAPI()
result = api.ccd_directory(2019, fips='36,34')
print(result.count)

df = result.to_df()
print(df.head())
print()
df.info()
print()
print(df.describe())
print()
print(df.columns.tolist())
```

Run again. The column list will be long. Note the columns the pipeline cares about: `ncessch`, `school_name`, `zip_mailing`, `city_location`, `state_location`, `school_level`, `enrollment`, `lowest_grade_offered`, `highest_grade_offered`.

Also note that `ncessch` and `zip_mailing` appear as floats — `360007702472.0`, `10001.0`. These are IDs that should be strings. `transform.py` will normalize them in Session 8.

---

## api.py v1 — Complete File

Here is the complete `api.py` v1:

```python
from educationdata import EducationDataAPI

api = EducationDataAPI()
result = api.ccd_directory(2019, fips='36,34')
print(result.count)

df = result.to_df()
print(df.head())
print()
df.info()
print()
print(df.describe())
print()
print(df.columns.tolist())
```

In Session 7 we will:

1. Define a `CCD_COLUMNS` list with the 9 columns the pipeline needs
2. Wrap the API call in a `get_school_data(year)` function
3. Return only the selected columns
4. Remove the top-level print statements so `api.py` is safe to import from `main.py`

---

## Practice Exercise

> Optional enrichment — complete during the session if time allows, or finish independently on your fork.

### Your Task

Call the CCD directory API for the year **2018** instead of 2019.

1. Create an `EducationDataAPI` instance
2. Call `ccd_directory` for 2018 with `fips='36,34'`
3. Print `result.count` — how many schools are returned?
4. Convert to a DataFrame with `.to_df()`
5. Print `.head()` and `.info()`
6. Print the list of column names

Run from the repo root:

```
python exercises/session_06_exercise.py
```

## Additional Resources

- [EducationDataAPI — GSU-Analytics/EducationDataAPI](https://github.com/GSU-Analytics/EducationDataAPI)
- [Urban Institute Education Data Portal](https://educationdata.urban.org/)
- [requests documentation](https://requests.readthedocs.io/)
- *Automate the Boring Stuff with Python*, Chapter 12 — Downloading Files from the Web
