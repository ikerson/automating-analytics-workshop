# Session 6 Exercise — Calling the Education Data API
#
# Task:
#   1. Create an EducationDataAPI instance
#   2. Call ccd_directory for the year 2018 with fips='36,34'
#   3. Print result.count — how many schools are returned?
#   4. Convert to a DataFrame with .to_df()
#   5. Print .head() and .info()
#   6. Print the list of column names
#
# Run from the repo root:
#   python exercises/session_06_exercise.py

from educationdata import EducationDataAPI

# 1. Create an API instance
api = EducationDataAPI()

# TODO: Call ccd_directory for 2018 — note: fips must be a string, not a list
result = api.ccd_directory(2018, fips="___")

# 3. How many schools are returned?
print(result.count)

# TODO: Convert to a DataFrame
df = ___.to_df()

# 5. Inspect the results
df.___()
print()
df.info()
print()

# TODO: Print the list of column names
print(df.columns.tolist())
print("Done.")
