# Before You Begin Exercise - Python Fundamentals
#
# Run from the repo root:
#   python exercises/session_03_answer.py

exam_scores = [65, 92, 81, 40, 70]

def passing_scores(scores, cutoff):
    scores_above_cutoff = []
    for score in scores:
        if score >= cutoff:
            scores_above_cutoff.append(score)
    return scores_above_cutoff

scores_above_or_at_70 = passing_scores(exam_scores, 70)
print(f'Scores greater than or equal to 70: {scores_above_or_at_70}')

repeat_score = len(set(exam_scores)) != len(exam_scores)
print(f'Any students with the same score?: {repeat_score}')