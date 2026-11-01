"""Quick test for the retrieval pipeline. Run: python -m src.retrieval.test_pipeline"""
from src.retrieval.retrieval_pipeline import RetrievalPipeline
from src.ingestion.load_all_pdfs import load_all_pdfs
from src.preprocessing.chunking import create_chunks
from src.retrieval.bm25_search import BM25Retriever

docs   = load_all_pdfs("data/raw/annual_reports")
chunks = create_chunks(docs)
bm25   = BM25Retriever(chunks)
pipe   = RetrievalPipeline(bm25)
results = pipe.retrieve("revenue growth")
for doc in results:
    print("=" * 50)
    print(f"Source: {doc.metadata.get('source')}")
    print(doc.page_content[:300])
