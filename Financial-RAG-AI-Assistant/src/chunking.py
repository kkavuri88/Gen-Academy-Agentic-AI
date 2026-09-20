from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker

def fixed_chunks(documents, chunk_size: int, overlap: int):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(documents)

def semantic_chunks(documents, embeddings):
    # SemanticChunker detects meaning shifts using embedding distances.
    # "percentile" is a practical default for a class project.
    splitter = SemanticChunker(
        embeddings,
        breakpoint_threshold_type="percentile",
        breakpoint_threshold_amount=95,
    )
    return splitter.split_documents(documents)
