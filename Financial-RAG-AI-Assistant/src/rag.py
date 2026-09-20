from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from .config import CHAT_MODEL, EMBEDDING_MODEL, TOP_K_CANDIDATES, TOP_K_FINAL
from .reranker import LocalReranker

SYSTEM = '''You are a financial document analysis assistant.
Answer ONLY from the supplied annual-report context.

Rules:
1. Do not use outside knowledge.
2. Do not invent financial figures, dates, or conclusions.
3. If the context is insufficient, say exactly:
   "I could not find sufficient information in the annual report to answer this question."
4. Be concise but complete.
5. Cite supporting pages inline as [p. X].
'''

def get_embeddings():
    return OpenAIEmbeddings(model=EMBEDDING_MODEL)

def _format_context(docs):
    blocks = []
    for d in docs:
        page = d.metadata.get("page_number", "?")
        blocks.append(f"[PAGE {page}]\n{d.page_content}")
    return "\n\n---\n\n".join(blocks)

def retrieve(store, question, rerank=True):
    candidates = store.similarity_search(question, k=TOP_K_CANDIDATES)
    if rerank:
        candidates = LocalReranker().rerank(question, candidates, TOP_K_FINAL)
    else:
        candidates = candidates[:TOP_K_FINAL]
    return candidates

def answer_question(store, question, rerank=True):
    docs = retrieve(store, question, rerank=rerank)
    context = _format_context(docs)
    llm = ChatOpenAI(model=CHAT_MODEL, temperature=0)
    msg = llm.invoke([
        ("system", SYSTEM),
        ("human", f"Context:\n{context}\n\nQuestion: {question}")
    ])
    pages = sorted({d.metadata.get("page_number") for d in docs if d.metadata.get("page_number")})
    return {"answer": msg.content, "pages": pages, "documents": docs}
