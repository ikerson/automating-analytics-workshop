# Session 7 Exercise — Working with API Results
#
# Task:
#   1. Create an EducationDataAPI instance and call ccd_directory(2019, fips='36,34')
#   2. Convert to a DataFrame with .to_df()
#   3. Select this subset of columns:
#      ['ncessch', 'school_name', 'city_location', 'state_location', 'school_level', 'enrollment']
#   4. Filter to middle schools only: rows where school_level == 2
#   5. Print how many middle schools remain
#   6. Save the filtered result to exercises/data/middle_schools_2019.csv (no index)
#
# Run from the repo root:
#   python exercises/session_07_exercise.py

from pathlib import Path
from educationdata import EducationDataAPI

COLUMNS = ['ncessch', 'school_name', 'city_location', 'state_location', 'school_level', 'enrollment']

# TODO: Create an EducationDataAPI instance
# Hint: api = EducationDataAPI()


# TODO: Call ccd_directory for 2019 with fips='36,34'
# Hint: result = api.ccd_directory(2019, fips='36,34')


# TODO: Convert to a DataFrame
# Hint: df = result.to_df()


# TODO: Select the COLUMNS subset
# Hint: df = df[COLUMNS].copy()


# TODO: Filter to middle schools (school_level == 2)
# Hint: df = df[df['school_level'] == 2]


# TODO: Print how many middle schools remain
# Hint: print(f"Middle schools: {len(df)}")


# TODO: Save to exercises/data/middle_schools_2019.csv (index=False)
# Hint: df.to_csv(Path('exercises') / 'data' / 'middle_schools_2019.csv', index=False)


print("Done.")
