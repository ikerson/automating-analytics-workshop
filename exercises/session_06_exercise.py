# Session 6 Exercise — Creating Visualizations
#
# Task:
#   1. Load exercises/data/merged_contacts.csv (produced in the Session 4 exercise)
#   2. Drop rows with no school match (school_name is NaN)
#   3. Count students per school using groupby + agg, sort descending, keep top 5
#   4. Create a horizontal bar chart (barh) of top 5 schools by student count
#   5. Label the x-axis "Number of Contacts", add a title "Top 5 Middle Schools by Contacts"
#   6. Invert the y-axis so the school with the most contacts appears at the top
#   7. Call plt.tight_layout() and save the chart to exercises/data/top_schools_chart.png
#   8. Call plt.close() after saving
#
# Run from the repo root:
#   python exercises/session_06_exercise.py

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = Path('exercises') / 'data'

# TODO: Load merged_contacts.csv
merged = pd.read_csv(DATA_DIR / "___")

# TODO: Drop rows with no school match, then build the top-5 count
matched = merged.dropna(subset=["___"])
top5 = (
    matched.groupby("___")
    .agg(student_count=("___", "count"))
    .reset_index()
    .sort_values("___", ascending=False)
    .head(5)
)

# 4. Build the chart
fig, ax = plt.subplots(figsize=(9, 5))

# TODO: Plot a horizontal bar chart — fill in the x and y columns
ax.barh(top5["___"], top5["___"], color='steelblue')

# TODO: Fill in the x-axis label and chart title from the task description
ax.set_xlabel("___")
ax.set_title("___")

# 6. Highest bar at the top
ax.invert_yaxis()

# TODO: Save the chart and close
plt.tight_layout()
plt.savefig(DATA_DIR / "___")
plt.close()
print("Done.")
