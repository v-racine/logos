from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Paper(BaseModel):
    id: Optional[int] = None
    title: str
    authors: Optional[str] = None
    source_url: str
    content: str
    publication_year: Optional[int] = None
    ingested_at: Optional[datetime] = None


class Chunk(BaseModel):
    id: Optional[int] = None
    paper_id: int
    content: str
    chunk_index: int
    embedding: Optional[list[float]] = None
    created_at: Optional[datetime] = None


class RetrievedChunk(BaseModel):
    chunk_id: int
    paper_id: int
    content: str
    chunk_index: int
    similarity_score: float
    paper_title: str
    authors: Optional[str] = None
    source_url: str
    publication_year: Optional[int] = None


class QueryResult(BaseModel):
    answer: str
    retrieved_chunks: list[RetrievedChunk]
    full_prompt: str
