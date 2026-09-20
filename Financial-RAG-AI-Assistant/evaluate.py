import json
import pandas as pd
from src.config import ROOT, FIXED_DIR, SEMANTIC_DIR
from src.rag import get_embeddings, retrieve
from src.vectorstore import load_store

def page_set(docs):
    return {d.metadata.get("page_number") for d in docs if d.metadata.get("page_number")}

def hit(retrieved_pages, expected_pages):
    # Populate expected_pages after manually validating the report.
    if not expected_pages:
        return None
    return int(bool(set(expected_pages) & set(retrieved_pages)))

def main():
    questions = json.loads((ROOT / "evaluation" / "questions.json").read_text())
    emb = get_embeddings()
    stores = {
        "fixed": load_store(emb, FIXED_DIR, "fixed_chunks"),
        "semantic": load_store(emb, SEMANTIC_DIR, "semantic_chunks"),
    }

    rows = []
    for item in questions:
        q = item["question"]
        expected = item.get("expected_pages", [])
        for strategy, store in stores.items():
            for rerank in (False, True):
                docs = retrieve(store, q, rerank=rerank)
                pages = sorted(page_set(docs))
                rows.append({
                    "question_id": item["id"],
                    "question": q,
                    "strategy": strategy,
                    "reranked": rerank,
                    "retrieved_pages": ",".join(map(str, pages)),
                    "expected_pages": ",".join(map(str, expected)),
                    "page_hit": hit(pages, expected),
                    "notes": ""
                })

    out = ROOT / "evaluation" / "results.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f"Wrote {out}")
    print("Next: validate expected pages and add qualitative notes for your report.")

if __name__ == "__main__":
    main()
