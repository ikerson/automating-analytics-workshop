# Session 9 Exercise — Working with Database Results
#
# Task:
#   1. Load student_report/.env
#   2. Connect to Oracle using LightOracleConnection
#   3. Query all rows from the course table
#   4. Normalize column names to lowercase
#   5. Filter to courses with cost > 1000
#   6. Save the filtered result to exercises/data/courses_over_1000.csv (no index)
#   7. Print how many courses remain after filtering
#
# Run from the repo root:
#   python exercises/session_09_exercise.py
#
# NOTE: VPN required — the Oracle server is only reachable on the GSU network.

from pathlib import Path
from dotenv import load_dotenv
from lightoracle import LightOracleConnection

# 1. Load credentials
load_dotenv(Path("student_report") / ".env")

# 2. Connect to Oracle
conn = LightOracleConnection()

# TODO: Query all rows from the course table
df = conn.execute_query("___")

# 4. Normalize column names to lowercase
df.columns = df.columns.str.lower()

# TODO: Filter to courses with cost > 1000
df = df[df["___"] > ___]

# TODO: Save to exercises/data/courses_over_1000.csv — no row index
df.to_csv(Path("exercises") / "data" / "___", index=False)

print(f"Courses with cost > 1000: {len(___)}")
print("Done.")
