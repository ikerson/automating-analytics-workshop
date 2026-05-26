# Session 6 Exercise — Calling the Education Data API (Answer)
#
# Run from the repo root:
#   python exercises/session_06_answer.py

from educationdata import EducationDataAPI

api = EducationDataAPI()
result = api.ccd_directory(2018, fips='36,34')
print(result.count)
df = result.to_df()
print(df.head())
print()
df.info()
print()
print(df.columns.tolist())
print("Done.")
