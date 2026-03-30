import psycopg2
from src.config import Config


from src.infrastructure.db import PostgresPaperRepository, PostgresVectorStore
from src.infrastructure.embedding import OpenAIEmbeddingClient
from src.services.indexing import IndexingService

config = Config.from_env()

conn = psycopg2.connect(config.database_url)
paper_repo = PostgresPaperRepository(conn)
vector_store = PostgresVectorStore(conn)
embedding_client = OpenAIEmbeddingClient(config.openai_api_key)

# Derive path (source store → chunk → embed → vector index)
indexing = IndexingService(
    paper_repo=paper_repo,
    embedding_client=embedding_client,
    vector_store=vector_store,
)

indexing.rebuild_index()
conn.close()
