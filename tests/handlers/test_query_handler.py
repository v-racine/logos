from src.handlers.gradio_ui import GradioApp
from src.domain.entities import RetrievedChunk, QueryResult


class FakeQueryService:
    def __init__(self, answer="Test answer.", should_raise=False):
        self._answer = answer
        self._should_raise = should_raise

    def query(self, question, history=None):
        if self._should_raise:
            raise RuntimeError("something broke")
        return QueryResult(
            answer=self._answer,
            retrieved_chunks=[
                RetrievedChunk(
                    chunk_id=1,
                    paper_id=1,
                    content="Chunk content.",
                    chunk_index=0,
                    similarity_score=0.85,
                    paper_title="Test Paper",
                    source_url="https://example.com",
                    publication_year=2024,
                )
            ],
            full_prompt="[SYSTEM]\ntest\n\n[USER]\ntest",
        )


def test_empty_input_returns_unchanged_history():
    app = GradioApp(query_service=FakeQueryService())

    chat_history, history_state, chunks_md, prompt_md = app._handle_query("   ", [], [])
    assert chat_history == []
    assert history_state == []
    assert chunks_md == ""
    assert prompt_md == ""


def test_successful_query_appends_to_chat_history():
    app = GradioApp(query_service=FakeQueryService(answer="The answer."))

    chat_history, history_state, chunks_md, prompt_md = app._handle_query(
        "What is opacity?", [], []
    )

    assert len(chat_history) == 2
    assert chat_history[0] == {"role": "user", "content": "What is opacity?"}
    assert chat_history[1] == {"role": "assistant", "content": "The answer."}


def test_successful_query_appends_to_history_state():
    app = GradioApp(query_service=FakeQueryService(answer="The answer."))

    chat_history, history_state, chunks_md, prompt_md = app._handle_query(
        "What is opacity?", [], []
    )

    assert len(history_state) == 2
    assert history_state[0] == {"role": "user", "content": "What is opacity?"}
    assert history_state[1] == {"role": "assistant", "content": "The answer."}


def test_successful_query_preserves_existing_history():
    app = GradioApp(query_service=FakeQueryService(answer="Second answer."))
    existing_chat = [
        {"role": "user", "content": "first question"},
        {"role": "assistant", "content": "first answer"},
    ]
    existing_state = [
        {"role": "user", "content": "first question"},
        {"role": "assistant", "content": "first answer"},
    ]

    chat_history, history_state, _, _ = app._handle_query(
        "second question", existing_chat, existing_state
    )

    assert len(chat_history) == 4
    assert len(history_state) == 4
    assert chat_history[-1]["content"] == "Second answer."


def test_exception_returns_error_in_chat_history():
    app = GradioApp(query_service=FakeQueryService(should_raise=True))

    chat_history, history_state, chunks_md, prompt_md = app._handle_query(
        "test question", [], []
    )

    assert len(chat_history) == 2
    assert "Something went wrong" in chat_history[1]["content"]


def test_exception_does_not_modify_history_state():
    app = GradioApp(query_service=FakeQueryService(should_raise=True))

    chat_history, history_state, chunks_md, prompt_md = app._handle_query(
        "test question", [], []
    )

    assert history_state == []
