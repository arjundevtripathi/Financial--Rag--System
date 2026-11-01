import re

def clean_text(text: str) -> str:
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\t+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.replace("\x00", "").strip()
