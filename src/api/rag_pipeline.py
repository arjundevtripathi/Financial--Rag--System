import os
from src.llm.response_generator import ResponseGenerator
from src.utils.logger import logger


class RAGPipeline:
    def __init__(self):
        logger.info("Initialising RAG Pipeline...")
        self.generator = ResponseGenerator()
        self.retrieval = None
        self.fallback  = None
        self._setup_retrieval()
        logger.info("RAG Pipeline ready.")

    def _setup_retrieval(self):
        """Build BM25 + hybrid retrieval if PDFs exist, else use vector-only."""
        pdf_dir  = "data/raw/annual_reports"
        ec_dir   = "data/raw/earnings_calls"
        has_pdfs = os.path.exists(pdf_dir) and any(f.endswith(".pdf") for f in os.listdir(pdf_dir))
        has_txts = os.path.exists(ec_dir)  and any(f.endswith(".txt") for f in os.listdir(ec_dir))

        if has_pdfs or has_txts:
            from src.ingestion.load_all_pdfs import load_all_pdfs
            from src.ingestion.earnings_loader import load_transcripts
            from src.preprocessing.chunking import create_chunks
            from src.retrieval.bm25_search import BM25Retriever
            from src.retrieval.retrieval_pipeline import RetrievalPipeline

            all_docs = []
            if has_pdfs:
                all_docs.extend(load_all_pdfs(pdf_dir))
            if has_txts:
                all_docs.extend(load_transcripts(ec_dir))

            chunks = create_chunks(all_docs)
            bm25   = BM25Retriever(chunks)
            self.retrieval = RetrievalPipeline(bm25)
            self.fallback  = None
            logger.info(f"Retrieval ready with {len(chunks)} chunks.")
        else:
            try:
                from src.retrieval.retriever import VectorRetriever
                self.retrieval = None
                self.fallback  = VectorRetriever()
                logger.info("Using vector-only fallback retrieval.")
            except Exception:
                self.retrieval = None
                self.fallback  = None
                logger.warning("No documents found. Upload files first.")

    def reindex(self):
        """Re-build retrieval after new file uploads."""
        logger.info("Re-indexing after file upload...")
        self._setup_retrieval()

    def ask(self, question: str, top_k: int = 5):
        if self.retrieval is None and self.fallback is None:
            return (
                "No documents have been indexed yet. "
                "Please upload a financial document (PDF, TXT, or CSV) first.",
                [],
            )

        if self.retrieval:
            docs = self.retrieval.retrieve(question)
        else:
            docs = self.fallback.retrieve(question, k=top_k)

        answer = self.generator.generate(question, docs)
        sources = [
            {
                "source":  d.metadata.get("source", "unknown"),
                "company": d.metadata.get("company", "unknown"),
                "excerpt": d.page_content[:200],
            }
            for d in docs
        ]
        return answer, sources
