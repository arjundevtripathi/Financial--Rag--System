from src.embeddings.vector_store import get_embedding_model
def test_embedding_model():
    model = get_embedding_model()
    assert model is not None
