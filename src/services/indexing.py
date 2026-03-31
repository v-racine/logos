from nltk.tokenize import sent_tokenize

from src.domain.entities import Chunk
from src.domain.interfaces import PaperRepository, EmbeddingClient, VectorStore


class IndexingService:
    def __init__(
        self,
        paper_repo: PaperRepository,
        embedding_client: EmbeddingClient,
        vector_store: VectorStore,
        chunk_size: int = 1024,
        chunk_overlap: int = 100,
    ):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")

        self._paper_repo = paper_repo
        self._embedding_client = embedding_client
        self._vector_store = vector_store
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap

    # The main derive path. It indexes a single paper: read from source store →
    # chunk → embed → save to vector store.
    def index_paper(self, paper_id: int) -> int:
        paper = self._paper_repo.get_paper(paper_id)
        texts = self._chunk_text(paper.content)
        embeddings = self._embedding_client.embed_many(texts)

        chunks = [
            Chunk(
                paper_id=paper_id,
                content=text,
                chunk_index=i,
                embedding=embedding,
            )
            for i, (text, embedding) in enumerate(zip(texts, embeddings))
        ]

        self._vector_store.save_chunks(chunks)

        print(f"✓ Indexed '{paper.title}': {len(chunks)} chunks")
        return len(chunks)

    # Indexes every paper in source store
    def index_all(self) -> int:
        papers = self._paper_repo.get_all_papers()
        total = 0

        for paper in papers:
            total += self.index_paper(paper.id)
        return total

    def rebuild_index(self) -> int:
        self._vector_store.delete_all_chunks()

        print("✓ Cleared existing index")
        return self.index_all()

    def _chunk_text(self, text: str) -> list[str]:
        sentences = sent_tokenize(text)

        chunks = []
        current_sentences = []
        current_length = 0

        for sentence in sentences:
            sentence_len = len(sentence)

            if (
                current_length + sentence_len + 1 > self._chunk_size
                and current_sentences
            ):
                chunks.append(" ".join(current_sentences))

                # Build overlap from tail of current_sentences
                overlap_sentences = []
                overlap_len = 0
                for s in reversed(current_sentences):
                    if overlap_len + len(s) + 1 > self._chunk_overlap:
                        break
                    overlap_sentences.insert(0, s)
                    overlap_len += len(s) + 1

                current_sentences = overlap_sentences
                current_length = sum(len(s) + 1 for s in current_sentences)

            current_sentences.append(sentence)
            current_length += sentence_len + 1

        if current_sentences:
            chunks.append(" ".join(current_sentences))

        return chunks
