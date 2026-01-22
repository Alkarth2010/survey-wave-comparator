import pandas as pd

def generate_report(outputs):
    output_path = "output/survey_comparison_report.xlsx"

    with pd.ExcelWriter(output_path) as writer:

        # -------------------------
        # Questions (always written)
        # -------------------------
        if outputs.get("questions") is not None and not outputs["questions"].empty:
            outputs["questions"].to_excel(
                excel_writer=writer,
                sheet_name="Question_Changes",
                index=False
            )

        # -------------------------
        # Variables (write only if data exists)
        # -------------------------
        if outputs.get("variables") is not None and not outputs["variables"].empty:
            outputs["variables"].to_excel(
                excel_writer=writer,
                sheet_name="Variable_Changes",
                index=False
            )

        # -------------------------
        # Scales (write only if data exists)
        # -------------------------
        if outputs.get("scales") is not None and not outputs["scales"].empty:
            outputs["scales"].to_excel(
                excel_writer=writer,
                sheet_name="Scale_Changes",
                index=False
            )
