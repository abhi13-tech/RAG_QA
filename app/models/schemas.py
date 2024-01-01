from pydantic import BaseModel
from typing import List, Optional

class IngestRequest(BaseModel):
    paths: Optional[List[str]] = None

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class QARequest(BaseModel):
    query: str
    top_k: int = 5

class FeedbackRequest(BaseModel):
    query: str
    answer: str
    helpful: bool
    comment: Optional[str] = None

