# Survey Wave Comparator

A Python automation tool for comparing survey waves across SPSS data files and Word questionnaires.

This project helps market research and data processing teams identify questionnaire changes, variable label changes, added or dropped variables, scale/value recoding, and other wave-on-wave differences that can affect validation, tabulation, reporting, and client deliverables.

## Why This Project Exists

Survey wave validation is often manual, repetitive, and quality-sensitive. Even small changes in questionnaire wording, SPSS variable labels, value labels, or variable names can create downstream issues in tabulation and reporting.

Survey Wave Comparator automates the first layer of comparison so analysts can review changes faster, catch inconsistencies earlier, and focus human attention on the items that need judgment.

## Key Features

- Extracts variable names and variable labels from SPSS `.sav` files
- Extracts questions from Word questionnaire `.docx` files
- Compares Wave 1 vs Wave 2 questionnaire text
- Detects added, dropped, modified, and unchanged questions
- Compares SPSS variable names and variable labels
- Flags variable name mismatches and variable label review cases
- Compares value labels and scales between matched variables
- Detects added, removed, unchanged, and recoded scale values
- Generates a structured Excel validation report
- Uses fuzzy matching to support practical market research review workflows

## Tech Stack

- Python
- pandas
- pyreadstat
- python-docx
- RapidFuzz
- openpyxl
- xlsxwriter
- PyYAML

## Project Structure

```text
survey-wave-comparator/
|-- config/
|   `-- rules.yaml
|-- scripts/
|   |-- extract_spss.py
|   |-- extract_word.py
|   |-- normalize.py
|   |-- compare_questions.py
|   |-- compare_variables.py
|   |-- compare_scales.py
|   |-- summary.py
|   `-- report.py
|-- run.py
|-- requirements.txt
`-- README.md
```

## Expected Input Structure

```text
input/
|-- wave_2024/
|   |-- data.sav
|   `-- questionnaire.docx
`-- wave_2025/
    |-- data.sav
    `-- questionnaire.docx
```

## How It Works

1. Reads SPSS metadata from both survey waves.
2. Extracts variable names, variable labels, and value labels.
3. Reads questionnaire text from Word documents.
4. Normalizes question text for comparison.
5. Uses fuzzy matching to compare questions across waves.
6. Compares SPSS variable names and labels.
7. Compares value labels and detects recoded scale values.
8. Generates an Excel report with summary and review sheets.

## Output

The tool generates:

```text
output/survey_comparison_report.xlsx
```

The Excel report includes:

- Summary report
- Question changes
- Variable changes
- Scale changes
- Color-coded review statuses
- Hyperlinks from the summary sheet to detailed review sheets

## Example Use Cases

- Market research wave-on-wave survey validation
- SPSS metadata quality checks
- Questionnaire-to-data consistency review
- Variable label comparison
- Scale/value label recoding checks
- Pre-tabulation data processing review
- Data quality automation for research operations

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python run.py
```

## Configuration

Similarity thresholds can be adjusted in:

```text
config/rules.yaml
```

Example:

```yaml
question_similarity_threshold: 90
```

## Current Status

This is a working Python automation project focused on survey wave comparison and market research data validation. It is designed as a practical workflow tool for data processing teams that need structured, repeatable, and review-friendly validation checks.

## Future Improvements

- Streamlit UI for uploading files and reviewing results
- AI-assisted explanation of detected changes
- Support for more questionnaire formats
- Exportable summary dashboard
- Human-in-the-loop review tagging
- Configurable input folders from the UI
- More detailed validation rules for complex survey structures

## Privacy Note

No survey data is included in this repository. Input files should be kept local or handled according to the relevant client, company, and data privacy requirements.

## Author

Built by Alagappan Ramasamy as part of practical automation work across market research data processing, survey validation, and AI-assisted workflow improvement.
