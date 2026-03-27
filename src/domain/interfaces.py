from abc import ABC, abstractmethod
from src.domain.entities import Paper, Chunk, RetrievedChunk, QueryResult

class EmbeddingClient(ABC):
    @abstractmethod
    def embed(self, text: str) -> list[float]:
        pass

    @abstractmethod
    def embed_many(self, texts: list[str]) -> list[list[float]]:
        pass

class LLMClient(ABC):
    @abstractmethod
    def generate(self, query: str, chunks: list[RetrievedChunk]) -> QueryResult:
        pass

class PDFParser(ABC):
    @abstractmethod
    def extract_text(self, pdf_path: str) -> str:
        pass
    
class VectorStore(ABC):
    @abstractmethod
    def save_paper(self, paper: Paper) -> int:
        pass

    @abstractmethod
    def save_chunks(self, chunks: list[Chunk]) -> None:
        pass

    @abstractmethod
    def similarity_search(
        self,
        embedding: list[float],
        limit: int
    ) -> list[RetrievedChunk]:
        pass

    @abstractmethod
    def get_all_papers(self) -> list[Paper]:
        pass