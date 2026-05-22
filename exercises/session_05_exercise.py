# Session 5 Exercise — Working with Database Results
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
#   python exercises/session_05_exercise.py
#
# NOTE: VPN required — the Oracle server is only reachable on the GSU network.

from pathlib import Path
from dotenv import load_dotenv
from lightoracle import LightOracleConnection

# TODO: Load student_report/.env
# Hint: load_dotenv(Path('student_report') / '.env')


# TODO: Create a LightOracleConnection
# Hint: conn = LightOracleConnection()


# TODO: Query all rows from the course table
# Hint: df = conn.execute_query("SELECT * FROM course")


# TODO: Normalize column names to lowercase
# Hint: df.columns = df.columns.str.lower()


# TODO: Filter to courses with cost > 1000
# Hint: df = df[df['cost'] > 1000]


# TODO: Save to exercises/data/courses_over_1000.csv (index=False)
# Hint: df.to_csv(Path('exercises') / 'data' / 'courses_over_1000.csv', index=False)


# TODO: Print how many courses remain after filtering
# Hint: print(f"Courses with cost > 1000: {len(df)}")


print("Done.")


# ---------------------------------------------------------------------------
# Answer — uncomment to check your work
# ---------------------------------------------------------------------------

# from pathlib import Path
# from dotenv import load_dotenv
# from lightoracle import LightOracleConnection
#
# load_dotenv(Path('student_report') / '.env')
# conn = LightOracleConnection()
# df = conn.execute_query("SELECT * FROM course")
# df.columns = df.columns.str.lower()
# df = df[df['cost'] > 1000]
# df.to_csv(Path('exercises') / 'data' / 'courses_over_1000.csv', index=False)
# print(f"Courses with cost > 1000: {len(df)}")
# print("Done.")
