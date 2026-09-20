from flashrank import Ranker, RerankRequest

class LocalReranker:
    def __init__(self):
        self.ranker = Ranker()

    def rerank(self, query, documents, top_n=5):
        passages = [
            {"id": str(i), "text": d.page_content, "meta": d.metadata}
            for i, d in enumerate(documents)
        ]
        results = self.ranker.rerank(
            RerankRequest(query=query, passages=passages)
        )
        ranked = []
        for item in results[:top_n]:
            ranked.append(documents[int(item["id"])])
        return ranked
