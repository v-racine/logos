import pytest
from nltk.tokenize import sent_tokenize
from src.services.indexing import IndexingService
from src.domain.interfaces import PaperRepository, EmbeddingClient, VectorStore


class FakePaperRepository(PaperRepository):
    def save_paper(self, paper):
        return 1

    def get_paper(self, paper_id):
        pass

    def get_all_papers(self):
        return []


class FakeEmbeddingClient(EmbeddingClient):
    def embed(self, text):
        return [0.1]

    def embed_many(self, texts):
        return [[0.1] for _ in texts]


class FakeVectorStore(VectorStore):
    def save_chunks(self, chunks):
        pass

    def delete_all_chunks(self):
        pass

    def similarity_search(self, embedding, limit):
        return []


def make_service(chunk_size=100, chunk_overlap=20):
    return IndexingService(
        paper_repo=FakePaperRepository(),
        embedding_client=FakeEmbeddingClient(),
        vector_store=FakeVectorStore(),
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )


def test_short_text_produces_single_chunk():
    service = make_service()
    chunks = service._chunk_text("This is a short sentence.")
    assert len(chunks) == 1
    assert chunks[0] == "This is a short sentence."


def test_long_text_produces_multiple_chunks():
    service = make_service(chunk_size=50, chunk_overlap=10)
    text = "First sentence here. Second sentence here. Third sentence is also here. Fourth sentence too."
    chunks = service._chunk_text(text)
    assert len(chunks) > 1


def test_chunks_never_end_mid_sentence():
    service = make_service(chunk_size=80, chunk_overlap=20)
    text = "The first claim is important. The second claim follows. The third claim is also relevant. And a fourth."
    chunks = service._chunk_text(text)
    for chunk in chunks:
        assert chunk.rstrip().endswith((".", "!", "?")) or chunk == chunks[-1]


def test_overlap_carries_tail_sentences():
    service = make_service(chunk_size=60, chunk_overlap=30)
    text = "Sentence one. Sentence two. Sentence three. Sentence four. Sentence five."
    chunks = service._chunk_text(text)
    if len(chunks) >= 2:
        first_chunk_sentences = sent_tokenize(chunks[0])
        last_sentence = first_chunk_sentences[-1]
        assert last_sentence in chunks[1]


def test_single_long_sentence_kept_whole():
    service = make_service(chunk_size=20, chunk_overlap=5)
    text = "This is a single very long sentence that exceeds the chunk size limit."
    chunks = service._chunk_text(text)

    assert len(chunks) == 1
    assert chunks[0] == text


def test_empty_string_produces_empty_list():
    service = make_service()
    chunks = service._chunk_text("")
    assert chunks == []


def test_constructor_rejects_overlap_gte_chunk_size():
    with pytest.raises(ValueError):
        make_service(chunk_size=100, chunk_overlap=100)

    with pytest.raises(ValueError):
        make_service(chunk_size=100, chunk_overlap=150)
