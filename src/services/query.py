from src.domain.entities import QueryResult
from src.domain.interfaces import EmbeddingClient, VectorStore, LLMClient


# The main read path: question → embed → search → generate answer
class QueryService:
    def __init__(
        self,
        embedding_client: EmbeddingClient,
        vector_store: VectorStore,
        llm_client: LLMClient,
        top_k: int = 5,
    ):
        self._embedding_client = embedding_client
        self._vector_store = vector_store
        self._llm_client = llm_client
        self._top_k = top_k

    def query(self, question: str, history: list[dict] | None = None) -> QueryResult:
        embedding = self._embedding_client.embed(question)
        chunks = self._vector_store.similarity_search(embedding, self._top_k)

        result = self._llm_client.generate(question, chunks, history=history)
        return result
