import os

class Settings:
    INDEX_BACKEND: str = os.getenv("INDEX_BACKEND", "faiss")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    COLLECTION: str = os.getenv("QDRANT_COLLECTION", "docs")

    LLM_MODE: str = os.getenv("LLM_MODE", "local")  # local|litellm|openrouter
    LITELLM_MODEL: str = os.getenv("LITELLM_MODEL", "gpt-3.5-turbo")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")

    # Embeddings and Reranking
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    RERANKING: str = os.getenv("RERANKING", "off")  # on|off
    RERANKER_MODEL: str = os.getenv("RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")

settings = Settings()
