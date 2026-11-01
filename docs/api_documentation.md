# Financial RAG API Documentation

## Base URL
`http://localhost:8000`

## Endpoints

### GET /
Returns API status.

### GET /health
Returns `{"status": "ok"}`

### POST /ask
**Request:**
```json
{"question": "What was revenue?", "top_k": 5}
```
**Response:**
```json
{
  "question": "What was revenue?",
  "answer": "**Answer:** Revenue was $45.2 billion...",
  "sources": [{"source": "Q1_2025.txt", "company": "Q1", "excerpt": "..."}]
}
```

## Swagger UI
Visit `http://localhost:8000/docs` for interactive API documentation.
