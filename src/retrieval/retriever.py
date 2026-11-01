from src.embeddings.vector_store import load_vector_store
from src.utils.config import TOP_K_RESULTS

class VectorRetriever:
    def __init__(self):
        self.db = load_vector_store()

    def retrieve(self, query: str, k: int = None):
        return self.db.similarity_search(query, k=k or TOP_K_RESULTS)
