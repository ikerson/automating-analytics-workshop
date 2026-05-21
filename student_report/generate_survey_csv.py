"""
One-time script — run by the workshop author, not participants.
Produces student_report/data/survey_middle_schools.csv, which is then
committed to the repo as static "survey" data.

Requires: VPN connected to GSU network.
"""
import os
import random
import re
from pathlib import Path

import oracledb
import pandas as pd
from dotenv import load_dotenv
from educationdata import EducationDataAPI

load_dotenv(Path(__file__).parent / ".env")

_USER = os.getenv("DB_USER")
_PASSWORD = os.getenv("DB_PASSWORD")
_DSN = "ec2-54-91-230-172.compute-1.amazonaws.com:1521/XEPDB1"

STUDENT_QUERY = """
    SELECT s.student_id, s.zip AS zip_code, z.city, z.state
    FROM student s JOIN zipcode z ON s.zip = z.zip
    WHERE z.state IN ('NY', 'NJ')
"""


def is_plausible_middle_school(name):
    name_upper = str(name).upper()
    bad_patterns = [
        r'^PS \d+', r'^P\.S\. \d+', r'^P\.S\.\d+',
        r'^HS \d+', r'^H\.S\. \d+',
        r'ELEMENTARY',
        r'EARLY CHILDHOOD',
        r'PRIMARY',
        r'\bHIGH SCHOOL\b',
        r'HIGH SCH\b',
        r'\bHS\b',
    ]
    for pat in bad_patterns:
        if re.search(pat, name_upper):
            return False
    return True


def main():
    random.seed(42)

    print("Connecting to Oracle...")
    with oracledb.connect(user=_USER, password=_PASSWORD, dsn=_DSN) as conn:
        students = pd.read_sql(STUDENT_QUERY, conn)
    students.columns = students.columns.str.lower()
    print(f"  {len(students)} NY/NJ students")

    student_zips = set(students['zip_code'].astype(str).str.zfill(5))

    print("Fetching CCD directory (NY + NJ)...")
    api = EducationDataAPI()
    result = api.ccd_directory(2019, fips='36,34')
    ccd = result.to_df()
    print(f"  {len(ccd)} school records before filtering")

    ccd['zip_mailing'] = ccd['zip_mailing'].astype(str).str.split('.').str[0].str.zfill(5)
    ccd = ccd[ccd['school_level'].isin([2, 4])].copy()
    ccd = ccd[ccd['zip_mailing'].isin(student_zips)].copy()
    ccd = ccd[ccd['school_name'].apply(is_plausible_middle_school)].copy()
    print(f"  {len(ccd)} plausible middle schools in student ZIPs")

    schools_by_zip = ccd.groupby('zip_mailing')[['school_name', 'ncessch']].apply(
        lambda g: g.to_dict('records')
    ).to_dict()

    rows = []
    for _, row in students.iterrows():
        student_zip = str(row['zip_code']).zfill(5)
        choices = schools_by_zip.get(student_zip, [])
        if choices:
            school = random.choice(choices)
            ncessch = str(school['ncessch']).split('.')[0]
            rows.append({
                'student_id': int(row['student_id']),
                'middle_school_name': school['school_name'],
                'ncessch': ncessch,
            })
        else:
            rows.append({
                'student_id': int(row['student_id']),
                'middle_school_name': '',
                'ncessch': '',
            })

    survey_df = pd.DataFrame(rows)
    survey_df['middle_school_name'] = survey_df['middle_school_name'].replace('', pd.NA)
    survey_df['ncessch'] = survey_df['ncessch'].replace('', pd.NA)

    out_path = Path(__file__).parent / "data" / "survey_middle_schools.csv"
    out_path.parent.mkdir(exist_ok=True)
    survey_df.to_csv(out_path, index=False)
    print(f"\nWrote {len(survey_df)} rows to {out_path}")
    print(f"  {survey_df['middle_school_name'].notna().sum()} students matched a school")
    print(f"  {survey_df['middle_school_name'].isna().sum()} students had no match (will appear as NaN)")


if __name__ == "__main__":
    main()
