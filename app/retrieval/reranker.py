from __future__ import annotations
from typing import List, Dict, Tuple
from functools import lru_cache
from app.core.config import settings

class _NoopReranker:
    def score(self, query: str, texts: List[str]) -> List[float]:
        # basic heuristic: length-based proxy
        return [len(t) for t in texts]

@lru_cache(maxsize=1)
def _get_model():
    try:
        from sentence_transformers import CrossEncoder  # type: ignore
        return CrossEncoder(settings.RERANKER_MODEL)
    except Exception:
        return _NoopReranker()

def rerank_hits(query: str, hits: List[Dict], enabled: bool | None = None) -> List[Dict]:
    use_rerank = settings.RERANKING.lower() == "on" if enabled is None else enabled
    if not use_rerank or not hits:
        return hits
    model = _get_model()
    texts = [h.get("text", "") for h in hits]
    try:
        if hasattr(model, "predict"):
            pairs = [(query, t) for t in texts]
            scores = model.predict(pairs)
        else:
            scores = model.score(query, texts)
    except Exception:
        scores = [h.get("score", 0.0) for h in hits]
    scored = [dict(h, rerank_score=float(s)) for h, s in zip(hits, scores)]
    scored.sort(key=lambda x: x.get("rerank_score", x.get("score", 0.0)), reverse=True)
    return scored
