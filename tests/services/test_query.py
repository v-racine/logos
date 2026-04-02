from src.services.query import QueryService
from src.domain.entities import RetrievedChunk, QueryResult, LLMResponse
from src.domain.interfaces import EmbeddingClient, VectorStore, LLMClient


def make_chunk():
    return RetrievedChunk(
        chunk_id=1,
        paper_id=1,
        content="Test content.",
        chunk_index=0,
        similarity_score=0.9,
        paper_title="Test Paper",
        source_url="https://example.com",
        publication_year=2024,
    )


class FakeEmbeddingClient(EmbeddingClient):
    def __init__(self):
        self.last_text = None

    def embed(self, text):
        self.last_text = text
        return [0.1, 0.2, 0.3]

    def embed_many(self, texts):
        return [[0.1, 0.2, 0.3] for _ in texts]


class FakeVectorStore(VectorStore):
    def __init__(self, chunks=None):
        self._chunks = chunks or [make_chunk()]
        self.last_embedding = None
        self.last_limit = None

    def save_chunks(self, chunks):
        pass

    def delete_all_chunks(self):
        pass

    def similarity_search(self, embedding, limit):
        self.last_embedding = embedding
        self.last_limit = limit
        return self._chunks


class FakeLLMClient(LLMClient):
    def __init__(self):
        self.last_query = None
        self.last_chunks = None
        self.last_history = None

    def generate(self, query, chunks, history=None):
        self.last_query = query
        self.last_chunks = chunks
        self.last_history = history

        return QueryResult(
            llm_response=LLMResponse(
                answer="Generated answer.",
                citations=[],
                caveat=None,
            ),
            retrieved_chunks=chunks,
            full_prompt="[SYSTEM]\ntest\n\n[USER]\ntest",
        )


def test_query_calls_embed_with_question():
    embedding_client = FakeEmbeddingClient()
    service = QueryService(
        embedding_client=embedding_client,
        vector_store=FakeVectorStore(),
        llm_client=FakeLLMClient(),
    )

    service.query("What is epistemic opacity?")

    assert embedding_client.last_text == "What is epistemic opacity?"


def test_query_passes_embedding_to_similarity_search():
    vector_store = FakeVectorStore()
    service = QueryService(
        embedding_client=FakeEmbeddingClient(),
        vector_store=vector_store,
        llm_client=FakeLLMClient(),
    )

    service.query("test question")

    assert vector_store.last_embedding == [0.1, 0.2, 0.3]
    assert vector_store.last_limit == 5


def test_query_passes_chunks_and_question_to_llm():
    chunks = [make_chunk()]
    llm_client = FakeLLMClient()
    service = QueryService(
        embedding_client=FakeEmbeddingClient(),
        vector_store=FakeVectorStore(chunks=chunks),
        llm_client=llm_client,
    )

    service.query("test question")

    assert llm_client.last_query == "test question"
    assert llm_client.last_chunks == chunks


def test_query_passes_history_to_llm():
    llm_client = FakeLLMClient()
    service = QueryService(
        embedding_client=FakeEmbeddingClient(),
        vector_store=FakeVectorStore(),
        llm_client=llm_client,
    )
    history = [
        {"role": "user", "content": "previous question"},
        {"role": "assistant", "content": "previous answer"},
    ]

    service.query("follow up question", history=history)

    assert llm_client.last_history == history


def test_query_passes_none_history_by_default():
    llm_client = FakeLLMClient()
    service = QueryService(
        embedding_client=FakeEmbeddingClient(),
        vector_store=FakeVectorStore(),
        llm_client=llm_client,
    )

    service.query("test question")

    assert llm_client.last_history is None


def test_query_returns_query_result():
    service = QueryService(
        embedding_client=FakeEmbeddingClient(),
        vector_store=FakeVectorStore(),
        llm_client=FakeLLMClient(),
    )

    result = service.query("test")

    assert isinstance(result, QueryResult)
    assert result.llm_response.answer == "Generated answer."
