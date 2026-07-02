# Before You Begin Exercise - Python Fundamentals
#
# Task:
# Write a script that:
# 
# 1. Defines a list of at least five numeric exam scores.
# 2. Writes a function `passing_scores(scores, cutoff)` that loops over the list and returns a new list containing only the scores at or above `cutoff`.
# 3. Calls the function with a cutoff of `70` and prints the result.
# 4. Checks to see if there are any students who got the same score, printing the result.
# 
# Run from the repo root:
#   python exercises/session_03_exercise.py

# TODO: Make a list of exam scores
exam_scores = "___"

# TODO: Define a function that loops over the scores
def passing_scores(scores, cutoff):
    scores_above_cutoff = "___"
    ...
    return scores_above_cutoff

# TODO: Call the function
scores_above_or_at_70 = passing_scores("___", "___")
print(f'Scores greater than or equal to 70: {"___"}')

# TODO: Check to see if any students got the same score
## HINT: You might find the len() function useful!
repeat_score = "___"
print(f'Any students with the same score?: {"___"}')