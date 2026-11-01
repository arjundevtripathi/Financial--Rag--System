import os
from src.ingestion.pdf_loader import load_pdf
from src.utils.logger import logger

def load_all_pdfs(folder_path: str):
    all_docs = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            path = os.path.join(folder_path, file)
            logger.info(f"Loading: {file}")
            docs = load_pdf(path)
            all_docs.extend(docs)
    logger.info(f"Total pages loaded: {len(all_docs)}")
    return all_docs
