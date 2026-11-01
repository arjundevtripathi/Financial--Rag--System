# Financial RAG System

A production-ready **Retrieval-Augmented Generation (RAG)** system for querying
financial documents using LangChain, ChromaDB, Hybrid Search, and GPT.

---

## Quick Start

### 1. Install
```bash
pip install -r requirements.txt
```

### 2. Configure
```bash
cp .env.example .env
# Edit .env → add your OPENAI_API_KEY
```

### 3. Add PDFs
```
data/raw/annual_reports/Apple_2024.pdf
data/raw/annual_reports/Microsoft_2024.pdf
```

### 4. Build Index
```bash
python main.py
```

### 5. Start API
```bash
uvicorn src.api.app:app --reload
```

### 6. Start UI
```bash
streamlit run frontend/streamlit_app.py
```

Open: http://localhost:8501

---

## Docker
```bash
docker-compose -f deployment/docker-compose.yml up --build
```

---

## Tech Stack
| Component   | Technology                        |
|-------------|-----------------------------------|
| LLM         | OpenAI GPT-4o-mini                |
| Embeddings  | sentence-transformers/MiniLM-L6   |
| Vector DB   | ChromaDB                          |
| Sparse      | BM25 (rank-bm25)                  |
| Reranker    | CrossEncoder ms-marco-MiniLM      |
| Framework   | LangChain                         |
| API         | FastAPI                           |
| UI          | Streamlit                         |
| Evaluation  | RAGAS                             |
| Deployment  | Docker + Kubernetes               |

---

## Example Questions
- What was total revenue?
- What was net income growth?
- What risks were identified?
- Compare Apple and Microsoft revenue
- What was EPS?
- Summarize the Q3 earnings call

---

## 📤 File Upload

The app supports uploading documents directly from the UI:

1. Open `http://localhost:8501`
2. Click the **📂 Upload Documents** tab
3. Drag & drop or browse for files:
   - `.pdf` → Annual Reports (goes to `data/raw/annual_reports/`)
   - `.txt` / `.md` → Earnings Calls (goes to `data/raw/earnings_calls/`)
   - `.csv` → Market News (headline + date columns)
4. Click **🚀 Upload & Index All Files**
5. Switch to **💬 Ask Questions** tab and start querying

### Upload API (direct)
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@Apple_2024.pdf"
```

### List documents
```bash
curl http://localhost:8000/documents
```

### Delete a document
```bash
curl -X DELETE http://localhost:8000/documents/Apple_2024.pdf
```
