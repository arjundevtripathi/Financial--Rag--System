from pydantic import BaseModel
from typing import Optional, List

class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 5

class SourceInfo(BaseModel):
    source: str
    company: str
    excerpt: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: Optional[List[SourceInfo]] = []

class UploadResponse(BaseModel):
    message: str
    filename: str
    type: str
    path: str

class DocumentInfo(BaseModel):
    filename: str
    type: str
    size_kb: float
    folder: str

class DocumentListResponse(BaseModel):
    documents: List[DocumentInfo]
    total: int
