import psycopg2

from src.config import Config
from src.infrastructure.db import PostgresVectorStore
from src.infrastructure.embedding import OpenAIEmbeddingClient
from src.infrastructure.llm import OpenAILLMClient
from src.services.query import QueryService
from src.handlers.gradio_ui import GradioApp


def main():
    """Initializes and launches the Gradio application."""
    config = Config.from_env()

    conn = psycopg2.connect(config.database_url)
    vector_store = PostgresVectorStore(conn)

    embedding_client = OpenAIEmbeddingClient(api_key=config.openai_api_key)
    llm_client = OpenAILLMClient(api_key=config.openai_api_key)

    query_service = QueryService(
        embedding_client=embedding_client,
        vector_store=vector_store,
        llm_client=llm_client,
    )

    app = GradioApp(query_service=query_service)
    app.build().launch()


if __name__ == "__main__":
    main()
