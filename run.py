import yaml
from scripts.extract_spss import extract_spss
from scripts.extract_word import extract_questions
from scripts.normalize import normalize_text
from scripts.compare_questions import compare_questions
from scripts.compare_variables import compare_variables
from scripts.compare_scales import compare_scales
from scripts.report import generate_report

# Load rules
with open("config/rules.yaml") as f:
    rules = yaml.safe_load(f)

wave1 = "input/wave_2024"
wave2 = "input/wave_2025"

# SPSS
v1, s1 = extract_spss(f"{wave1}/data.sav", "2024")
v2, s2 = extract_spss(f"{wave2}/data.sav", "2025")

# Word
q1 = extract_questions(f"{wave1}/questionnaire.docx", "2024")
q2 = extract_questions(f"{wave2}/questionnaire.docx", "2025")

# Normalize
q1["clean_text"] = q1["question_text"].apply(normalize_text)
q2["clean_text"] = q2["question_text"].apply(normalize_text)

# Compare questions & variables
q_diff = compare_questions(q1, q2, rules["question_similarity_threshold"])
v_diff = compare_variables(v1, v2)

# -------------------------------------------------
# Build variable mapping for scale comparison
# -------------------------------------------------
var_map = v_diff[
    v_diff["old_var"].notna() &
    v_diff["new_var"].notna() &
    ~v_diff["status"].isin(["ADDED", "DROPPED"])
][["old_var", "new_var", "status"]]

# -------------------------------------------------
# Scale comparison (full intelligence)
# -------------------------------------------------
s_diff = compare_scales(
    s1,
    s2,
    var_map,
    label_threshold=rules.get("scale_label_similarity_threshold", 95)
)

# Report
generate_report({
    "questions": q_diff,
    "variables": v_diff,
    "scales": s_diff
})

print("✅ Done! Check output folder.")
