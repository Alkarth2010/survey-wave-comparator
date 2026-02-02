import pandas as pd
from rapidfuzz import fuzz


def compare_scales(s1, s2, var_map, label_threshold=95):
    """
    Full-intelligence scale comparison for matched variables only.

    Parameters
    ----------
    s1 : DataFrame
        Wave 1 scales (var_name, value, value_label)
    s2 : DataFrame
        Wave 2 scales (var_name, value, value_label)
    var_map : DataFrame
        Variable mapping table (old_var, new_var, status)
    label_threshold : int
        Similarity threshold for label match

    Returns
    -------
    DataFrame
        Scale comparison results
    """

    results = []

    for _, row in var_map.iterrows():
        old_var = row["old_var"]
        new_var = row["new_var"]
        var_status = row["status"]

        s1_sub = s1[s1["var_name"] == old_var]
        s2_sub = s2[s2["var_name"] == new_var]

        used_s2_values = set()

        # ----------------------------------
        # Compare Wave 1 → Wave 2
        # ----------------------------------
        for _, r1 in s1_sub.iterrows():
            best_score = 0
            best_match = None

            for _, r2 in s2_sub.iterrows():
                score = fuzz.token_sort_ratio(
                    str(r1["value_label"]).lower(),
                    str(r2["value_label"]).lower()
                )
                if score > best_score:
                    best_score = score
                    best_match = r2

            if best_match is not None and best_score >= label_threshold:
                used_s2_values.add(best_match["value"])

                if r1["value"] == best_match["value"]:
                    status = (
                        "UNCHANGED"
                        if best_score >= label_threshold
                        else "LABEL MODIFIED"
                    )
                else:
                    status = "VALUE RECODED"

                results.append({
                    "old_var": old_var,
                    "new_var": new_var,
                    "old_value": r1["value"],
                    "new_value": best_match["value"],
                    "old_label": r1["value_label"],
                    "new_label": best_match["value_label"],
                    "similarity_score": best_score,
                    "var_status": var_status,
                    "status": status
                })

            else:
                # Value removed in Wave 2
                results.append({
                    "old_var": old_var,
                    "new_var": new_var,
                    "old_value": r1["value"],
                    "new_value": None,
                    "old_label": r1["value_label"],
                    "new_label": None,
                    "similarity_score": best_score,
                    "var_status": var_status,
                    "status": "REMOVED"
                })

        # ----------------------------------
        # Added values in Wave 2
        # ----------------------------------
        for _, r2 in s2_sub.iterrows():
            if r2["value"] not in used_s2_values:
                results.append({
                    "old_var": old_var,
                    "new_var": new_var,
                    "old_value": None,
                    "new_value": r2["value"],
                    "old_label": None,
                    "new_label": r2["value_label"],
                    "similarity_score": None,
                    "var_status": var_status,
                    "status": "ADDED"
                })

    return pd.DataFrame(results)
