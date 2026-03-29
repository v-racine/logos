import os
import psycopg2
from dotenv import load_dotenv

from src.infrastructure.db import PostgresVectorStore
from src.infrastructure.embedding import OpenAIEmbeddingClient
from src.infrastructure.llm import OpenAILLMClient
from src.services.query import QueryService
from src.handlers.gradio_ui import GradioApp


def main():
    """Initializes and launches the Gradio application."""
    load_dotenv()

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set.")

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    conn = psycopg2.connect(database_url)
    vector_store = PostgresVectorStore(conn)

    embedding_client = OpenAIEmbeddingClient(api_key=openai_api_key)
    llm_client = OpenAILLMClient(api_key=openai_api_key)

    query_service = QueryService(
        embedding_client=embedding_client,
        vector_store=vector_store,
        llm_client=llm_client,
    )

    app = GradioApp(query_service=query_service)
    app.build().launch()


if __name__ == "__main__":
    main()
