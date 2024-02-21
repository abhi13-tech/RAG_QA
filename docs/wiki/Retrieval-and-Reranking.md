Retrieval and Reranking

Retrievers
- Dense (FAISS or Qdrant)
- TF‑IDF (cosine similarity)
- Hybrid (RRF merge of dense + TF‑IDF)

Reranker (optional)
- CrossEncoder model scores (query, passage) pairs
- Enable with RERANKING=on

Tuning Tips
- Adjust EMBEDDING_MODEL and RERANKER_MODEL
- Try hybrid first; then add rerank for quality at small k

