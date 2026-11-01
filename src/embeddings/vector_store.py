from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from src.utils.config import CHROMA_DB_PATH, EMBEDDING_MODEL
from src.utils.logger import logger

def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def create_vector_store(chunks):
    logger.info("Creating ChromaDB vector store...")
    embeddings = get_embedding_model()
    db = Chroma.from_documents(documents=chunks, embedding=embeddings,
                                persist_directory=CHROMA_DB_PATH)
    logger.info(f"Vector store created with {len(chunks)} chunks.")
    return db

def load_vector_store():
    return Chroma(persist_directory=CHROMA_DB_PATH,
                  embedding_function=get_embedding_model())
