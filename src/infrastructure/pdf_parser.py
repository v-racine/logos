import fitz #PyMuPDF
from src.domain.interfaces import PDFParser

class PyMuPDFParser(PDFParser):
  def extract_text(self, pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
      text += page.get_text()
    doc.close()
    return text.strip()
  