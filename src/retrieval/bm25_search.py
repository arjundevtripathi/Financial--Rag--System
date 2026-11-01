from rank_bm25 import BM25Okapi
from src.utils.config import TOP_K_RESULTS

class BM25Retriever:
    def __init__(self, documents):
        self.documents = documents
        corpus = [doc.page_content.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(corpus)

    def retrieve(self, query: str, k: int = None):
        k = k or TOP_K_RESULTS
        scores = self.bm25.get_scores(query.lower().split())
        ranked = sorted(zip(self.documents, scores), key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in ranked[:k]]
