import fitz #PyMuPDF
from src.domain.interfaces import PDFParser

class PyMuPDFParser(PDFParser):
  def extract_text(self, pdf_path: str) -> str:
    with fitz.open(pdf_path) as doc:
      text = "".join(page.get_text() for page in doc)
    return text.strip()
  