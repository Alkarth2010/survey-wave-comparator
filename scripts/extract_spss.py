import pyreadstat
import pandas as pd

def extract_spss(sav_path, wave):
    df, meta = pyreadstat.read_sav(sav_path)

    variables = pd.DataFrame({
        "var_name": meta.column_names,
        "var_label": meta.column_labels,
        "wave": wave
    })

    values = []
    for var, labels in meta.value_labels.items():
        for k, v in labels.items():
            values.append({
                "var_name": var,
                "value": k,
                "value_label": v,
                "wave": wave
            })

    return variables, pd.DataFrame(values)