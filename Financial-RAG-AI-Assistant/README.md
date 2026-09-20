# Financial RAG AI Assistant

Week 2 project for a Financial Document Intelligence RAG pipeline.

## Goal

Answer financial questions from a public annual report with grounded citations,
compare fixed-size and semantic chunking on the same queries, and measure the
effect of reranking.

## Architecture

PDF -> cleaning -> fixed/semantic chunking -> OpenAI embeddings -> Chroma ->
top-k retrieval -> local FlashRank reranker -> LLM -> answer with page citations

## Setup

1. Create and activate a virtual environment.

   Windows:
   `python -m venv .venv`
   `.venv\Scripts\activate`

2. Install dependencies:
   `pip install -r requirements.txt`

3. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.

4. Place the JPMorgan Chase 2024 Annual Report PDF in:
   `data/jpmorgan_2024_annual_report.pdf`

5. Build both vector stores:
   `python ingest.py`

6. Launch the app:
   `streamlit run app.py`

7. Generate evaluation output:
   `python evaluate.py`

## Evaluation design

Use the same questions against four configurations:

- Fixed chunks, no reranking
- Fixed chunks + reranking
- Semantic chunks, no reranking
- Semantic chunks + reranking

Before reporting retrieval accuracy, manually verify the correct source pages in
the annual report and populate `expected_pages` in
`evaluation/questions.json`. Do not fabricate scores.

Recommended metrics:
- Retrieval page hit rate
- Answer faithfulness (manual 0/1 or rubric)
- Correct refusal on unanswerable questions
- Optional response latency

## Project report sections

1. Project overview
2. Corpus/dataset
3. Ingestion and cleaning
4. Fixed-size chunking
5. Semantic chunking
6. Embedding/vector-store configuration
7. Retrieval and reranking
8. Prompt/instructions
9. Evaluation questions and methodology
10. Chunking comparison results
11. Reranking impact
12. Failure analysis
13. Learnings and iterations

## Important

Do not commit `.env`, API keys, or proprietary documents.
