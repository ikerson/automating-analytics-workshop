# Session 9 Exercise — Oracle Connection
#
# Task:
#   1. Load student_report/.env
#   2. Connect to Oracle using LightOracleConnection
#   3. Query the first 10 rows of the zipcode table
#   4. Print the result
#
# Run from the repo root:
#   python exercises/session_09_exercise.py
#
# NOTE: VPN required — the Oracle server is only reachable on the GSU network.

from pathlib import Path
from dotenv import load_dotenv
from lightoracle import LightOracleConnection

# TODO: Load credentials from the .env file
load_dotenv(Path("___") / "___")

# 2. Connect to Oracle
conn = LightOracleConnection()

# TODO: Query the first 10 rows of the zipcode table
df = conn.execute_query("___")

# 4. Print the result
print(df)
print("Done.")
