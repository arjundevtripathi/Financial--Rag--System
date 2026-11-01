import os
from src.ingestion.load_all_pdfs import load_all_pdfs
from src.ingestion.earnings_loader import load_transcripts
from src.ingestion.news_loader import load_news
from src.preprocessing.chunking import create_chunks
from src.preprocessing.metadata_processor import enrich_metadata
from src.embeddings.vector_store import create_vector_store
from src.utils.logger import logger

def build_index():
    all_docs = []
    pdf_dir = "data/raw/annual_reports"
    if os.path.exists(pdf_dir) and any(f.endswith(".pdf") for f in os.listdir(pdf_dir)):
        logger.info("Loading PDFs...")
        all_docs.extend(load_all_pdfs(pdf_dir))

    ec_dir = "data/raw/earnings_calls"
    if os.path.exists(ec_dir) and any(f.endswith(".txt") for f in os.listdir(ec_dir)):
        logger.info("Loading earnings calls...")
        all_docs.extend(load_transcripts(ec_dir))

    news_path = "data/raw/market_news/news.csv"
    if os.path.exists(news_path):
        logger.info("Loading news...")
        all_docs.extend(load_news(news_path))

    if not all_docs:
        raise ValueError("No documents found. Add PDFs to data/raw/annual_reports/")

    logger.info(f"Total docs: {len(all_docs)}")
    chunks = create_chunks(all_docs)
    chunks = enrich_metadata(chunks)
    logger.info(f"Total chunks: {len(chunks)}")
    return create_vector_store(chunks)
