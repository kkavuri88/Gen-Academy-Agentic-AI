import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "data" / "jpmorgan_2024_annual_report.pdf"
VECTOR_DIR = ROOT / "vectorstores"
FIXED_DIR = VECTOR_DIR / "fixed"
SEMANTIC_DIR = VECTOR_DIR / "semantic"

CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4.1-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

FIXED_CHUNK_SIZE = 1000
FIXED_CHUNK_OVERLAP = 150
TOP_K_CANDIDATES = 10
TOP_K_FINAL = 5
