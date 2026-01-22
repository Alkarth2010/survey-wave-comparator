def compare_scales(s1, s2):
    merged = s1.merge(
        s2,
        on=["var_name", "value"],
        how="outer",
        suffixes=("_w1", "_w2"),
        indicator=True
    )

    merged["status"] = merged["_merge"].map({
        "left_only": "REMOVED",
        "right_only": "ADDED",
        "both": "UNCHANGED"
    })

    return merged