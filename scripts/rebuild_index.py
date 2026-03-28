import os
import psycopg2
from dotenv import load_dotenv

from src.infrastructure.db import PostgresPaperRepository, PostgresVectorStore
from src.infrastructure.embedding import OpenAIEmbeddingClient
from src.services.indexing import IndexingService

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
paper_repo = PostgresPaperRepository(conn)
vector_store = PostgresVectorStore(conn)
embedding_client = OpenAIEmbeddingClient(api_key=os.getenv("OPENAI_API_KEY"))

# Derive path (source store → chunk → embed → vector index)
indexing = IndexingService(
    paper_repo=paper_repo,
    embedding_client=embedding_client,
    vector_store=vector_store,
)

indexing.rebuild_index()
conn.close()
