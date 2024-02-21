Architecture

Components
- Ingest: loaders + chunker → data/processed/*.jsonl
- Index: FAISS (local) or Qdrant (Compose); TF‑IDF for hybrid
- Retrieval: dense, TF‑IDF, or hybrid (RRF)
- Reranker: CrossEncoder (optional)
- LLM: local stub, LiteLLM, or OpenRouter
- API/UI: FastAPI + Streamlit
- Eval: metrics across retrieval variants

Data Flow
1) data/raw/* → ingest → data/processed/chunks.jsonl
2) build index (dense + TF‑IDF)
3) search top‑k, optional rerank
4) answer with LLM using contexts
5) eval metrics (EM/F1/faithfulness/recall)

