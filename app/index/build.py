from typing import List, Dict
from pathlib import Path
import json

from app.core.config import settings
from app.index.faiss_index import FaissIndex
from app.index.qdrant_index import QdrantIndex
from app.index.tfidf_index import TfidfIndex
from app.index.hybrid_index import HybridIndex

_PROCESSED_DIR = Path("data/processed")

_INDEX_SINGLETON = None
_DENSE_SINGLETON = None
_BM25_SINGLETON = None

def _load_processed() -> List[Dict]:
    docs = []
    for p in _PROCESSED_DIR.glob("*.jsonl"):
        for line in p.read_text(encoding="utf-8").splitlines():
            docs.append(json.loads(line))
    return docs

def get_dense_index():
    global _DENSE_SINGLETON
    if _DENSE_SINGLETON is None:
        if settings.INDEX_BACKEND.lower() == "qdrant":
            _DENSE_SINGLETON = QdrantIndex()
        else:
            _DENSE_SINGLETON = FaissIndex()
    return _DENSE_SINGLETON

def get_bm25_index():
    global _BM25_SINGLETON
    if _BM25_SINGLETON is None:
        _BM25_SINGLETON = TfidfIndex()
    return _BM25_SINGLETON

def get_index():
    global _INDEX_SINGLETON
    if _INDEX_SINGLETON is None:
        if settings.INDEX_BACKEND.lower() == "hybrid":
            _INDEX_SINGLETON = HybridIndex(get_dense_index(), get_bm25_index())
        elif settings.INDEX_BACKEND.lower() == "qdrant":
            _INDEX_SINGLETON = QdrantIndex()
        else:
            _INDEX_SINGLETON = FaissIndex()
    return _INDEX_SINGLETON

def build_index() -> int:
    docs = _load_processed()
    if not docs:
        return 0
    texts = [d["text"] for d in docs]
    metas = [{"text": d["text"], "source": d.get("source", "") } for d in docs]
    # Always (re)build both dense and BM25 indices to support hybrid eval
    get_dense_index().add(texts, metas)
    get_bm25_index().add(texts, metas)
    # Initialize default index singleton
    _ = get_index()
    return len(texts)
