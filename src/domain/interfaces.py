from abc import ABC, abstractmethod
from src.domain.entities import RetrievedChunk, QueryResult

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