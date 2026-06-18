# Session 11 Exercise — Working with API Results
#
# Task:
#   1. Create an EducationDataAPI instance and call ccd_directory(2019, fips='36,34')
#   2. Convert to a DataFrame with .to_df()
#   3. Select this subset of columns:
#      ['ncessch', 'school_name', 'city_location', 'state_location', 'school_level', 'enrollment']
#   4. Filter to middle schools only: rows where school_level == 2
#   5. Print how many middle schools remain
#   6. Save the filtered result to exercises/data/middle_schools_2019_filtered.csv (no index)
#
# Run from the repo root:
#   python exercises/session_11_exercise.py

from pathlib import Path
from educationdata import EducationDataAPI

COLUMNS = ['ncessch', 'school_name', 'city_location', 'state_location', 'school_level', 'enrollment']

# TODO: Call ccd_directory for 2019 — note: fips must be a string, not a list
api = EducationDataAPI()
result = api.ccd_directory(2019, fips="___")

# 2. Convert to a DataFrame
df = result.to_df()

# 3. Select the column subset defined above
df = df[COLUMNS].copy()

# TODO: Filter to middle schools (school_level == 2)
df = df[df["school_level"] == ___]

print(f"Middle schools: {len(df)}")

# TODO: Save to exercises/data/middle_schools_2019_filtered.csv — no row index
df.to_csv(Path("exercises") / "data" / "___", index=False)
print("Done.")
