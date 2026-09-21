import streamlit as st
from src.config import FIXED_DIR, SEMANTIC_DIR
from src.rag import get_embeddings, answer_question
from src.vectorstore import load_store

st.set_page_config(page_title="Financial RAG AI Assistant", page_icon="📊", layout="wide")
st.markdown(
    """
    <style>
    :root {
        --truist-purple: #2e1a47;
        --truist-charcoal: #34363b;
        --truist-lilac: #f5f1f8;
        --truist-border: #ded5e7;
    }
    .stApp {
        background: linear-gradient(180deg, var(--truist-lilac) 0, #ffffff 260px);
        color: var(--truist-charcoal);
    }
    .block-container {
        max-width: 1080px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }
    h1, h2, h3 { color: var(--truist-purple) !important; }
    h1 { font-weight: 750 !important; letter-spacing: -0.035em; }
    [data-testid="stCaptionContainer"] { color: #625a6b; margin-bottom: 2rem; }
    [data-testid="stSidebar"] {
        background: var(--truist-lilac);
        border-right: 1px solid var(--truist-border);
    }
    [data-testid="stTextInput"] input { border-radius: 8px; }
    [data-testid="stTextInput"] input:focus {
        border-color: var(--truist-purple);
        box-shadow: 0 0 0 2px #2e1a4726;
    }
    [data-testid="stButton"] button[kind="primary"] {
        background: var(--truist-purple);
        border: 1px solid var(--truist-purple);
        border-radius: 8px;
        color: #ffffff;
        font-weight: 650;
        padding-inline: 1.75rem;
    }
    [data-testid="stButton"] button[kind="primary"]:hover {
        background: #42265f;
        border-color: #42265f;
    }
    [data-testid="stExpander"] {
        border: 1px solid var(--truist-border);
        border-radius: 8px;
        background: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("Financial RAG AI Assistant")
st.caption("AI-powered question answering over the JPMorgan Chase 2024 Annual Report")

if not FIXED_DIR.exists() or not SEMANTIC_DIR.exists():
    st.error("Vector stores not found. Run: python ingest.py")
    st.stop()

@st.cache_resource
def stores():
    emb = get_embeddings()
    return {
        "Fixed-size chunking": load_store(emb, FIXED_DIR, "fixed_chunks"),
        "Semantic chunking": load_store(emb, SEMANTIC_DIR, "semantic_chunks"),
    }

strategy = st.sidebar.selectbox("Chunking strategy", ["Fixed-size chunking", "Semantic chunking"])
rerank = st.sidebar.toggle("Use reranking", value=True)

question = st.text_input(
    "Ask a question about the annual report",
    placeholder="What were the major drivers of net income?"
)

if st.button("Ask", type="primary") and question.strip():
    with st.spinner("Retrieving and generating a grounded answer..."):
        result = answer_question(stores()[strategy], question, rerank=rerank)

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Retrieved sources")
    st.write("Pages:", ", ".join(map(str, result["pages"])) if result["pages"] else "Unknown")

    with st.expander("Show retrieved context"):
        for i, d in enumerate(result["documents"], 1):
            st.markdown(f"**Result {i} — page {d.metadata.get('page_number', '?')}**")
            st.write(d.page_content[:1800])
