Configuration

Core
- INDEX_BACKEND: faiss | qdrant | hybrid (default: faiss)
- LLM_MODE: local | litellm | openrouter (default: local)
- EMBEDDING_MODEL: sentence-transformers model id
- RERANKING: on | off (default: off)
- RERANKER_MODEL: cross-encoder model id

Vector DB
- QDRANT_URL: http://qdrant:6333 (Compose default)
- QDRANT_COLLECTION: docs (default)

LLM Providers
- OPENROUTER_MODEL, OPENROUTER_API_KEY
- LITELLM_BASE, LITELLM_MODEL

Tip
- See .env.example. Do not commit real keys.

