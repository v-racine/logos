from src.services.ingestion import IngestionService
from src.domain.interfaces import PDFParser, PaperRepository


class FakePDFParser(PDFParser):
    def __init__(self, text="Extracted text from PDF."):
        self._text = text
        self.last_path = None

    def extract_text(self, pdf_path):
        self.last_path = pdf_path
        return self._text


class FakePaperRepository(PaperRepository):
    def __init__(self, paper_id=42):
        self._paper_id = paper_id
        self.saved_paper = None

    def save_paper(self, paper):
        self.saved_paper = paper
        return self._paper_id

    def get_paper(self, paper_id):
        pass

    def get_all_papers(self):
        return []


def test_ingest_calls_parser_with_correct_path():
    parser = FakePDFParser()
    repo = FakePaperRepository()
    service = IngestionService(parser=parser, paper_repo=repo)

    service.ingest(
        pdf_path="data/papers/Duede(2023).pdf",
        title="Test",
        authors="Author",
        source_url="https://example.com",
    )

    assert parser.last_path == "data/papers/Duede(2023).pdf"


def test_ingest_saves_paper_with_all_fields():
    parser = FakePDFParser(text="The full paper content.")
    repo = FakePaperRepository()
    service = IngestionService(parser=parser, paper_repo=repo)

    service.ingest(
        pdf_path="data/papers/test.pdf",
        title="Deep Learning Opacity",
        authors="Eamon Duede",
        source_url="https://philsci-archive.pitt.edu/21085/",
        publication_year=2023,
    )

    assert repo.saved_paper.title == "Deep Learning Opacity"
    assert repo.saved_paper.authors == "Eamon Duede"
    assert repo.saved_paper.source_url == "https://philsci-archive.pitt.edu/21085/"
    assert repo.saved_paper.content == "The full paper content."
    assert repo.saved_paper.publication_year == 2023


def test_ingest_returns_paper_id():
    parser = FakePDFParser()
    repo = FakePaperRepository(paper_id=7)
    service = IngestionService(parser=parser, paper_repo=repo)

    result = service.ingest(
        pdf_path="test.pdf",
        title="Test",
        authors="Author",
        source_url="https://example.com",
    )

    assert result == 7


def test_ingest_without_publication_year_defaults_to_none():
    parser = FakePDFParser()
    repo = FakePaperRepository()
    service = IngestionService(parser=parser, paper_repo=repo)

    service.ingest(
        pdf_path="test.pdf",
        title="Test",
        authors="Author",
        source_url="https://example.com",
    )

    assert repo.saved_paper.publication_year is None
