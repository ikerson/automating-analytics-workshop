# Session 7 Exercise — Creating Visualizations

> Optional enrichment — complete during the session if time allows, or finish independently on your fork.

## Your Task

1. Load `exercises/data/merged_contacts.csv` (produced in the Session 5 exercise)
2. Drop rows with no school match (`school_name` is NaN)
3. Count students per school using `groupby` + `agg`, sort descending, keep top 5
4. Create a horizontal bar chart (`barh`) of top 5 schools by student count
5. Label the x-axis "Number of Contacts", add the title "Top 5 Middle Schools by Contacts"
6. Invert the y-axis so the school with the most contacts appears at the top
7. Call `plt.tight_layout()` and save the chart to `exercises/data/top_schools_chart.png`
8. Call `plt.close()` after saving

## Starter Script

Open [`session_07_exercise.py`](session_07_exercise.py) and fill in the blanks marked with `# TODO:`. If you get stuck, the completed version is at [`session_07_answer.py`](session_07_answer.py).

Run from the repo root:

```
python exercises/session_07_exercise.py
```
