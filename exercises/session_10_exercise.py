# Session 10 Exercise — Creating Visualizations
#
# Task:
#   1. Load exercises/data/merged_contacts.csv (produced in the Session 8 exercise)
#   2. Drop rows with no school match (school_name is NaN)
#   3. Count students per school using groupby + agg, sort descending, keep top 5
#   4. Create a horizontal bar chart (barh) of top 5 schools by student count
#   5. Label the x-axis "Number of Contacts", add a title "Top 5 Middle Schools by Contacts"
#   6. Invert the y-axis so the school with the most contacts appears at the top
#   7. Call plt.tight_layout() and save the chart to exercises/data/top_schools_chart.png
#   8. Call plt.close() after saving
#
# Run from the repo root:
#   python exercises/session_10_exercise.py

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = Path('exercises') / 'data'

# TODO: Load merged_contacts.csv
# Hint: merged = pd.read_csv(DATA_DIR / 'merged_contacts.csv')


# TODO: Drop rows with no school match and count students per school (top 5)
# Hint: matched = merged.dropna(subset=['school_name'])
# Hint: top5 = (
#     matched.groupby('school_name')
#     .agg(student_count=('student_id', 'count'))
#     .reset_index()
#     .sort_values('student_count', ascending=False)
#     .head(5)
# )


# TODO: Create the figure and axes
# Hint: fig, ax = plt.subplots(figsize=(9, 5))


# TODO: Plot a horizontal bar chart (barh)
# Hint: ax.barh(top5['school_name'], top5['student_count'], color='steelblue')


# TODO: Label the x-axis and add a title
# Hint: ax.set_xlabel("Number of Contacts")
# Hint: ax.set_title("Top 5 Middle Schools by Contacts")


# TODO: Invert the y-axis so the largest bar is at the top
# Hint: ax.invert_yaxis()


# TODO: Call plt.tight_layout(), save to top_schools_chart.png, then call plt.close()
# Hint: plt.tight_layout()
# Hint: plt.savefig(DATA_DIR / 'top_schools_chart.png')
# Hint: plt.close()


print("Done.")


# ---------------------------------------------------------------------------
# Answer — uncomment to check your work
# ---------------------------------------------------------------------------

# from pathlib import Path
# import pandas as pd
# import matplotlib.pyplot as plt
#
# DATA_DIR = Path('exercises') / 'data'
#
# merged = pd.read_csv(DATA_DIR / 'merged_contacts.csv')
#
# matched = merged.dropna(subset=['school_name'])
# top5 = (
#     matched.groupby('school_name')
#     .agg(student_count=('student_id', 'count'))
#     .reset_index()
#     .sort_values('student_count', ascending=False)
#     .head(5)
# )
#
# fig, ax = plt.subplots(figsize=(9, 5))
# ax.barh(top5['school_name'], top5['student_count'], color='steelblue')
# ax.set_xlabel("Number of Contacts")
# ax.set_title("Top 5 Middle Schools by Contacts")
# ax.invert_yaxis()
# plt.tight_layout()
# plt.savefig(DATA_DIR / 'top_schools_chart.png')
# plt.close()
# print("Done.")
