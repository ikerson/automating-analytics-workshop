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

# TODO: Create an EducationDataAPI instance
# Hint: api = EducationDataAPI()


# TODO: Call ccd_directory for 2018 with fips='36,34'
# Note: fips must be a string — fips=[36, 34] returns HTTP 400
# Hint: result = api.ccd_directory(2018, fips='36,34')


# TODO: Print result.count


# TODO: Convert to a DataFrame
# Hint: df = result.to_df()


# TODO: Print .head() and .info()


# TODO: Print the list of column names
# Hint: print(df.columns.tolist())


print("Done.")


# ---------------------------------------------------------------------------
# Answer — uncomment to check your work
# ---------------------------------------------------------------------------

# from educationdata import EducationDataAPI
#
# api = EducationDataAPI()
# result = api.ccd_directory(2018, fips='36,34')
# print(result.count)
# df = result.to_df()
# print(df.head())
# print()
# df.info()
# print()
# print(df.columns.tolist())
# print("Done.")
