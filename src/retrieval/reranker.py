from sentence_transformers import CrossEncoder
from src.utils.config import TOP_K_RESULTS

class Reranker:
    def __init__(self):
        self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def rerank(self, query: str, docs, top_k: int = None):
        top_k = top_k or TOP_K_RESULTS
        if not docs:
            return []
        scores = self.model.predict([(query, doc.page_content) for doc in docs])
        ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in ranked[:top_k]]
