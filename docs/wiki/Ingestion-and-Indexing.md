Ingestion and Indexing

Ingestion
- Discovers files in data/raw/ (txt, md, pdf/html best-effort)
- Chunks text (simple fixed-size) → data/processed/chunks.jsonl
- Run: make ingest or POST /ingest

Indexing
- Dense: sentence-transformers embeddings (hash fallback offline)
- TF‑IDF: sklearn TfidfVectorizer persisted to index/tfidf
- Qdrant: created if missing; non-destructive
- Run: make index or POST /index

Hybrid
- Dense + TF‑IDF via Reciprocal Rank Fusion (RRF)
- Enable by setting INDEX_BACKEND=hybrid

