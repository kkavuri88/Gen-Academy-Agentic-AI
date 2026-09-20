import re
from langchain_community.document_loaders import PyPDFLoader

def _clean(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def load_pdf(path):
    docs = PyPDFLoader(str(path)).load()
    for d in docs:
        d.page_content = _clean(d.page_content)
        # Human-friendly page number while retaining original metadata.
        d.metadata["page_number"] = int(d.metadata.get("page", 0)) + 1
        d.metadata["source_name"] = path.name
    return [d for d in docs if d.page_content.strip()]
