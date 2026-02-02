import pandas as pd

def build_summary_report(q_df, v_df, s_df):
    rows = []

    # -------------------------
    # Question counts
    # -------------------------
    rows.append({
        "Category": "Questions",
        "Metric": "Questions unchanged",
        "Count": (q_df["status"] == "UNCHANGED").sum()
    })

    rows.append({
        "Category": "Questions",
        "Metric": "Questions modified / dropped",
        "Count": (q_df["status"] == "MODIFIED / DROPPED").sum()
    })

    # Questions added (Wave 2 only)
    matched_wave2 = q_df["question_wave2"].notna().sum()
    total_wave2 = q_df["question_wave2"].nunique(dropna=True)

    rows.append({
        "Category": "Questions",
        "Metric": "Questions added",
        "Count": (q_df["status"] == "ADDED").sum()
    })

    # -------------------------
    # Variable counts
    # -------------------------
    matched_mask = (
        v_df["old_var"].notna() &
        v_df["new_var"].notna() &
        ~v_df["status"].isin(["ADDED", "DROPPED"])
    )

    rows.append({
        "Category": "Variables",
        "Metric": "Variables matched (common)",
        "Count": matched_mask.sum()
    })

    rows.append({
        "Category": "Variables",
        "Metric": "Variables marked for review",
        "Count": v_df["status"].isin([
            "REVIEW",
            "VARIABLE NAME MISMATCH",
            "VARIABLE LABEL REVIEW"
        ]).sum()
    })

    rows.append({
        "Category": "Variables",
        "Metric": "Variables added",
        "Count": (v_df["status"] == "ADDED").sum()
    })

    rows.append({
        "Category": "Variables",
        "Metric": "Variables removed",
        "Count": (v_df["status"] == "DROPPED").sum()
    })

    # -------------------------
    # Scale counts
    # -------------------------
    rows.append({
        "Category": "Scales",
        "Metric": "Variables with scale changes",
        "Count": s_df[s_df["status"] != "UNCHANGED"][
            ["old_var", "new_var"]
        ].drop_duplicates().shape[0]
    })

    rows.append({
        "Category": "Scales",
        "Metric": "Variables with recoded values",
        "Count": s_df[s_df["status"] == "VALUE RECODED"][
            ["old_var", "new_var"]
        ].drop_duplicates().shape[0]
    })

    return pd.DataFrame(rows)
