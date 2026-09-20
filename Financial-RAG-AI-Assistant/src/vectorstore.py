from langchain_chroma import Chroma

def build_store(chunks, embeddings, persist_dir, collection_name):
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(persist_dir),
        collection_name=collection_name,
    )

def load_store(embeddings, persist_dir, collection_name):
    return Chroma(
        embedding_function=embeddings,
        persist_directory=str(persist_dir),
        collection_name=collection_name,
    )
