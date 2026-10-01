import sys
import psycopg2
from src.config import Config


from src.infrastructure.db import PostgresVectorStore
from src.infrastructure.embedding import OpenAIEmbeddingClient
from src.infrastructure.llm import OpenAILLMClient
from src.services.query import QueryService

config = Config.from_env()
conn = psycopg2.connect(config.database_url)

vector_store = PostgresVectorStore(conn)
embedding_client = OpenAIEmbeddingClient(api_key=config.openai_api_key)
llm_client = OpenAILLMClient(api_key=config.openai_api_key)

# Read path (question → search/retrieval → answer)
query_service = QueryService(
    embedding_client=embedding_client,
    vector_store=vector_store,
    llm_client=llm_client,
)

question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What is epistemic opacity?"

result = query_service.query(question)

print(f"\nQuestion: {question}")
print(f"\nAnswer: {result.llm_response.answer}")
if result.llm_response.caveat:
    print(f"\nCaveat: {result.llm_response.caveat}")
print("\n--- Citations ---")
for citation in result.llm_response.citations:
    year = f" ({citation.year})" if citation.year else ""
    print(f"- {citation.authors}{year}. {citation.title}")
print("\n--- Retrieved Chunks ---")
for chunk in result.retrieved_chunks:
    print(f"\n[{chunk.paper_title}] (score:{chunk.similarity_score:.3f})")
    print(f"{chunk.content[:200]}...")

print("\n--- Full Prompt ---")
print(result.full_prompt)

conn.close()
