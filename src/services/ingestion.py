from src.domain.entities import Paper
from src.domain.interfaces import PDFParser, PaperRepository


class IngestionService:
    def __init__(self, parser: PDFParser, paper_repo: PaperRepository):
        self._parser = parser
        self._paper_repo = paper_repo

    def ingest(self, pdf_path: str, title: str, authors: str, source_url: str) -> int:
        content = self._parser.extract_text(pdf_path)
        paper = Paper(
            title=title,
            authors=authors,
            source_url=source_url,
            content=content,
        )
        paper_id = self._paper_repo.save_paper(paper)
        print(f"✓ Ingested '{title}' with id {paper_id}")
        return paper_id
