import os
import shutil
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.api.models import QueryRequest, QueryResponse, SourceInfo
from src.api.rag_pipeline import RAGPipeline
from src.utils.logger import logger

UPLOAD_DIR = "data/raw/annual_reports"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title="Financial RAG API",
    description="Upload and query financial documents with RAG + GPT",
    version="2.0.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

pipeline = RAGPipeline()


@app.get("/")
def home():
    return {"message": "Financial RAG API Running", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a financial document (PDF, TXT, CSV). Re-indexes automatically."""
    allowed = {".pdf", ".txt", ".csv", ".md"}
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {allowed}",
        )

    # Choose destination based on file type
    if ext in {".txt", ".md"}:
        dest_dir = "data/raw/earnings_calls"
    elif ext == ".csv":
        dest_dir = "data/raw/market_news"
        # Always save as news.csv so loader picks it up
        file.filename = "news.csv"
    else:
        dest_dir = "data/raw/annual_reports"

    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, file.filename)

    try:
        with open(dest_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        logger.info(f"Uploaded: {file.filename} → {dest_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # Re-index so new file is immediately searchable
    try:
        pipeline.reindex()
        logger.info("Re-indexed after upload.")
    except Exception as e:
        logger.warning(f"Re-index failed: {e}")

    return JSONResponse({
        "message": f"'{file.filename}' uploaded and indexed successfully.",
        "filename": file.filename,
        "type": ext,
        "path": dest_path,
    })


@app.get("/documents")
def list_documents():
    """List all uploaded documents."""
    docs = []
    for folder, dtype in [
        ("data/raw/annual_reports", "PDF Report"),
        ("data/raw/earnings_calls", "Earnings Call"),
        ("data/raw/market_news",    "Market News"),
    ]:
        if os.path.exists(folder):
            for f in os.listdir(folder):
                if not f.startswith("."):
                    path = os.path.join(folder, f)
                    docs.append({
                        "filename": f,
                        "type":     dtype,
                        "size_kb":  round(os.path.getsize(path) / 1024, 1),
                        "folder":   folder,
                    })
    return {"documents": docs, "total": len(docs)}


@app.delete("/documents/{filename}")
def delete_document(filename: str):
    """Delete an uploaded document and re-index."""
    for folder in ["data/raw/annual_reports", "data/raw/earnings_calls", "data/raw/market_news"]:
        path = os.path.join(folder, filename)
        if os.path.exists(path):
            os.remove(path)
            logger.info(f"Deleted: {path}")
            try:
                pipeline.reindex()
            except Exception as e:
                logger.warning(f"Re-index after delete failed: {e}")
            return {"message": f"'{filename}' deleted and index updated."}
    raise HTTPException(status_code=404, detail=f"File '{filename}' not found.")


@app.post("/ask", response_model=QueryResponse)
def ask(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    try:
        answer, sources = pipeline.ask(request.question, top_k=request.top_k)
        return QueryResponse(
            question=request.question,
            answer=answer,
            sources=[SourceInfo(**s) for s in sources],
        )
    except Exception as e:
        logger.error(f"API error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
