from src.infrastructure.llm import OpenAILLMClient
from src.domain.entities import RetrievedChunk


def make_chunk(title="Test Paper", content="Some content", year=None):
    return RetrievedChunk(
        chunk_id=1,
        paper_id=1,
        content=content,
        chunk_index=0,
        similarity_score=0.9,
        paper_title=title,
        source_url="https://example.com",
        publication_year=year,
    )


def make_client():
    return OpenAILLMClient(api_key="sk-fake-key")


def test_build_context_single_chunk_with_year():
    client = make_client()
    chunks = [
        make_chunk(title="Deep Learning Opacity", content="DLMs are opaque.", year=2025)
    ]

    result = client._build_context(chunks)

    assert result == "[Source: Deep Learning Opacity (2025)]\nDLMs are opaque."


def test_build_context_single_chunk_without_year():
    client = make_client()
    chunks = [make_chunk(title="Deep Learning Opacity", content="DLMs are opaque.")]

    result = client._build_context(chunks)

    assert result == "[Source: Deep Learning Opacity]\nDLMs are opaque."


def test_build_context_multiple_chunks_joined_by_separator():
    client = make_client()
    chunks = [
        make_chunk(title="Paper A", content="Content A.", year=2023),
        make_chunk(title="Paper B", content="Content B.", year=2024),
    ]

    result = client._build_context(chunks)

    assert "\n\n***\n\n" in result
    assert "[Source: Paper A (2023)]" in result
    assert "[Source: Paper B (2024)]" in result


def test_build_context_empty_list():
    client = make_client()
    result = client._build_context([])

    assert result == ""


def test_system_prompt_contains_key_instructions():
    client = make_client()
    prompt = client._system_prompt()

    assert "philosophy of science" in prompt
    assert "publication year" in prompt.lower()
    assert "Do NOT hallucinate" in prompt


def test_system_prompt_has_no_missing_spaces():
    client = make_client()
    prompt = client._system_prompt()

    assert ".A" not in prompt
    assert ".C" not in prompt
    assert ".I" not in prompt
