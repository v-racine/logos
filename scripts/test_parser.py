from src.infrastructure.pdf_parser import PyMuPDFParser                  
   
parser = PyMuPDFParser()                                                 
text = parser.extract_text("data/papers/Peters(2024).pdf")
print(text[:2000])  # first 2000 chars to see what you're getting