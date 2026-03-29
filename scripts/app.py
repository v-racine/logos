import os
import psycopg2
from dotenv import load_dotenv

from src.infrastructure.db import PostgresVectorStore
from src.infrastructure.embedding import OpenAIEmbeddingClient
from src.infrastructure.llm import OpenAILLMClient
from src.services.query import QueryService
from src.handlers.gradio_ui import GradioApp

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
vector_store = PostgresVectorStore(conn)

embedding_client = OpenAIEmbeddingClient(api_key=os.getenv("OPENAI_API_KEY"))
llm_client = OpenAILLMClient(api_key=os.getenv("OPENAI_API_KEY"))

query_service = QueryService(
    embedding_client=embedding_client,
    vector_store=vector_store,
    llm_client=llm_client,
)

app = GradioApp(query_service=query_service)
app.build().launch()
