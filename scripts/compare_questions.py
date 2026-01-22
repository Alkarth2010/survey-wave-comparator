from rapidfuzz import fuzz
import pandas as pd

def compare_questions(q1, q2, threshold):
    results = []

    for _, r1 in q1.iterrows():
        best_score = 0
        best_match = None

        for _, r2 in q2.iterrows():
            score = fuzz.token_sort_ratio(
                r1["clean_text"], r2["clean_text"]
            )
            if score > best_score:
                best_score = score
                best_match = r2

        if best_score >= threshold:
            status = "UNCHANGED"
            q2_text = best_match["question_text"]
        else:
            status = "MODIFIED / DROPPED"
            q2_text = None

        results.append({
            "question_wave1": r1["question_text"],
            "question_wave2": q2_text,
            "similarity": best_score,
            "status": status
        })

    return pd.DataFrame(results)