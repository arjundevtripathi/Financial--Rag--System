from langchain_community.document_loaders import PyPDFLoader

def load_pdf(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    filename = os.path.basename(pdf_path)
    for page in pages:
        page.metadata["source"]  = filename
        page.metadata["company"] = filename.split("_")[0]
        page.metadata["type"]    = "annual_report"
    return pages

import os
