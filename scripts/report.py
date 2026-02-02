import pandas as pd
from scripts.summary import build_summary_report 

def generate_report(outputs):
    output_path = "output/survey_comparison_report.xlsx"

    with pd.ExcelWriter(output_path) as writer:

        # -------------------------
        # REPORT (FIRST SHEET)
        # -------------------------
        report_df = build_summary_report(
            outputs["questions"],
            outputs["variables"],
            outputs["scales"]
        )

        report_df.to_excel(
            writer,
            sheet_name="Report",
            index=False
        )

        # -------------------------
        # Questions
        # -------------------------
        if outputs.get("questions") is not None and not outputs["questions"].empty:
            outputs["questions"].to_excel(
                writer,
                sheet_name="Question_Changes",
                index=False
            )

        # -------------------------
        # Variables
        # -------------------------
        if outputs.get("variables") is not None and not outputs["variables"].empty:
            outputs["variables"].to_excel(
                writer,
                sheet_name="Variable_Changes",
                index=False
            )

        # -------------------------
        # Scales
        # -------------------------
        if outputs.get("scales") is not None and not outputs["scales"].empty:
            outputs["scales"].to_excel(
                writer,
                sheet_name="Scale_Changes",
                index=False
            )
