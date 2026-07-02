# Session 12 Exercise — Working with API Results (Answer)
#
# Run from the repo root:
#   python exercises/session_12_answer.py

from pathlib import Path
from educationdata import EducationDataAPI

COLUMNS = ['ncessch', 'school_name', 'city_location', 'state_location', 'school_level', 'enrollment']

api = EducationDataAPI()
result = api.ccd_directory(2019, fips='36,34')
df = result.to_df()
df = df[COLUMNS].copy()
df = df[df['school_level'] == 2]
print(f"Middle schools: {len(df)}")
df.to_csv(Path('exercises') / 'data' / 'middle_schools_2019_filtered.csv', index=False)
print("Done.")
