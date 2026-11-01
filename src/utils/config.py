import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY")
MODEL_NAME      = os.getenv("MODEL_NAME", "gpt-4o-mini")
CHROMA_DB_PATH  = os.getenv("CHROMA_DB_PATH", "vector_db/chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
CHUNK_SIZE      = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP   = int(os.getenv("CHUNK_OVERLAP", "200"))
TOP_K_RESULTS   = int(os.getenv("TOP_K_RESULTS", "5"))
