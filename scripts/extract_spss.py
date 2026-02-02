import pyreadstat
import pandas as pd


def extract_spss(sav_path, wave):
    df, meta = pyreadstat.read_sav(sav_path)

    # Variable metadata
    variables = pd.DataFrame({
        "var_name": meta.column_names,
        "var_label": meta.column_labels,
        "wave": wave
    })

    values = []

    # variable → value label set name
    var_to_labelset = meta.variable_to_label

    # value label set name → {value: label}
    labelsets = meta.value_labels

    for var, labelset_name in var_to_labelset.items():
        if labelset_name in labelsets:
            for val, lbl in labelsets[labelset_name].items():
                values.append({
                    "var_name": var,              # ✅ CORRECT
                    "value": val,
                    "value_label": lbl,
                    "wave": wave
                })

    return variables, pd.DataFrame(values)
