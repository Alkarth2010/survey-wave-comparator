import pandas as pd
from rapidfuzz import fuzz
import re

def split_option_stem(label):
    if label is None:
        return None, None
    parts = re.split(r"\s*-\s*", label, maxsplit=1)
    if len(parts) == 2:
        return parts[0].strip().lower(), parts[1].strip().lower()
    return None, label.strip().lower()


def compare_variables(v1, v2):
    results = []

    # Track matched variables
    matched_v1 = set()
    matched_v2 = set()

    # -----------------------------
    # PHASE 1: var_name match
    # -----------------------------
    common_vars = set(v1["var_name"]).intersection(set(v2["var_name"]))

    for var in common_vars:
        r1 = v1[v1["var_name"] == var].iloc[0]
        r2 = v2[v2["var_name"] == var].iloc[0]

        score = fuzz.token_sort_ratio(
            str(r1["var_label"]).lower(),
            str(r2["var_label"]).lower()
        )

        status = "COMMON" if score >= 95 else "REVIEW"

        results.append({
            "old_var": var,
            "new_var": var,
            "old_label": r1["var_label"],
            "new_label": r2["var_label"],
            "similarity_score": score,
            "status": status
        })

        matched_v1.add(var)
        matched_v2.add(var)

    # -----------------------------
    # PHASE 2: unmatched → label check
    # -----------------------------
    v1_unmatched = v1[~v1["var_name"].isin(matched_v1)]
    v2_unmatched = v2[~v2["var_name"].isin(matched_v2)]

    for _, r1 in v1_unmatched.iterrows():
        best_score = 0
        best_match = None

        opt1, stem1 = split_option_stem(r1["var_label"])

        for _, r2 in v2_unmatched.iterrows():
            opt2, stem2 = split_option_stem(r2["var_label"])

            score = fuzz.token_sort_ratio(stem1, stem2)

            # 🚫 OPTION-LEVEL GUARD
            if score >= 95 and opt1 != opt2:
                continue

            if score > best_score:
                best_score = score
                best_match = r2
                best_opt2 = opt2

        if best_match is not None and best_score == 100:
            status = "VARIABLE NAME MISMATCH"
            matched_v1.add(r1["var_name"])
            matched_v2.add(best_match["var_name"])

        elif best_match is not None and best_score >= 95:
            status = "VARIABLE LABEL REVIEW"
            matched_v1.add(r1["var_name"])
            matched_v2.add(best_match["var_name"])

        else:
            continue

        results.append({
            "old_var": r1["var_name"],
            "new_var": best_match["var_name"],
            "old_label": r1["var_label"],
            "new_label": best_match["var_label"],
            "similarity_score": best_score,
            "status": status
        })

    # -----------------------------
    # DROPPED variables (old wave)
    # -----------------------------
    for _, r1 in v1.iterrows():
        if r1["var_name"] not in matched_v1:
            best_score = 0
            best_match_var = None
            best_match_label = None

            for _, r2 in v2.iterrows():
                score = fuzz.token_sort_ratio(
                    str(r1["var_label"]).lower(),
                    str(r2["var_label"]).lower()
                )
                if score > best_score:
                    best_score = score
                    best_match_var = r2["var_name"]
                    best_match_label = r2["var_label"]

            results.append({
                "old_var": r1["var_name"],
                "new_var": None,
                "old_label": r1["var_label"],
                "new_label": None,
                "similarity_score": best_score,
                "closest_new_var": best_match_var,
                "closest_new_label": best_match_label,
                "status": "DROPPED"
            })

    # -----------------------------
    # ADDED variables (new wave)
    # -----------------------------
    for _, r2 in v2.iterrows():
        if r2["var_name"] not in matched_v2:
            best_score = 0
            best_match_var = None
            best_match_label = None

            for _, r1 in v1.iterrows():
                score = fuzz.token_sort_ratio(
                    str(r2["var_label"]).lower(),
                    str(r1["var_label"]).lower()
                )
                if score > best_score:
                    best_score = score
                    best_match_var = r1["var_name"]
                    best_match_label = r1["var_label"]

            results.append({
                "old_var": None,
                "new_var": r2["var_name"],
                "old_label": None,
                "new_label": r2["var_label"],
                "similarity_score": best_score,
                "closest_old_var": best_match_var,
                "closest_old_label": best_match_label,
                "status": "ADDED"
            })
    return pd.DataFrame(results)