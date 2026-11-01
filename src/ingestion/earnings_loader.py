import os
from langchain_core.documents import Document

def load_transcripts(folder_path: str):
    docs = []
    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
                text = f.read()
            docs.append(Document(
                page_content=text,
                metadata={"source": file, "type": "earnings_call", "company": file.split("_")[0]},
            ))
    return docs
