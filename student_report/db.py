# db.py

from pathlib import Path
from dotenv import load_dotenv
from lightoracle import LightOracleConnection

load_dotenv(Path(__file__).parent / ".env")

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
    conn = LightOracleConnection()
    df = conn.execute_query(ENROLLMENT_QUERY)
    df.columns = df.columns.str.lower()
    return df
