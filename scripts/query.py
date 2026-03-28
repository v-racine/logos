import os
import sys
import psycopg2
from dotenv import load_dotenv

from src.infrastructure.db import PostgresPaperRepository, PostgresVectorStore
from src.infrastructure.embedding import OpenAIEmbeddingClient
from src.infrastructure.llm import OpenAILLMClient
from src.services.query import QueryService

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
paper_repo = PostgresPaperRepository(conn)
vector_store = PostgresVectorStore(conn)
embedding_client = OpenAIEmbeddingClient(api_key=os.getenv("OPENAI_API_KEY"))
llm_client = OpenAILLMClient(api_key=os.getenv("OPENAI_API_KEY"))

# Read path (question → search/retrieval → answer)
query_service = QueryService(
    embedding_client=embedding_client,
    vector_store=vector_store,
    llm_client=llm_client,
)

question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What is epistemic opacity?"

result = query_service.query(question)

print(f"\nQuestion: {question}")
print(f"\nAnswer: {result.answer}")
print("\n--- Retrieved Chunks ---")
for chunk in result.retrieved_chunks:
    print(f"\n[{chunk.paper_title}] (score:{chunk.similarity_score:.3f})")
    print(f"{chunk.content[:200]}...")

conn.close()
