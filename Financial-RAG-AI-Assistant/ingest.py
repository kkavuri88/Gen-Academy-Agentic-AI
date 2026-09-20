from shutil import rmtree
from src.config import (
    PDF_PATH, FIXED_DIR, SEMANTIC_DIR,
    FIXED_CHUNK_SIZE, FIXED_CHUNK_OVERLAP
)
from src.loader import load_pdf
from src.chunking import fixed_chunks, semantic_chunks
from src.rag import get_embeddings
from src.vectorstore import build_store

def main():
    if not PDF_PATH.exists():
        raise FileNotFoundError(
            f"Missing {PDF_PATH}. Put the annual-report PDF in data/ first."
        )

    print("Loading PDF...")
    docs = load_pdf(PDF_PATH)
    print(f"Loaded {len(docs)} pages.")

    embeddings = get_embeddings()

    print("Creating fixed-size chunks...")
    fixed = fixed_chunks(docs, FIXED_CHUNK_SIZE, FIXED_CHUNK_OVERLAP)
    print(f"Fixed chunks: {len(fixed)}")

    print("Creating semantic chunks (this uses embedding calls and can take time)...")
    semantic = semantic_chunks(docs, embeddings)
    print(f"Semantic chunks: {len(semantic)}")

    for p in (FIXED_DIR, SEMANTIC_DIR):
        if p.exists():
            rmtree(p)

    print("Building fixed vector store...")
    build_store(fixed, embeddings, FIXED_DIR, "fixed_chunks")

    print("Building semantic vector store...")
    build_store(semantic, embeddings, SEMANTIC_DIR, "semantic_chunks")

    print("Done. Both vector stores are ready.")

if __name__ == "__main__":
    main()
