from fastapi import FastAPI
from app.core.config import settings
from app.api import routes

app = FastAPI(title="RAG Q&A (Eval-Driven)")

app.include_router(routes.router)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "index_backend": settings.INDEX_BACKEND,
        "llm_mode": settings.LLM_MODE,
    }

