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
    {
        "pdf_path": "data/papers/Koskinen(2024b).pdf",
        "title": "We Still Have No Satisfactory Social Epistemology of AI-Based Science: A Response to Peters",
        "authors": "Inkeri Koskinen",
        "source_url": "https://wp.me/p1Bfg0-8LL",
    },
    {
        "pdf_path": "data/papers/Peters(2024b)-Living-with-Uncertainty.pdf",
        "title": "Living with Uncertainty: Full Transparency of AI isn't Needed for Epistemic Trust in AI-based Science",
        "authors": "Uwe Peters",
        "source_url": "https://philarchive.org/archive/PETLWU",
    },
    {
        "pdf_path": "data/papers/Ortmann(2025).pdf",
        "title": "Of Opaque Oracles: Epistemic Dependence on AI in Science Poses No Novel Problems for Social Epistemology",
        "authors": "Jakob Ortmann",
        "source_url": "https://doi.org/10.1007/s11229-025-04930-x",
    },
    {
        "pdf_path": "data/papers/Andrews(2025)-Theory-Free-Ideal.pdf",
        "title": "The Immortal Science of ML: Machine Learning & the Theory-Free Ideal",
        "authors": "Med Andrews",
        "source_url": "https://philsci-archive.pitt.edu/26075/",
    },
    {
        "pdf_path": "data/papers/Zakharova(2024).pdf",
        "title": "The Epistemology of AI-Driven Science: The Case of AlphaFold",
        "authors": "Daria Zakharova",
        "source_url": "https://philsci-archive.pitt.edu/26659/",
    },
    {
        "pdf_path": "data/papers/Grote-Genin-Sullivan(2024)-Reliability.pdf",
        "title": "Reliability in Machine Learning",
        "authors": "Thomas Grote, Konstantine Genin, Emily Sullivan",
        "source_url": "https://doi.org/10.1111/phc3.12974",
    },
    {
        "pdf_path": "data/papers/Duede-Davey(2024).pdf",
        "title": "Apriori Knowledge in an Era of Computational Opacity: The Role of AI in Mathematical Discovery",
        "authors": "Eamon Duede, Kevin Davey",
        "source_url": "https://philsci-archive.pitt.edu/24406/",
    },
    {
        "pdf_path": "data/papers/Curtis-Trudel-Roe-Voudouris(2025).pdf",
        "title": "How Deep Learning Can Justify Pursuit, and Why It Matters",
        "authors": "Andre E. Curtis-Trudel, Niall Roe, Konstantinos Voudouris",
        "source_url": "https://philsci-archive.pitt.edu/26983/",
    },
    {
        "pdf_path": "data/papers/Pietsch(2026).pdf",
        "title": "Nothing New Under the Sun - Large Language Models and Scientific Method",
        "authors": "Wolfgang Pietsch",
        "source_url": "https://philsci-archive.pitt.edu/28259/",
    },
    {
        "pdf_path": "data/papers/Thais-et-al(2026).pdf",
        "title": "AI for Science Needs Scientific Alignment",
        "authors": "Savannah Thais, Roberto Trotta, Nathan Suri, Emily Sullivan, Viyan Poonamallee, Tanaporan Na Narong, Rupert Croft, Nicole Hartman",
        "source_url": "https://philsci-archive.pitt.edu/28744/",
    },
    {
        "pdf_path": "data/papers/Zahavy(2026).pdf",
        "title": "LLMs Can't Jump",
        "authors": "Tom Zahavy",
        "source_url": "https://philsci-archive.pitt.edu/28024/",
    },
    {
        "pdf_path": "data/papers/Duede-Friedman(2025).pdf",
        "title": "Epistemic Gaps and the Attribution of (AI) Discovery",
        "authors": "Eamon Duede, Daniel Friedman",
        "source_url": "https://philsci-archive.pitt.edu/27719/",
    },
    {
        "pdf_path": "data/papers/Ladyman-Nefdt(2026).pdf",
        "title": "Are AI Language Models Scientific Models of Language?",
        "authors": "James Ladyman, Ryan M. Nefdt",
        "source_url": "https://philsci-archive.pitt.edu/27973/",
    },
    {
        "pdf_path": "data/papers/Duran(2025).pdf",
        "title": "Beyond Transparency: Computational Reliabilism as an Externalist Epistemology of Algorithms",
        "authors": "Juan Manuel Duran",
        "source_url": "https://philsci-archive.pitt.edu/23832/",
    },
    {
        "pdf_path": "data/papers/Peters-Chin-Yee(2025).pdf",
        "title": "Generalization Bias in Large Language Model Summarization of Scientific Research",
        "authors": "Uwe Peters, Benjamin Chin-Yee",
        "source_url": "https://philsci-archive.pitt.edu/25144/",
    },
    {
        "pdf_path": "data/papers/Jensen(2025).pdf",
        "title": "Uncertainties about Link Uncertainty: ML Models as Phenomenological Models",
        "authors": "Sara Pernille Jensen",
        "source_url": "https://philsci-archive.pitt.edu/26781/",
    },
    {
        "pdf_path": "data/papers/Ratti(2025).pdf",
        "title": "Epistemic Control and the Normativity of Machine Learning-Based Science",
        "authors": "Emanuele Ratti",
        "source_url": "https://philsci-archive.pitt.edu/27926/",
    },
    {
        "pdf_path": "data/papers/Boge(2025).pdf",
        "title": "Understanding (and) Machine Learning's Black Box Explanation Problems",
        "authors": "Florian J. Boge",
        "source_url": "https://philsci-archive.pitt.edu/26251/",
    },
]

for p in papers:
    ingestion.ingest(**p)

conn.close()
