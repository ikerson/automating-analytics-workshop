import os
from pathlib import Path
import oracledb
import pandas as pd
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

_USER = os.getenv("DB_USER")
_PASSWORD = os.getenv("DB_PASSWORD")
_DSN = os.getenv("DB_DSN")

ENROLLMENT_QUERY = """
    SELECT
        s.STUDENT_ID,
        s.FIRST_NAME,
        s.LAST_NAME,
        s.ZIP,
        z.CITY,
        z.STATE,
        c.DESCRIPTION  AS COURSE_NAME,
        c.COST,
        e.ENROLL_DATE,
        e.FINAL_GRADE
    FROM student s
    JOIN zipcode    z ON s.ZIP        = z.ZIP
    JOIN enrollment e ON s.STUDENT_ID = e.STUDENT_ID
    JOIN section  sec ON e.SECTION_ID = sec.SECTION_ID
    JOIN course     c ON sec.COURSE_NO = c.COURSE_NO
"""


def get_enrollment():
    with oracledb.connect(user=_USER, password=_PASSWORD, dsn=_DSN) as conn:
        df = pd.read_sql(ENROLLMENT_QUERY, conn)
    df.columns = df.columns.str.lower()
    return df
