from src.retrieval.reranker import Reranker
from src.retrieval.hybrid_search import HybridRetriever
from src.retrieval.query_processor import QueryProcessor
from src.utils.logger import logger

class RetrievalPipeline:
    def __init__(self, bm25_retriever):
        self.hybrid   = HybridRetriever(bm25_retriever)
        self.reranker = Reranker()

    def retrieve(self, query: str):
        query = QueryProcessor.expand(query)
        logger.info(f"Query: {query[:80]}")
        docs = self.hybrid.retrieve(query)
        docs = self.reranker.rerank(query, docs)
        logger.info(f"Retrieved {len(docs)} chunks.")
        return docs
