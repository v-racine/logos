import psycopg2
from src.config import Config

from src.infrastructure.db import PostgresPaperRepository
from src.infrastructure.pdf_parser import PyMuPDFParser
from src.services.ingestion import IngestionService

config = Config.from_env()

conn = psycopg2.connect(config.database_url)
paper_repo = PostgresPaperRepository(conn)
parser = PyMuPDFParser()

# Write path (PDF → source store)
ingestion = IngestionService(parser=parser, paper_repo=paper_repo)

papers = [
    {
        "pdf_path": "data/papers/Duede(2023).pdf",
        "title": "Deep Learning Opacity in Scientific Discovery",
        "authors": "Eamon Duede",
        "source_url": "https://philsci-archive.pitt.edu/21085/",
    },
    {
        "pdf_path": "data/papers/Koskinen(2024).pdf",
        "title": "We Have No Satisfactory Social Epistemology of AI-Based Science",
        "authors": "Inkeri Koskinen",
        "source_url": "https://philsci-archive.pitt.edu/22780/",
    },
    {
        "pdf_path": "data/papers/Peters(2024).pdf",
        "title": "Science Based on Artificial Intelligence Need Not Pose a Social Epistemological Problem",
        "authors": "Uwe Peters",
        "source_url": "https://social-epistemology.com/wp-content/uploads/2024/01/peters_reply_koskinen_serrc_1-26-2024.pdf",
    },
]

for p in papers:
    ingestion.ingest(**p)

conn.close()
