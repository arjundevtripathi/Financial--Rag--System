from src.retrieval.retriever import VectorRetriever
from src.utils.config import TOP_K_RESULTS

class HybridRetriever:
    def __init__(self, bm25_retriever):
        self.bm25   = bm25_retriever
        self.vector = VectorRetriever()

    def retrieve(self, query: str, k: int = None):
        k = k or TOP_K_RESULTS
        v_docs  = self.vector.retrieve(query, k=k)
        b_docs  = self.bm25.retrieve(query, k=k)
        seen, merged = set(), []
        for doc in v_docs + b_docs:
            key = doc.page_content[:80]
            if key not in seen:
                seen.add(key)
                merged.append(doc)
        return merged[:k * 2]
