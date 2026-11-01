"""
Financial RAG System - Entry Point

Steps:
  1. python main.py                            # Build index
  2. uvicorn src.api.app:app --reload          # Start API
  3. streamlit run frontend/streamlit_app.py  # Start UI
"""
import os, sys

def main():
    for d in ["data/raw/annual_reports","data/raw/earnings_calls",
               "data/raw/market_news","data/processed/chunks",
               "data/processed/embeddings","data/processed/metadata",
               "vector_db/chroma_db","logs"]:
        os.makedirs(d, exist_ok=True)

    pdf_dir = "data/raw/annual_reports"
    pdfs = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    if not pdfs:
        print("\n" + "="*60)
        print("No PDFs found in data/raw/annual_reports/")
        print("Add PDF files like Apple_2024.pdf and run again.")
        print("="*60)
        sys.exit(0)

    from src.embeddings.index_documents import build_index
    from src.utils.logger import logger
    logger.info("Starting indexing...")
    print(f"Found {len(pdfs)} PDF(s). Building index...")
    build_index()
    print("\nIndex Ready!")
    print("  Run: uvicorn src.api.app:app --reload")
    print("  Run: streamlit run frontend/streamlit_app.py")

if __name__ == "__main__":
    main()
