# Session 4 Exercise — Oracle Connection
#
# Task:
#   1. Load student_report/.env
#   2. Connect to Oracle using LightOracleConnection
#   3. Query the first 10 rows of the zipcode table
#   4. Print the result
#
# Run from the repo root:
#   python exercises/session_04_exercise.py
#
# NOTE: VPN required — the Oracle server is only reachable on the GSU network.

from pathlib import Path
from dotenv import load_dotenv
from lightoracle import LightOracleConnection

# TODO: Load student_report/.env
# Hint: load_dotenv(Path('student_report') / '.env')


# TODO: Create a LightOracleConnection
# Hint: conn = LightOracleConnection()


# TODO: Query the first 10 rows of the zipcode table
# Hint: conn.execute_query("SELECT * FROM zipcode FETCH FIRST 10 ROWS ONLY")


# TODO: Print the result


print("Done.")
