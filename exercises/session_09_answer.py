# Session 9 Exercise — Working with Database Results (Answer)
#
# Run from the repo root:
#   python exercises/session_09_answer.py
#
# NOTE: VPN required — the Oracle server is only reachable on the GSU network.

from pathlib import Path
from dotenv import load_dotenv
from lightoracle import LightOracleConnection

load_dotenv(Path('student_report') / '.env')
conn = LightOracleConnection()
df = conn.execute_query("SELECT * FROM course")
df.columns = df.columns.str.lower()
df = df[df['cost'] > 1000]
df.to_csv(Path('exercises') / 'data' / 'courses_over_1000.csv', index=False)
print(f"Courses with cost > 1000: {len(df)}")
print("Done.")
