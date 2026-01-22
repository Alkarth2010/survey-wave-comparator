from docx import Document
import pandas as pd

def extract_questions(docx_path, wave):
    doc = Document(docx_path)
    rows = []

    for p in doc.paragraphs:
        txt = p.text.strip()
        if len(txt) > 10 and "?" in txt:
            rows.append({
                "question_text": txt,
                "wave": wave
            })

    return pd.DataFrame(rows)