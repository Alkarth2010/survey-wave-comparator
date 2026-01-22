import re

def normalize_text(txt):
    txt = txt.lower()
    txt = re.sub(r"\s+", " ", txt)
    txt = re.sub(r"[^\w\s]", "", txt)
    return txt.strip()