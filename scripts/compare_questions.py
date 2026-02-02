from rapidfuzz import fuzz
import pandas as pd

def compare_questions(q1, q2, threshold):
    results = []
    matched_q2_indices = set()

    # ---------------------------------
    # Wave 1 → Wave 2 comparison
    # ---------------------------------
    for idx1, r1 in q1.iterrows():
        best_score = 0
        best_match = None
        best_idx2 = None

        for idx2, r2 in q2.iterrows():
            score = fuzz.token_sort_ratio(
                r1["clean_text"], r2["clean_text"]
            )
            if score > best_score:
                best_score = score
                best_match = r2
                best_idx2 = idx2

        if best_score >= threshold:
            status = "UNCHANGED"
            q2_text = best_match["question_text"]

            w1_200 = (r1["question_text"] or "")[:200].strip().lower()
            w2_200 = (q2_text or "")[:200].strip().lower()
            first_200_match = w1_200 == w2_200

            matched_q2_indices.add(best_idx2)
        else:
            status = "MODIFIED / DROPPED"
            q2_text = None
            first_200_match = False

        results.append({
            "question_wave1": r1["question_text"],
            "question_wave2": q2_text,
            "similarity": best_score,
            "first_200_char_match": first_200_match,
            "status": status
        })

    # ---------------------------------
    # ADDED questions (Wave 2 only)
    # ---------------------------------
    for idx2, r2 in q2.iterrows():
        if idx2 not in matched_q2_indices:
            results.append({
                "question_wave1": None,
                "question_wave2": r2["question_text"],
                "similarity": None,
                "first_200_char_match": None,
                "status": "ADDED"
            })

    return pd.DataFrame(results)
