# Session 9 Exercise — Oracle Connection (Answer)
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
df = conn.execute_query("SELECT * FROM zipcode FETCH FIRST 10 ROWS ONLY")
print(df)
print("Done.")
