RAG Q&A System — Evaluation‑Driven, Production‑Minded

Badges
- ![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
- ![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)
- ![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
- ![CI](https://img.shields.io/badge/CI-passing-brightgreen)
- ![Coverage](https://img.shields.io/badge/coverage-~80%25-blue)
- ![License](https://img.shields.io/badge/license-MIT-informational)

Highlights
- Hybrid retrieval: dense (sentence‑transformers) + BM25/TF‑IDF via Reciprocal Rank Fusion (RRF).
- Reranking: optional CrossEncoder reranker for higher‑quality top‑k.
- LLM adapters: local stub, LiteLLM proxy, or OpenRouter; swap with a flag.
- Eval harness: EM, F1, faithfulness, and retrieval recall across variants.
- Developer UX: FastAPI docs, Streamlit mini‑UI, Makefile tasks, Docker Compose.

Demo
- Streamlit overview
  - ![Streamlit UI](docs/ui-screenshot.svg)
  - Replace the placeholder with a real screenshot or GIF of `http://localhost:8501`.

Architecture
- Ingest: parse and chunk docs from `data/raw/` → `data/processed/`.
- Index: FAISS (local) or Qdrant (Compose); hybrid layer combines dense + TF‑IDF.
- Retrieve: dense, BM25/TF‑IDF, or hybrid (RRF) + optional reranker.
- Generate: LLM answers grounded in retrieved context (local/LiteLLM/OpenRouter).
- Evaluate: offline metrics for multiple retrieval/rerank variants.

Quick Start (Local)
1) Environment
   - `python -m venv .venv && source .venv/bin/activate`
   - `pip install -r requirements.txt`
2) Add content
   - Put PDFs/HTML/MD/TXT into `data/raw/` (sample docs included).
3) Build + run
   - `make ingest index`
   - `make api` → http://localhost:8000/docs
   - `make ui`  → http://localhost:8501

Quick Start (Docker Compose)
- `docker compose up --build`
  - Starts Qdrant, API, and UI. Defaults to `INDEX_BACKEND=qdrant`.

Configuration
- `INDEX_BACKEND`: `faiss` | `qdrant` | `hybrid` (default: `faiss`)
- `QDRANT_URL`: Qdrant endpoint (default: `http://qdrant:6333` in Compose)
- `LLM_MODE`: `local` | `litellm` | `openrouter` (default: `local`)
- `EMBEDDING_MODEL`: e.g., `sentence-transformers/all-MiniLM-L6-v2`
- `RERANKING`: `on` | `off` (default: `off`)
- `RERANKER_MODEL`: e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`
- `OPENROUTER_MODEL`, `OPENROUTER_API_KEY`, `LITELLM_BASE`, `LITELLM_MODEL`
- See `.env.example` for a reference (don’t commit real keys).

Make Targets
- `make ingest`: parse + chunk `data/raw/` into `data/processed/`
- `make index`: build dense and TF‑IDF indexes (supports hybrid)
- `make api`: run FastAPI server on :8000
- `make ui`: run Streamlit mini‑UI on :8501
- `make eval`: run offline eval (EM/F1/faithfulness/recall) for variants
- `make sample-baseline`: ingest + index sample docs and print retrieval metrics

API Endpoints
- `GET /health`: backend and mode summary
- `POST /ingest`: ingest from default folder or custom paths
- `POST /index`: build/update indexes
- `POST /search`: retrieve contexts for a query (respects hybrid/rerank)
- `POST /qa`: answer using retrieved contexts and configured LLM
- `POST /feedback`: persist thumbs‑up/down + comment

Evaluations
- Variants: `dense`, `dense+rerank`, `hybrid`, `hybrid+rerank`
- Metrics:
  - `em`: exact match to gold answer
  - `f1`: token‑level F1
  - `faithfulness`: share of answer tokens grounded in contexts
  - `retrieval_recall`: whether the gold snippet appears in top‑k
- Run: `make eval` (uses `eval/sets/sample.jsonl`)
- Tip: For real LLM answers, set `LLM_MODE=litellm|openrouter` and provide credentials. In `local` mode, answers are synthesized from context.

Project Structure
- `app/main.py`: FastAPI app entry
- `app/api/routes.py`: API routes
- `app/ingest/*`: file discovery, loaders, chunker, pipeline
- `app/embeddings/encoder.py`: sentence‑transformers with offline fallback
- `app/index/*`: FAISS, Qdrant, TF‑IDF, and Hybrid (RRF) backends; builder
- `app/retrieval/reranker.py`: CrossEncoder reranker (optional)
- `app/llm/adapters/*`: local stub, LiteLLM, OpenRouter
- `app/eval/harness.py`: evaluation harness (EM/F1/faithfulness/recall)
- `ui/app.py`: Streamlit mini‑UI
- `data/raw/`: your docs; sample content provided
- `eval/sets/`: synthetic QA set(s)

Sample Data
- Example docs: `data/raw/sample/`
- Synthetic QA set: `eval/sets/sample.jsonl`
- Baseline: `make sample-baseline`

Roadmap
- Proper BM25 baseline and comparison vs TF‑IDF
- Per‑query diffs and plots for variant comparisons
- Entailment‑based faithfulness scoring (when models available)
- OpenTelemetry traces and Prometheus metrics exporters by default
- Scripted QA generation from `data/raw/` for larger eval sets

Notes
- Offline friendly: if models can’t be downloaded, embeddings and reranker gracefully fall back to local heuristics.
- Security: keep secrets in environment variables or a local `.env` file.
