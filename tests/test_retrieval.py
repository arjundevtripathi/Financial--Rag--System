from src.retrieval.retriever import VectorRetriever
def test_retriever_loads():
    r = VectorRetriever()
    assert r is not None
